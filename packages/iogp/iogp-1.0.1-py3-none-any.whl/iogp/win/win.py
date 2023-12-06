"""
iogp.win: ctypes-based wrappers over useful Windows APIs.

Example usage: iterating all windows

    import iogp.win as win
    def callback(hwnd, lparam):
        size = 512
        buf = win.unicode_buffer(size)
        win.GetWindowText(hwnd, buf, size)
        print(f'[-] Handle: {hwnd}, title: {buf.value}')
        return 1  # 0 to stop
    win.EnumWindows(win.WNDENUMPROC(callback), 0)

Author: Vlad Ioan Topan (vtopan/gmail).
"""

import ctypes
from ctypes import byref, cast, windll, get_last_error, FormatError, c_void_p, c_int, \
    Structure, POINTER, WINFUNCTYPE
from ctypes.wintypes import BOOL, BYTE, WORD, DWORD, HANDLE, HWND, LPWSTR, LPARAM, HDC, RECT, \
    POINT, UINT


user32 = windll.user32
kernel32 = windll.kernel32
gdi32 = windll.gdi32
INVALID_HANDLE_VALUE = c_void_p(-1).value
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PDWORD = POINTER(DWORD)
PVOID = c_void_p

MAX_PATH = 260
SRCCOPY = 0xCC0020
DIB_RGB_COLORS = 0


# Structures

class RGBQUAD(Structure):
    _fields_ = [
        ("rgbBlue", BYTE),
        ("rgbGreen", BYTE),
        ("rgbRed", BYTE),
        ("rgbReserved", BYTE),
    ]
PRGBQUAD = POINTER(RGBQUAD)     # NOQA


class BITMAPINFOHEADER(Structure):
    _fields_ = [
        ("biSize", DWORD),
        ("biWidth", DWORD),
        ("biHeight", DWORD),
        ("biPlanes", WORD),
        ("biBitCount", WORD),
        ("biCompression", DWORD),
        ("biSizeImage", DWORD),
        ("biXPelsPerMeter", DWORD),
        ("biYPelsPerMeter", DWORD),
        ("biClrUsed", DWORD),
        ("biClrImportant", DWORD),
    ]
PBITMAPINFOHEADER = POINTER(BITMAPINFOHEADER)   # NOQA


class BITMAPINFO(Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", RGBQUAD * 1),
    ]
PBITMAPINFO = POINTER(BITMAPINFO)   # NOQA


### Windows APIs

GetActiveWindow = WINFUNCTYPE(HWND)(("GetActiveWindow", user32))
# (hWnd)
SetActiveWindow = WINFUNCTYPE(HWND, HWND)(("SetActiveWindow", user32))
GetForegroundWindow = WINFUNCTYPE(HWND)(("GetForegroundWindow", user32))
# (hWnd)
SetForegroundWindow = WINFUNCTYPE(BOOL, HWND)(("SetForegroundWindow", user32))
# (hWnd)
SetFocus = WINFUNCTYPE(HWND, HWND)(("SetFocus", user32))
# (lpClassName, lpWindowName)
FindWindow = WINFUNCTYPE(HWND, LPWSTR, LPWSTR)(("FindWindowW", user32))
# (hwnd, lParam) - callback for EnumWindows
WNDENUMPROC = WINFUNCTYPE(BOOL, HWND, LPARAM)
# (lpEnumFunc, lParam)
EnumWindows = WINFUNCTYPE(BOOL, WNDENUMPROC, LPARAM)(("EnumWindows", user32))
# (hWnd, lpString, nMaxCount)
GetWindowText = WINFUNCTYPE(c_int, HWND, LPWSTR, c_int)(("GetWindowTextW", user32))
# (hWnd, lpdwProcessId)
GetWindowThreadProcessId = WINFUNCTYPE(DWORD, HWND, PDWORD)(("GetWindowThreadProcessId", user32))
# (dwDesiredAccess, bInheritHandle, dwProcessId)
OpenProcess = WINFUNCTYPE(HANDLE, DWORD, BOOL, DWORD)(("OpenProcess", kernel32))
# (hProcess, dwFlags, lpExeName, lpdwSize)
QueryFullProcessImageName = WINFUNCTYPE(BOOL, HANDLE, DWORD, LPWSTR,
        PDWORD)(("QueryFullProcessImageNameW", kernel32))
# (hObject)
CloseHandle = WINFUNCTYPE(BOOL, HANDLE)(("CloseHandle", kernel32))
# (hWnd)
GetWindowDC = WINFUNCTYPE(HDC, HWND)(("GetWindowDC", user32))
# (hdc, x, y, cx, cy, hdcSrc, x1, y1, rop)
BitBlt = WINFUNCTYPE(BOOL, HDC, c_int, c_int, c_int, c_int, HDC, c_int, c_int, DWORD)(("BitBlt", gdi32))
# (hdc, cx, cy)
CreateCompatibleBitmap = WINFUNCTYPE(HANDLE, HDC, c_int, c_int)(("CreateCompatibleBitmap", gdi32))
# (hdc)
CreateCompatibleDC = WINFUNCTYPE(HDC, HDC)(("CreateCompatibleDC", gdi32))
# (hdc, hbm, start, cLines, lpvBits, lpbmi, usage)
GetDIBits = WINFUNCTYPE(c_int, HDC, HANDLE, UINT, UINT, PVOID, PBITMAPINFO, UINT)(("GetDIBits", gdi32))
# (hdc, h)
SelectObject = WINFUNCTYPE(HANDLE, HDC, HANDLE)(("SelectObject", gdi32))
# (hWnd, lpRect)
GetWindowRect = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))(("GetWindowRect", user32))
# (hWnd, lpRect)
GetClientRect = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))(("GetClientRect", user32))
# (hdc)
DeleteDC = WINFUNCTYPE(BOOL, HDC)(("DeleteDC", gdi32))
# (ho)
DeleteObject = WINFUNCTYPE(BOOL, HANDLE)(("DeleteObject", gdi32))
# (hWnd, hDC)
ReleaseDC = WINFUNCTYPE(c_int, HWND, HDC)(("ReleaseDC", user32))
# (hWnd, lpPoint)
ClientToScreen = WINFUNCTYPE(BOOL, HWND, POINTER(POINT))(("ClientToScreen", user32))
# (hwnd, hdcBlt, nFlags)
PrintWindow = WINFUNCTYPE(BOOL, HWND, HDC, UINT)(("PrintWindow", user32))
# (hWnd, bInvert)
FlashWindow = WINFUNCTYPE(BOOL, HWND, BOOL)(("FlashWindow", user32))


### Useful wrappers

def last_error():
    err = get_last_error()
    return "0x%08X: %s" % (err, FormatError(err))


def unicode_buffer(size):
    """
    Create a WSTR buffer of `size` characters.
    """
    return ctypes.create_unicode_buffer(size)


def get_window_rect(title=None):
    """
    Get the coordinates of the window given by title (default: the top window).

    :return: tuple(x1, y1, x2, y2) or None (if window not found)
    """
    if title:
        hwnd = FindWindow(None, title)
        if not hwnd:
            return None
    else:
        hwnd = GetForegroundWindow()
    rect = RECT()
    GetWindowRect(hwnd, byref(rect))
    return (rect.left, rect.top, rect.right, rect.bottom)


def get_window_size(title=None):
    """
    Get the coordinates of the window given by title (default: the top window).

    :return: tuple(width, height) or None (if window not found)
    """
    if title:
        hwnd = FindWindow(None, title)
        if not hwnd:
            return None
    else:
        hwnd = GetForegroundWindow()
    rect = RECT()
    GetClientRect(hwnd, byref(rect))
    return (rect.right, rect.bottom)


def screenshot(hwnd=None, include_titlebar=True, as_rgb=True):
    """
    Take a screenshot of the given window (if None, use the current active window).

    :param hwnd: Window handle (or None).
    :param include_titlebar: Include the window's title bar in the screenshot.
    :param as_rgb: Return the raw bytes as 'RGB' instead of 'BGRX'.
    :return: tuple(width, height, raw_bmp_data)
    """
    if hwnd is None:
        hwnd = GetForegroundWindow()
    dc = GetWindowDC(hwnd)
    if not hwnd:
        raise OSError(f'GetForegroundWindow failed: {last_error()}')
    cdc = CreateCompatibleDC(dc)
    if not cdc:
        raise OSError(f'CreateCompatibleDC failed: {last_error()}')
    rect = RECT()
    fun = GetWindowRect if include_titlebar else GetClientRect
    if not fun(hwnd, byref(rect)):
        raise OSError(f'GetClient/WindowRect failed: {last_error()}')
    left, right, top, bottom = rect.left, rect.right, rect.top, rect.bottom
    width = right - left
    height = bottom - top
    bmp = CreateCompatibleBitmap(dc, width, height)
    if not bmp:
        raise OSError(f'CreateCompatibleBitmap failed: {last_error()}')
    if not SelectObject(cdc, bmp):
        raise OSError(f'SelectObject failed: {last_error()}')
    if not PrintWindow(hwnd, cdc, 0 if include_titlebar else 1):
        raise OSError(f'PrintWindow failed: {last_error()}')
    bmph = BITMAPINFOHEADER(ctypes.sizeof(BITMAPINFOHEADER), width, height, 1, 32, 0)
    buffer = ctypes.create_string_buffer(width * height * 4)
    cnt = GetDIBits(cdc, bmp, 0, height, buffer, cast(byref(bmph), PBITMAPINFO), DIB_RGB_COLORS)
    if not cnt:
        raise OSError(f'GetDIBits failed: {last_error()}')
    DeleteDC(cdc)
    ReleaseDC(hwnd, dc)
    DeleteObject(bmp)
    if as_rgb:
        rgb = ctypes.create_string_buffer(width * height * 3)
        rgb[0::3] = buffer[2::4]
        rgb[1::3] = buffer[1::4]
        rgb[2::3] = buffer[0::4]
        buffer = rgb
    return (width, height, buffer)


