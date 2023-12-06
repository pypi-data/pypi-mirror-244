"""
iogp.data.carve: File carving / extraction APIs.

*coin regexes adapted from https://github.com/Concinnity-Risks/RansomCoinPublic

Author: Vlad Topan (vtopan/gmail)
"""
import collections
import mmap
import re
import struct


PAT = {
    'Bitcoin Private Key': '5[HJK][1-9A-Za-z][A-HJ-NP-Za-km-z]{48}',
	'Bitcoin Address': '[13][a-km-zA-HJ-NP-Z1-9]{25,34}',
    'Bitcoin Cash Address': '(bitcoincash:)?[qp][a-z0-9]{41}|(BITCOINCASH:)?[QP][A-Z0-9]{41}',
    'Ethereum Address': '0x[a-fA-F0-9]{40}',
    'Litecoin Address': '[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}',
}
RX = {
    'file_magic': (rb'(7z)\xBC\xAF\x27\x1C|(PK)\x01\x02|(BM)|(MZ).{1,200}PE\0\0|(\xFF\xD8\xFF)|\x7F(ELF)|(GIF)8[79]', re.S),
    'text_file': (rb'[\x20-\x7E\x09\x0A\x0D]{512,}',),
    'jpg_end': (rb'\xFF\xD9',),
}
for k in RX:
    RX[k] = re.compile(*RX[k])

MAGIC_MAP = {
    b'7z': '7z',
    b'PK': 'zip',
    b'BM': 'bmp',
    b'MZ': 'exe',
    b'\xFF\xD8\xFF': 'jpg',
    b'ELF': 'elf',
    b'GIF': 'gif',
}

ZIP_POTENTIAL_CDS = set()


def extract_jpg(data, offset):
    """
    Extract a JPG image.
    """
    if offset + 0x100 > len(data):
        return None, None
    m = RX['jpg_end'].search(data, pos=offset)
    if m:
        return m.end(), 'jpg'
    return None, None


def extract_exe(data, offset):
    """
    Extract an MZ/PE image.
    """
    if offset + 0x400 > len(data):
        return None, None
    e_lfanew = struct.unpack('<i', data[offset + 0x3C:offset + 0x40])[0]
    peoffs = offset + e_lfanew
    if e_lfanew < 0 or peoffs + 0x1000 > len(data) or data[peoffs:peoffs + 4] != b'PE\0\0':
        return None, None
    seccnt = struct.unpack('<H', data[peoffs + 6:peoffs + 8])[0]
    secoffs = peoffs + 0xF8
    endoffs = -1
    for i in range(seccnt):
        offs = secoffs + i * 40 + 16
        fsize, faddr = struct.unpack('<II', data[offs:offs + 8])
        if fsize:
            endoffs = max(endoffs, faddr + fsize)
    return endoffs, 'exe'


def extract_zip(data, offset):
    """
    Extract a zip archive.
    """
    if offset in ZIP_POTENTIAL_CDS:
        return None, None
    # regex finds central directory entries, must validate each one - can mark checked ones though
    crt_offs = cd_start = offset
    delta = 28
    while 1:
        ZIP_POTENTIAL_CDS.add(crt_offs)
        base = crt_offs + delta
        fmt = '<HHHHHII'
        fmt_size = struct.calcsize(fmt)
        fn_len, ext_len, cmt_len, _, _, _, lfh_offs = struct.unpack(fmt, data[base:base + fmt_size])
        crt_offs += delta + fmt_size + fn_len + ext_len + cmt_len
        next_magic = data[crt_offs:crt_offs + 4]
        if next_magic[:2] != b'PK':
            return None, None
        if next_magic[2:4] != b'\x01\x02':
            if next_magic[2:4] == b'\x06\x06':
                # EOCDR64
                fmt = '<IQHHIIQQQQ'
                _, size, _, _, _, _, _, _, _, rel_offs = struct.unpack(fmt, data[crt_offs:crt_offs + struct.calcsize(fmt)])
                crt_offs += 12 + size
                next_magic = data[crt_offs:crt_offs + 4]
                if next_magic[:2] != b'PK':
                    return None, None
            if next_magic[2:4] == b'\x06\x07':
                # EOCDL64
                crt_offs += 20
                next_magic = data[crt_offs:crt_offs + 4]
                if next_magic[:2] != b'PK':
                    return None, None
            if next_magic[2:4] == b'\x05\x06':
                # EOCD
                fmt = '<IHHHHIIH'
                _, _, _, _, _, _, rel_offs, cmt_len = struct.unpack(fmt, data[crt_offs:crt_offs + struct.calcsize(fmt)])
                crt_offs += 22 + cmt_len
                start = cd_start - rel_offs
                if start < 0 or data[start:start + 4] != b'PK\x03\x04':
                    return None, None
                return (crt_offs - start, 'zip', start)
            else:
                return None, None


def extract_7z(data, offset):
    """
    Extract a 7z archive.
    """
    magic, ver_maj, ver_min, crc, next_offs, next_size, next_crc = struct.unpack('<6sBBIQQI', data[offset:offset + 32])
    if ver_maj != 0 or ver_min > 10:
        return None, None
    size = 32 + next_offs + next_size
    if offset + size > len(data):
        return None, None
    return size, '7z'


def extract_bmp(data, offset):
    """
    Extract a bitmap image.
    """
    magic, size, zero, offs = struct.unpack('<2sIII', data[offset:offset + 14])
    if zero != 0 or offset + offs > len(data) or offset + size > len(data):
        return None, None
    return size, 'bmp'


def extract_elf(data, offset):
    """
    Extract an ELF binary.
    """
    is64 = data[offset + 4] == 2
    spat, base, size = ('<QQIHHHHH', 0x20, 30) if is64 else ('<IIIHHHHH', 0x1C, 22)
    e_phoff, e_shoff, _, _, e_phentsize, e_phnum, e_shentsize, e_shnum  = struct.unpack(spat, data[offset + base:offset + base + size])
    szmax = 0
    for i in range(e_shnum):
        offs = e_shoff + e_shentsize * i
        offs, size = struct.unpack('<II', data[offs + 16:offs + 24])
        if size:
            szmax = max(szmax, offs + size)
    for i in range(e_phnum):
        offs = e_phoff + e_phentsize * i
        offs, _, _, size = struct.unpack('<IIII', data[offs + 4:offs + 20])
        if size:
            szmax = max(szmax, offs + size)
    return szmax, 'elf'


def extract_embedded_files(data, whitelist=None, to_eof=False):
    """
    Extract embedded files from the given `bytes` buffer (or `mmap` object), returns

    :param whitelist: List of extensions to extract (default: all known).
    :return: Yields tuples (offset, size, extension); size is None if unknown.
    """
    global ZIP_POTENTIAL_CDS
    ZIP_POTENTIAL_CDS = set()
    for m in RX['file_magic'].finditer(data, pos=1):
        magic = [x for x in m.groups() if x][0]
        if whitelist and MAGIC_MAP[magic] not in whitelist:
            continue
        ext = MAGIC_MAP[magic]
        offset = m.start()
        extractor = globals().get('extract_' + ext)
        if extractor and not to_eof:
            res = extractor(data, offset)
            size, ext = res[:2]
            if len(res) == 3:
                offset = res[-1]
            if size == 0:
                size = len(data) - offset
        else:
            size = len(data) - offset
        if ext is not None:
            yield (offset, size, ext)


if __name__ == '__main__':
    import glob
    import os
    import sys
    import mmap

    whitelist = None if len(sys.argv) < 3 else [x.strip().lower() for x in sys.argv[2].split(',')]
    for f in glob.glob(sys.argv[1]):
        print(f'[*] Carving {f}...')
        fh = open(f, 'rb')
        data = mmap.mmap(f.fileno(), 0)
        for offs, size, ext in extract_embedded_files(data, whitelist):
            fn = f'{os.path.basename(f)}.emb@{offs:X}.{ext}'
            print(f'[-]   - found {ext} @ 0x{offs:X}[{size}] - saving as {fn}...')
            open(fn, 'wb').write(data[offs:offs + size])
