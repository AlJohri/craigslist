import importlib
import argparse

def cdn_url_to_http(url):
	return "http://" + url.lstrip("//")

class ActionNoYes(argparse.Action):
    def __init__(self, opt_name, dest, default=True, required=False, help=None):
        super(ActionNoYes, self).__init__(['--' + opt_name, '--no-' + opt_name], dest, nargs=0, const=None, default=default, required=required, help=help)
    def __call__(self, parser, namespace, values, option_string=None):
        if option_string.starts_with('--no-'):
            setattr(namespace, self.dest, False)
        else:
            setattr(namespace, self.dest, True)

def import_class(s):
    module_string, klass_string = s.rsplit('.', 1)
    module = importlib.import_module(module_string)
    klass = getattr(module, klass_string)
    return klass