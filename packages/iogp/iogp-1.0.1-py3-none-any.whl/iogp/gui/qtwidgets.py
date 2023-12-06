"""
iogp.gui.qtwidgets: Custom Qt widgets.

Author: Vlad Topan (vtopan/gmail)
"""
from .qt import QTextBrowser, QFontMetrics



class VMessageLog(QTextBrowser):

    def __init__(self, *args, rows=4, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet('QScrollBar:vertical {width: 10px;}')
        self.setPlaceholderText('Log messages')
        self.setReadOnly(1)
        rowheight = QFontMetrics(self.font()).lineSpacing()
        self.setFixedHeight(10 + rows * rowheight)
        self.setOpenExternalLinks(True)
