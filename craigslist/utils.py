import importlib, re

def cdn_url_to_http(url):
    if url.startswith("//"):
        return "http://" + url.lstrip("//")
    return url

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

def convert_dict_to_camel_case(d): # pragma: no cover
    from boltons.iterutils import remap

    re1 = re.compile(r'(.)([A-Z][a-z]+)')
    re2 = re.compile(r'([a-z0-9])([A-Z])')

    def convert_str_to_camel_case(s):
        s1 = re.sub(re1, r'\1_\2', s)
        return re.sub(re2, r'\1_\2', s1).lower()

    def visit(path, key, value):
        new_key = convert_str_to_camel_case(key) if isinstance(key, str) else key
        return new_key, value

    return remap(d, visit=visit)

from blessings import Terminal
t = Terminal()