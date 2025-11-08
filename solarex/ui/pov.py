from PyQt6 import QtCore, QtWidgets, QtGui
class POVWindow(QtWidgets.QMainWindow):
    def __init__(self, core, start_url: str):
        super().__init__(); self.core = core; self.setWindowTitle("SolarEx POV"); self.resize(1200,800)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint, True)
        view = self.core.render.new_view(); self.setCentralWidget(view)
        if hasattr(view,"load"): view.load(QtCore.QUrl(start_url))
        QtWidgets.QShortcut(QtGui.QKeySequence("Escape"), self, activated=self.close)
def init(core): core.ui = POVWindow
