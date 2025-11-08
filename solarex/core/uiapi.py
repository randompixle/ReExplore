from PyQt6 import QtWidgets

class UIAPI:
    def __init__(self, core): self.core = core
    def _tb(self, win):
        tb = win.findChild(QtWidgets.QToolBar, "plugin_toolbar")
        if not tb:
            tb = QtWidgets.QToolBar("Plugin Toolbar", win)
            tb.setObjectName("plugin_toolbar")
            win.addToolBar(tb)
        return tb
    def add_button(self, win, text, cb):
        b = QtWidgets.QPushButton(text); b.clicked.connect(cb); self._tb(win).addWidget(b); return b
    def add_menu(self, win, title):
        mb = win.menuBar() or QtWidgets.QMenuBar(win); win.setMenuBar(mb); return mb.addMenu(title)
    def add_menu_item(self, menu, text, cb):
        act = menu.addAction(text); act.triggered.connect(cb); return act
    def show_message(self, text, title="SolarEx"):
        QtWidgets.QMessageBox.information(None, title, text)
