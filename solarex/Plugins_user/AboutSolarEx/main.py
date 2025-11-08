def init(core):
    def on_window(win):
        menu = core.ui_api.add_menu(win, "Help")
        core.ui_api.add_menu_item(menu, "About SolarEx", lambda: core.ui_api.show_message(
            "SolarEx Browser\nVersion 1.0 Dev Edition\nBuilt on PyQt6\n(c) 2025 Solar Labs"
        ))
    core.on_window_created(on_window)
