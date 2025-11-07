def init(core):
    print("[Logger] Ready.")
    old_new_view = core.render.new_view
    def hooked_view(*a, **kw):
        view = old_new_view(*a, **kw)
        if hasattr(view, "urlChanged"):
            view.urlChanged.connect(lambda u: print(f"[Logger] {u.toString()}"))
        return view
    core.render.new_view = hooked_view
