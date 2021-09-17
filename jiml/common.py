from importlib import import_module

from jinja2 import Undefined, StrictUndefined


UNDEFINED = {
    'undefined': Undefined,
    'strictundefined': StrictUndefined,
}


def import_name(path):
    if '.' not in path:
        return import_module(path)

    module_path, name = path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, name)


def fix_import(value):
    return import_name(value) if isinstance(value, str) else value


def fix_imports(imports):
    if isinstance(imports, list):
        imports = {name.rsplit('.', 1)[-1]: name for name in imports}
    return {
        name: fix_import(value)
        for name, value in imports.items()
    }


def get_undefined(value):
    if not isinstance(value, str):
        return value

    obj_value = UNDEFINED.get(value.lower())
    if obj_value is not None:
        return obj_value

    return fix_import(value)
