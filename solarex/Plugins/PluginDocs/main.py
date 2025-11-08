from PyQt6 import QtWidgets
DOC = """
<h2>SolarEx Plugin & Renderer Guide</h2>
<p>Plugins live in <code>solarex/Plugins</code> or <code>~/.config/SolarEx/plugins</code>.</p>
<h3>Create a Renderer</h3>
<pre>
# solarex/render/modules/myengine.py
metadata = {"id":"myengine","name":"My Engine","description":"...", "version":"1.0"}
def get_settings_schema(core): return [{"key":"font_size","type":"spin","label":"Font size","default":13}]
def new_view(core, *a, **kw):
    from PyQt6 import QtWidgets, QtCore
    class MyView(QtWidgets.QTextBrowser):
        def load(self, url): self.setSource(QtCore.QUrl(url.toString() if hasattr(url,'toString') else str(url)))
    return MyView()
</pre>
"""
def init(core):
    def on_window(win):
        menu = core.ui_api.add_menu(win, "Help")
        def show():
            d = QtWidgets.QDialog(win); d.setWindowTitle("SolarEx Docs"); d.resize(800,600)
            lay = QtWidgets.QVBoxLayout(d); w = QtWidgets.QTextBrowser(); w.setHtml(DOC); lay.addWidget(w); d.exec()
        core.ui_api.add_menu_item(menu, "Plugin/Renderer Docs", show)
    core.on_window_created(on_window)
