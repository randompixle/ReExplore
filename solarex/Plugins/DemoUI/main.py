def init(core):
    def on_window(win):
        m = core.ui_api.add_menu(win, "Demo")
        core.ui_api.add_menu_item(m, "Say Hi", lambda: core.ui_api.show_message("Hello from DemoUI!"))
        core.ui_api.add_button(win, "Demo", lambda: core.ui_api.show_message(f"Active renderer: {core.render.active_id}"))
    core.on_window_created(on_window)
