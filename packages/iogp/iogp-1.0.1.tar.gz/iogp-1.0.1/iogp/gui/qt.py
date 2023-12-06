"""
iogp.gui.qt: GUI wrappers and helper functions for PySide6 (Qt5).

Author: Vlad Topan (vtopan/gmail)
"""

from PySide6.QtCore import (SIGNAL, QByteArray, QCoreApplication, QDate, QDateTime,  # noqa: F401
        QEvent, QSortFilterProxyModel, Qt, QThread, Signal, Slot)
from PySide6.QtGui import (QBrush, QClipboard, QColor, QCursor, QDesktopServices,  # noqa: F401
        QFont, QFontMetrics, QIcon, QIntValidator, QKeySequence, QPalette, QPixmap, QShortcut,
        QStandardItemModel, QTextCursor)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,  # noqa: F401
        QCompleter, QDateEdit, QDateTimeEdit, QFrame, QGridLayout, QHBoxLayout, QHeaderView, QLabel,
        QLayout, QLineEdit, QListWidget, QMainWindow, QMessageBox, QPushButton, QStatusBar,
        QTableView, QTableWidget, QTableWidgetItem, QTabWidget, QTextBrowser, QTextEdit,
        QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)
from logging import error, warn


class WidgetManager:
    """
    Widget manager for PySide6/Qt5.
    """

    def __init__(self, parent, widgets=None):
        self.widgets = None
        self.parent = parent
        if widgets:
            self.load_widgets(widgets)

    def load_widgets(self, widgets):
        """
        Converts recursive structures of lists, dicts and GUI widgets to a proper PySide6 layout.

        A list is converted to a QVBoxLayout, a dict to a QHBoxLayout, everything else is presumed
        to be a widget and simply added to the current layout. The keys in each dict are mapped to
        the corresponding widgets in the output `widget_map` dict.

        Known keywords:
        - '!tab' converts a dict to a QTabWidget
        - '!vertical' converts a dict to a QVBoxLayout instead of a QHBoxLayout
        - '!horizontal' converts a list to a QHBoxLayout instead of a QVBoxLayout
        - '!border' creates a border (QFrame) around the layout (the value can be CSS styling)
        - '!stretch' sets stretching rules (e.g. '!stretch': (0, 2) sets the stretch property of
            widget 0 to 2; can be a list of tuples to set the stretch for multiple widgets

        :return: The top-level layout.
        """
        self.layout = None
        self.widget_map = {}
        self.tabs = []
        if isinstance(widgets, str):
            # todo parse as JSON
            raise NotImplementedError(':(')
        if isinstance(widgets, {}):
            self.layout, self.widgets = self.create_layouts(widgets)
        else:
            raise ValueError(
                    f'Cannot process {widgets} of type {type(widgets)}, should be dict or JSON str!'
            )

    def create_layouts(self, widgets, name=None):
        """
        Parse the nested widget structure and generate the layout tree.
        """

        def _handle_directive(name, value=None):
            nonlocal layout
            if name.startswith('!stretch'):
                if not isinstance(value, list):
                    value = [value]
                for e in value:
                    layout.setStretch(*e)
            elif name == '!border':
                frame = QFrame()
                layout = QHBoxLayout()
                layout.addWidget(frame)
                frame.setLayout(layout)
                frame.setFrameStyle(QFrame.StyledPanel)
                if value and isinstance(value, str):
                    frame.setStyleSheet(value)
            elif name in ('!horizontal', '!vertical', '!tab'):
                pass
            else:
                raise ValueError(f'Unknown directive {name}!')

        if not isinstance(widgets, (list, dict)):
            raise ValueError('The toplevel node must be a list or a dict!')
        layout = QVBoxLayout() if ((isinstance(widgets, list) and '!horizontal' not in widgets)
                or '!vertical' in widgets) else QHBoxLayout()
        tab = None
        if '!tab' in widgets:
            tab = QTabWidget()
            self.tabs.append(tab)
            self.widget_map[name] = tab
            layout.addWidget(tab)
        if tab and not isinstance(widgets, {}):
            raise ValueError('Tab widgets must be dicts!')
        for widget in widgets:
            w_name = None
            add_layout_fun = layout.addLayout
            if isinstance(widgets, dict):
                w_name, widget = widget, widgets[widget]
            # handle directives
            if isinstance(w_name, str) and w_name[0] == '!':
                _handle_directive(w_name, widget)
                continue
            elif isinstance(widget, str):
                _handle_directive(widget)
                continue
            # add this widget(s) or layout
            if tab:
                tab_widget = QWidget()
                tab.addTab(tab_widget, w_name)
                add_layout_fun = tab_widget.setLayout
            if isinstance(widget, (list, dict)):
                widget = self.create_layouts(widget, name=w_name)
                add_layout_fun(widget)
            elif isinstance(widget, QLayout):
                add_layout_fun(widget)
            else:
                if tab:
                    tab_layout = QVBoxLayout()
                    tab_widget.setLayout(tab_layout)
                    tab_layout.addWidget(widget)
                else:
                    layout.addWidget(widget)
            if w_name:
                self.widget_map[w_name] = widget
        return layout

    def connect_buttons(self):
        """
        Connect self.parent.clicked_<widget_name> handlers to .clicked events.
        """
        for k, v in self.wm.widget_map.items():
            if isinstance(v, QPushButton):
                method = 'clicked_' + k
                if hasattr(self, method):
                    self[k].clicked.connect(getattr(self, method))
                else:
                    warn(f'Missing implementation for {method}!\n')

    def __getattr__(self, name):
        return self.widget_map[name]

    def __getitem__(self, key):
        return self.widget_map[key]
