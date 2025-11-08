from PyQt6 import QtWidgets
def init(core):
    def on_win(win):
        menubar = win.menuBar() if hasattr(win, "menuBar") else None
        if not menubar: return
        menu = menubar.addMenu("Settings")
        rmenu = menu.addMenu("Renderer")
        for be in core.render.list_backends():
            act = rmenu.addAction(f"{be.name}")
            def make_switch(bid):
                def _():
                    core.render.set_active(bid)
                    core.settings.set("renderer", bid)
                    if hasattr(win, "swap_current_view"): win.swap_current_view(bid)
                return _
            act.triggered.connect(make_switch(be.id))
        rmenu.addSeparator()
        act_opts = rmenu.addAction("Renderer Options…")
        def open_opts():
            dlg = QtWidgets.QDialog(win); dlg.setWindowTitle("Renderer Options"); lay = QtWidgets.QVBoxLayout(dlg)
            be = core.render.backends.get(core.render.active_id); schema = be.settings_schema(core) if be else []
            edits = {}
            for item in schema:
                row = QtWidgets.QHBoxLayout(); label = QtWidgets.QLabel(item.get("label", item["key"])); row.addWidget(label)
                key = item["key"]; t = item["type"]; ns = f"renderer.{core.render.active_id}"
                if t == "checkbox":
                    w = QtWidgets.QCheckBox(); w.setChecked(bool(core.settings.get_ns(ns,key,item.get('default'))))
                elif t == "spin":
                    w = QtWidgets.QSpinBox(); w.setRange(item.get('min',0), item.get('max',100)); w.setSingleStep(item.get('step',1)); w.setValue(int(core.settings.get_ns(ns,key,item.get('default',0))))
                else:
                    w = QtWidgets.QLineEdit(str(core.settings.get_ns(ns,key,item.get('default',''))))
                row.addWidget(w, 1); lay.addLayout(row); edits[key]=(t,w,ns)
            btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Save | QtWidgets.QDialogButtonBox.StandardButton.Cancel); lay.addWidget(btns)
            def save():
                for key,(t,w,ns) in edits.items():
                    if t=="checkbox": core.settings.set_ns(ns,key,bool(w.isChecked()))
                    elif t=="spin": core.settings.set_ns(ns,key,int(w.value()))
                    else: core.settings.set_ns(ns,key,w.text())
                dlg.accept()
            btns.accepted.connect(save); btns.rejected.connect(dlg.reject); dlg.exec()
        act_opts.triggered.connect(open_opts)
    core.on_window_created(on_win)
