"""
iogp.data.str: Strings.

Author: Vlad Topan (vtopan/gmail)
"""

def ellipsis(s, size):
    """
    Trim a string to a maximum size, add an ellipsis ("[...]") if trimmed.
    """
    if len(s) > size:
        s = s[:size - 5] + '[...]'
    return s
