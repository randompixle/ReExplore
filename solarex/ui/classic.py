from PyQt6 import QtCore, QtWidgets

class ClassicWindow(QtWidgets.QMainWindow):
    def __init__(self, core, start_url: str | None = None):
        super().__init__(); self.core = core
        self.setWindowTitle("SolarEx"); self.resize(1200, 800)
        top = QtWidgets.QWidget(); layout = QtWidgets.QVBoxLayout(top); layout.setContentsMargins(6,6,6,6)
        bar = QtWidgets.QHBoxLayout()
        self.addr = QtWidgets.QLineEdit(); self.addr.setPlaceholderText("Enter URL…")
        self.go = QtWidgets.QPushButton("Go"); self.newtab = QtWidgets.QPushButton("+")
        bar.addWidget(self.addr, 1); bar.addWidget(self.go, 0); bar.addWidget(self.newtab, 0)
        self.tabs = QtWidgets.QTabWidget(); self.tabs.setTabsClosable(True); self.tabs.tabCloseRequested.connect(self.close_tab)
        layout.addLayout(bar); layout.addWidget(self.tabs, 1); self.setCentralWidget(top)
        self.go.clicked.connect(self.load_from_entry)
        self.addr.returnPressed.connect(self.load_from_entry)
        self.newtab.clicked.connect(lambda: self.open_tab("about:blank"))
        self.open_tab(start_url or "https://www.google.com/")

    def open_tab(self, url: str):
        view = self.core.render.new_view()
        idx = self.tabs.addTab(view, "New Tab"); self.tabs.setCurrentIndex(idx)
        if hasattr(view, "titleChanged"):
            view.titleChanged.connect(lambda t, i=idx: self.tabs.setTabText(i, (t[:20] if isinstance(t,str) else str(t)) or "Tab"))
        if hasattr(view, "load"): view.load(QtCore.QUrl(url))
        elif hasattr(view, "setSource"): view.setSource(QtCore.QUrl(url))

    def close_tab(self, index: int):
        w = self.tabs.widget(index); self.tabs.removeTab(index); w.deleteLater()
        if self.tabs.count() == 0: self.open_tab("about:blank")

    def load_from_entry(self):
        url = self.addr.text().strip()
        if not url: return
        if "://" not in url: url = "https://" + url
        w = self.tabs.currentWidget()
        if w and hasattr(w, "load"): w.load(QtCore.QUrl(url))
        elif w and hasattr(w, "setSource"): w.setSource(QtCore.QUrl(url))

    def swap_current_view(self, backend_id: str):
        cur = self.tabs.currentWidget(); url = None
        try:
            if hasattr(cur, "source"): url = cur.source().toString()
            elif hasattr(cur, "url"): url = cur.url().toString()
        except Exception: pass
        if not url: url = self.addr.text() or "https://www.google.com/"
        new_view = self.core.render.new_view()
        idx = self.tabs.currentIndex()
        self.tabs.removeTab(idx); self.tabs.insertTab(idx, new_view, "New Tab"); self.tabs.setCurrentIndex(idx)
        if hasattr(new_view, "load"): new_view.load(QtCore.QUrl(url))

def init(core): core.ui = ClassicWindow
