import importlib

def cdn_url_to_http(url):
	return "http://" + url.lstrip("//")

# TODO: rename to work with methods too
def import_class(s):
    try:
        module_string, klass_string = s.rsplit('.', 1)
    except ValueError:
        raise ValueError('could not parse {}. provide the full path to class'.format(s))
    module = importlib.import_module(module_string)
    klass = getattr(module, klass_string)
    return klass

def get_only_first_or_none(lst):
    if len(lst) > 1: raise ValueError("too many values")
    return lst[0] if len(lst) else None

from blessings import Terminal
t = Terminal()