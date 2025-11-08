from PyQt6 import QtWidgets
import json, os

DOC_HTML = """
<h2>SolarEx Plugin Developer Guide</h2>
<p>Plugins live inside <code>solarex/Plugins/</code> or <code>~/.config/SolarEx/plugins/</code>.</p>
<h3>Basic Structure</h3>
<pre>{
  "name": "MyPlugin",
  "version": "1.0",
  "entry": "main.py"
}</pre>
<h3>main.py Template</h3>
<pre>
def init(core):
    print("[MyPlugin] loaded!")
    def on_window(win):
        menu = core.ui_api.add_menu(win, "MyPlugin")
        core.ui_api.add_menu_item(menu, "Say Hi", lambda: core.ui_api.show_message("Hello from MyPlugin!"))
    core.on_window_created(on_window)
</pre>
<h3>UI Helpers</h3>
<ul>
<li><b>core.ui_api.add_button(win, text, callback)</b></li>
<li><b>core.ui_api.add_menu(win, title)</b></li>
<li><b>core.ui_api.add_menu_item(menu, text, callback)</b></li>
<li><b>core.ui_api.show_message(text)</b></li>
<li><b>core.ui_api.open_editor(core, path)</b></li>
</ul>
"""

TEMPLATE_MAIN = """def init(core):
    print("[{name}] Plugin loaded!")
    def on_window(win):
        menu = core.ui_api.add_menu(win, "{name}")
        core.ui_api.add_menu_item(menu, "Say Hi", lambda: core.ui_api.show_message("Hello from {name}!"))
    core.on_window_created(on_window)
"""

def init(core):
    print("[PluginDocs] Ready!")

    def show_docs():
        dlg = QtWidgets.QDialog()
        dlg.setWindowTitle("SolarEx Plugin Docs")
        dlg.resize(800, 600)
        layout = QtWidgets.QVBoxLayout(dlg)
        view = QtWidgets.QTextBrowser()
        view.setHtml(DOC_HTML)
        layout.addWidget(view)
        btn_create = QtWidgets.QPushButton("➕ Create New Plugin")
        layout.addWidget(btn_create)

        def create_plugin():
            name, ok = QtWidgets.QInputDialog.getText(dlg, "New Plugin", "Enter plugin name:")
            if not ok or not name.strip():
                return
            plugin_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", name.strip()))
            os.makedirs(plugin_dir, exist_ok=True)
            manifest = {"name": name.strip(), "version": "1.0", "entry": "main.py"}
            with open(os.path.join(plugin_dir, "plugin.json"), "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2)
            with open(os.path.join(plugin_dir, "main.py"), "w", encoding="utf-8") as f:
                f.write(TEMPLATE_MAIN.format(name=name.strip()))
            core.ui_api.show_message(f"Created new plugin: {name}")
            try:
                from solarex.Plugins.PluginForge.main import forge_open
                forge_open(core, plugin_dir)
            except Exception as e:
                core.ui_api.show_message(f"Could not open editor: {e}")
        btn_create.clicked.connect(create_plugin)
        dlg.exec()

    def on_window(win):
        menu = core.ui_api.add_menu(win, "Help")
        core.ui_api.add_menu_item(menu, "Plugin Documentation", show_docs)

    core.on_window_created(on_window)
