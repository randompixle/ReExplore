from PyQt6 import QtWidgets

class UIAPI:
    def __init__(self, core):
        self.core = core

    def _ensure_toolbar(self, win):
        tb = win.findChild(QtWidgets.QToolBar, "plugin_toolbar")
        if not tb:
            tb = QtWidgets.QToolBar("Plugin Toolbar", win)
            tb.setObjectName("plugin_toolbar")
            win.addToolBar(tb)
        return tb

    def add_button(self, win, text, callback):
        tb = self._ensure_toolbar(win)
        btn = QtWidgets.QPushButton(text)
        btn.clicked.connect(callback)
        tb.addWidget(btn)
        return btn

    def add_menu(self, win, title):
        mb = win.menuBar() or QtWidgets.QMenuBar(win)
        win.setMenuBar(mb)
        return mb.addMenu(title)

    def add_menu_item(self, menu, text, callback):
        act = menu.addAction(text)
        act.triggered.connect(callback)
        return act

    def show_message(self, text, title="SolarEx"):
        QtWidgets.QMessageBox.information(None, title, text)

    def open_editor(self, core, path: str):
        try:
            from solarex.Plugins.PluginForge.main import forge_open
            forge_open(core, path)
        except Exception as e:
            self.show_message(f"PluginForge not available: {e}")
