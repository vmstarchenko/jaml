import json

import jinja2
import yaml


def yaml_escape(obj):
    if isinstance(obj, jinja2.Undefined):
        if isinstance(obj, jinja2.StrictUndefined):
            raise jinja2.exceptions.UndefinedError(
                f"Can't serialize StrictUndefined var '{obj._undefined_name}'"
            )
        return ''

    res = yaml.dump(
        obj,
        width=float("inf"),
        default_flow_style=True,
        default_style='"',
    ).strip('\n')

    if '\n' in res:
        raise ValueError('escaped value contains newline symbol for object {}'.format(obj))

    return res


def _qstr(inp):
    if inp is None:
        inp = ''
    return json.dumps(str(inp))


def qstr(inp):
    return jinja2.Markup(_qstr(inp))


def str_(inp):
    return jinja2.Markup(_qstr(inp)[1:-1])


def json_dumps(inp):
    return jinja2.Markup(json.dumps(inp, ensure_ascii=False))


JIML_FILTERS = {
    'qstr': qstr,
    'str': str_,
    'json.dumps': json_dumps,
    'yaml.dumps': yaml_escape,
    'e': yaml_escape,
    'escape': yaml_escape,
}
