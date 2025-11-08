from PyQt6 import QtWebEngineWidgets, QtWebEngineCore

metadata = {
    "id": "qtweb",
    "name": "QtWebEngine (full)",
    "description": "Chromium-based WebEngine with JS/CSS",
    "version": "1.2.1",
}


def get_settings_schema(core):
    return [
        {"key": "cookies_enabled", "type": "checkbox", "label": "Enable persistent cookies", "default": True},
        {"key": "http_cache", "type": "checkbox", "label": "Enable HTTP disk cache", "default": True},
    ]


def new_view(core, *a, **kw):
    """Create a QWebEngineView using the correct API for all PyQt6 versions."""
    # Make sure the profile exists
    if core.profile.incognito:
        profile = QtWebEngineCore.QWebEngineProfile()
    else:
        profile = QtWebEngineCore.QWebEngineProfile(core.profile.profile_name)
        profile.setPersistentStoragePath(core.profile.storage_path)
        profile.setCachePath(core.profile.cache_path)
        profile.setPersistentCookiesPolicy(
            QtWebEngineCore.QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies
        )

    # Read settings
    cookies_on = core.settings.get_ns("renderer.qtweb", "cookies_enabled", True)
    cache_on = core.settings.get_ns("renderer.qtweb", "http_cache", True)

    if not cookies_on:
        profile.setPersistentCookiesPolicy(
            QtWebEngineCore.QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies
        )
    profile.setHttpCacheType(
        QtWebEngineCore.QWebEngineProfile.HttpCacheType.DiskHttpCache
        if cache_on
        else QtWebEngineCore.QWebEngineProfile.HttpCacheType.MemoryHttpCache
    )

    # ✅ Compatibility: QWebEnginePage moved from QtWebEngineWidgets → QtWebEngineCore
    try:
        page = QtWebEngineCore.QWebEnginePage(profile)
    except AttributeError:
        page = QtWebEngineWidgets.QWebEnginePage(profile)

    view = QtWebEngineWidgets.QWebEngineView()
    view.setPage(page)
    return view
