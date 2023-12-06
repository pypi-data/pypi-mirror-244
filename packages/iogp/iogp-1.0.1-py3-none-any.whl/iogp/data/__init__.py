"""
iogp.data: Various data processing tools.

Author: Vlad Topan (vtopan/gmail)
"""
from .fileid import get_file_type, get_ft_category, get_ft_ext, FT_UNKNOWN, FT_EMPTY, FT_CATEGORY
from .carve import extract_embedded_files
from .ds import AttrDict, Config, dict_to_AttrDict
from .archive import Archive
from .str import ellipsis
