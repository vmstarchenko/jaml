import json

import jinja2
import yaml
from jinja_vanish import DynAutoEscapeEnvironment, markup_escape_func


__all__ = (
    'qstr', 'str', 'json_dumps', 'FILTERS', 'Environment', 'convert',
)


def dump(obj):
    return yaml.dump(
        obj,
        width=float("inf"),
        default_flow_style=True,
        default_style='"',
    ).strip('\n')


def qstr(inp):
    if inp is None:
        inp = ''
    return json.dumps(str(inp))

def qstr_(inp):
    return jinja2.Markup(qstr(inp))


def str_(inp):
    return jinja2.Markup(qstr(inp)[1:-1])


def json_dumps(inp):
    return jinja2.Markup(json.dumps(inp, ensure_ascii=False))


JIML_FILTERS = {
    'qstr': qstr_,
    'str': str_,
    'json.dumps': json_dumps,
    'e': dump,
    'escape': dump,
}



class Environment(DynAutoEscapeEnvironment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters.update(JIML_FILTERS)


_env = Environment(autoescape=True, escape_func=markup_escape_func(dump))


def render(template, context):
    return _env.from_string(template).render(context)


def convert(template, context):
    return yaml.safe_load(render(template, context))
