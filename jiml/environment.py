import jinja2
import yaml
import jsonschema
from jinja_vanish import DynAutoEscapeEnvironment, markup_escape_func

from . import exceptions
from .filters import FILTERS, escape
from .common import fix_imports, get_undefined


class JimlTemplate(jinja2.Template):
    def render(self, context):
        try:
            self.input_schema_validator.validate(context)
        except jsonschema.exceptions.ValidationError as e:
            raise exceptions.InputSchemaValidationError(e) from e

        try:
            return super().render(context)
        except jinja2.exceptions.TemplateRuntimeError as e:
            raise exceptions.RenderTemplateError(e) from e

    def convert(self, context):
        try:
            output = yaml.safe_load(self.render(context))
        except yaml.error.MarkedYAMLError as e:
            raise exceptions.LoadResultsError(e) from e

        try:
            self.output_schema_validator.validate(output)
        except jsonschema.exceptions.ValidationError as e:
            raise exceptions.OutputSchemaValidationError(e) from e

        return output

    __call__ = convert


class JimlEnvironment(DynAutoEscapeEnvironment):
    template_class = JimlTemplate

    def __init__(
            self, *args, autoescape=True, undefined=jinja2.StrictUndefined, escape_func=None,
            filters=None, globals=None, **kwargs):
        if autoescape and escape_func is None:
            escape_func = markup_escape_func(escape)
        super().__init__(
            *args,
            autoescape=autoescape,
            undefined=get_undefined(undefined),
            escape_func=escape_func,
            **kwargs
        )

        if filters is None:
            filters = FILTERS
        self.filters.update(fix_imports(filters))

        if globals is not None:
            self.globals.update(fix_imports(globals))
