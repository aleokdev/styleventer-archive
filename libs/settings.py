from . import modutil
import json

_settings = {}

with open(modutil.absolutePath + "/settings.json", "r") as f:
    _settings = json.loads(f.read())

def get_setting(name, ids_prioritized = None):
    container = _settings.get(name, None)
    if container is None:
        return None

    if ids_prioritized == None:
        return container.get("_G", None)
    else:
        for id in ids_prioritized:
            if str(id) in container:
                return container[str(id)]
        return container.get("_G", None)


def set_local_setting(id, name, val):
    if name not in _settings:
        _settings[name] = {}
    _settings[name][str(id)] = val
    with open(modutil.absolutePath + "/settings.json", "w") as f:
        f.write(json.dumps(_settings))

def set_global_setting(name, val):
    set_local_setting("_G", name, val)

def clear_local_setting(id, name):
    if name not in _settings:
        return
    del _settings[name][str(id)]
    with open(modutil.absolutePath + "/settings.json", "w") as f:
        f.write(json.dumps(_settings))

def clear_global_setting(name):
    clear_local_setting("_G", name)