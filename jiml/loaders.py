import re
import pathlib

import jinja2
import yaml

from . import exceptions
from .validation import build_input_validator, build_output_validator
from .environment import JimlEnvironment
from .config import config


def split_template_options(template):
    doc_separator = '\n---\n'
    options = {}
    if re.match(r'^\s*#\s*options\n', template):
        if doc_separator not in template:
            raise exceptions.TemplateOptionsSyntaxError(
                'options specified but not separated from template'
            )

        options_data, template = template.split(doc_separator, 1)
        try:
            options = yaml.safe_load(options_data) or {}
        except yaml.error.MarkedYAMLError as e:
            raise exceptions.TemplateOptionsSyntaxError(e) from e
        assert isinstance(options, dict)
    return template, options


def load_template(template=None, path=None, env=None):
    if template is None:
        template = pathlib.Path(path).read_text()

    template, options = split_template_options(template)
    input_schema = options.pop('input_schema', None)
    output_schema = options.pop('output_schema', None)

    if options:
        env = {**config.get_values(), **options}

    if isinstance(env, dict):
        env = JimlEnvironment(**env)
    elif env is None:
        env = config.get_env()

    try:
        t = env.from_string(template)
    except jinja2.exceptions.TemplateSyntaxError as e:
        raise exceptions.TemplateSyntaxError(e) from e

    t.input_schema_validator = build_input_validator(input_schema)
    t.output_schema_validator = build_output_validator(output_schema)
    return t


def render(template, context, env=None):
    return load_template(template, env=env).render(context)


def convert(template, context, env=None):
    return load_template(template, env=env).convert(context)
