from PyQt6 import QtWidgets, QtCore
metadata = {"id":"minimal","name":"Minimal (no JS)","description":"QTextBrowser fallback","version":"1.1"}
def get_settings_schema(core): return []
class MinView(QtWidgets.QTextBrowser):
    def load(self, url):
        if hasattr(url,"toString"): url = url.toString()
        self.setSource(QtCore.QUrl(url))
def new_view(core, *a, **kw): return MinView()
