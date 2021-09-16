class JimlBaseException(Exception):
    pass


class TemplateSyntaxError(JimlBaseException):
    pass


class TemplateOptionsSyntaxError(TemplateSyntaxError):
    pass


class ConvertError(JimlBaseException):
    pass


class RenderTemplateError(ConvertError):
    pass


class LoadResultsError(ConvertError):
    pass


class JimlConvertError(JimlBaseException):
    pass


class InputSchemaSyntaxError(TemplateSyntaxError):
    pass


class OutputSchemaSyntaxError(TemplateSyntaxError):
    pass


class InputSchemaValidationError(ConvertError):
    pass


class OutputSchemaValidationError(ConvertError):
    pass
