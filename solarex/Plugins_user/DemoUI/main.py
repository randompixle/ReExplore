def init(core):
    print("[DemoUI] Plugin active.")
    def on_window(win):
        menu = core.ui_api.add_menu(win, "Demo")
        core.ui_api.add_menu_item(menu, "Say Hello", lambda: core.ui_api.show_message("Hello from DemoUI!"))
        core.ui_api.add_button(win, "Demo Button", lambda: core.ui_api.show_message("Button pressed!"))
    core.on_window_created(on_window)
