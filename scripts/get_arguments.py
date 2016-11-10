#!/usr/bin/env python3

import json
import requests
import lxml.html
from collections import namedtuple
from pprint import pprint as pp
from craigslist.search import get_url_base

BaseArgument = namedtuple('Argument', ['dest', 'default', 'action', 'const', 'nargs', 'choices'])
class Argument(BaseArgument):
    def __new__(cls, **kwargs):
        return super().__new__(cls, *[kwargs.get(k) for k in cls._fields])

LOCATION = 'washingtondc'
IGNORE_CHOICES = ['sale_date']

def slugify(s):
    return s.replace('-', '_').replace("'", '').replace(' ', '_').replace('+', 'plus').replace('/', '_')

def get_arguments(section):
    url = get_url_base(LOCATION) + '/' + section
    response = requests.get(url)
    doc = lxml.html.fromstring(response.content)
    arguments = []
    for ultag in doc.cssselect('div.search-options div.searchgroup ul.attr_list'):
        name = ultag.cssselect('li input')[0].get('name')
        if name not in IGNORE_CHOICES:
            choices = tuple(
                (slugify(tag.tail.strip()), tag.get('value'))
                    for tag in ultag.cssselect('li input') if tag.get('value'))
        else:
            choces = None
        argument = Argument(dest=name, nargs='*', choices=choices)
        arguments.append(argument)
    for tag in doc.cssselect(
            'div.search-options div.searchgroup > input, '
            'div.search-options div.searchgroup > label > input, '
            'div.search-options div.searchgroup > ul:not(.js-only):not(.attr_list) > li > label > input',):
        name = tag.get('name')
        if not name: continue
        type_ = tag.get('type')
        value = tag.get('value')
        if type_ == "checkbox":
            argument = Argument(dest=name, action='store_const', const=value)
        else:
            argument = Argument(dest=name)
        arguments.append(argument)
    for selecttag in doc.cssselect('div.search-options div.searchgroup select'):
        name = selecttag.get('name')
        if not name: continue
        default = None
        nargs = None
        if name not in IGNORE_CHOICES:
            choices = tuple(
                ((slugify(tag.text.strip())), tag.get('value'))
                    for tag in selecttag.cssselect('option') if tag.get('value') != '')
            potential_defaults = [value for key, value in choices if "all" in key]
            if len(potential_defaults) == 1:
                default = potential_defaults[0]
                nargs = '?'
        else:
            choices = None
        argument = Argument(dest=name, default=default, choices=choices)
        arguments.append(argument)
    return arguments

if __name__ == '__main__':
    sections = {'ccc', 'hhh', 'sss', 'jjj', 'ggg', 'rrr', 'bbb', 'stp'}
    arguments = [x._asdict() for x in set([argument for section in sections for argument in get_arguments(section)])]
    for argument in arguments:
        argument['choices'] = dict(argument['choices']) if argument.get('choices') else None
    print(json.dumps(arguments, indent=4, sort_keys=True))
