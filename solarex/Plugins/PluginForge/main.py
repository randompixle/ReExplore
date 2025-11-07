from PyQt6 import QtWidgets, QtGui, QtCore
import os

def forge_open(core, plugin_dir: str):
    if not os.path.isdir(plugin_dir):
        core.ui_api.show_message(f"Not a directory: {plugin_dir}")
        return
    main_py = os.path.join(plugin_dir, "main.py")
    if not os.path.exists(main_py):
        open(main_py, "a").close()

    dlg = QtWidgets.QDialog()
    dlg.setWindowTitle(f"PluginForge – {os.path.basename(plugin_dir)}")
    dlg.resize(900, 650)
    layout = QtWidgets.QVBoxLayout(dlg)

    # Header
    header = QtWidgets.QHBoxLayout()
    path_label = QtWidgets.QLabel(main_py)
    header.addWidget(path_label)
    layout.addLayout(header)

    # Editor
    edit = QtWidgets.QPlainTextEdit()
    try:
        with open(main_py, "r", encoding="utf-8") as f:
            edit.setPlainText(f.read())
    except Exception as e:
        edit.setPlainText(f"# Error opening file: {e}\n")
    layout.addWidget(edit, 1)

    # Buttons
    btns = QtWidgets.QHBoxLayout()
    btn_save = QtWidgets.QPushButton("Save")
    btn_reload = QtWidgets.QPushButton("Reload Plugin")
    btn_close = QtWidgets.QPushButton("Close")
    btns.addWidget(btn_save)
    btns.addWidget(btn_reload)
    btns.addStretch(1)
    btns.addWidget(btn_close)
    layout.addLayout(btns)

    def save():
        try:
            with open(main_py, "w", encoding="utf-8") as f:
                f.write(edit.toPlainText())
            core.ui_api.show_message("Saved.")
        except Exception as e:
            core.ui_api.show_message(f"Save failed: {e}")

    def reload_plug():
        save()
        # guess name from plugin.json
        manifest_path = os.path.join(plugin_dir, "plugin.json")
        name = None
        try:
            import json
            with open(manifest_path, "r", encoding="utf-8") as f:
                name = json.load(f).get("name")
        except Exception as e:
            core.ui_api.show_message(f"Read manifest failed: {e}")
            return
        try:
            core.plugin_manager.reload(core, name)
            core.ui_api.show_message(f"Reloaded plugin: {name}")
        except Exception as e:
            core.ui_api.show_message(f"Reload failed: {e}")

    btn_save.clicked.connect(save)
    btn_reload.clicked.connect(reload_plug)
    btn_close.clicked.connect(dlg.close)

    dlg.exec()
