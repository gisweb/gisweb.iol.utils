

def _removePersistentUtility(portal):
    pass

def uninstall(portal,reinstall=False):
    if not reinstall:
        _removePersistentUtility(portal)
