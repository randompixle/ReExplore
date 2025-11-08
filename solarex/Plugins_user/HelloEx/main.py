from PyQt6 import QtCore
def init(core):
    print("[HelloEx] Registered about:helloex")
    old_view = core.render.new_view
    def patched_view(*a, **kw):
        view = old_view(*a, **kw)
        def intercept(url):
            try: s = url.toString()
            except Exception: return
            if s == "about:helloex":
                html = "<html><body><h1>SolarEx says hi!</h1><p>Custom plugin page.</p></body></html>"
                if hasattr(view, "setHtml"): view.setHtml(html, QtCore.QUrl("about:blank"))
        if hasattr(view, "urlChanged"):
            view.urlChanged.connect(intercept)
        return view
    core.render.new_view = patched_view
