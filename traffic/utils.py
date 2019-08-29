import re
import importlib


__all__ = [
    'camel_case_to_underscore'
]

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def camel_case_to_underscore(name: str):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def import_type(name: str):
    if name.count('.') < 1:
        raise ValueError('Type name should contains dot: "%s", because otherwise I can not split it into module name and type name' % name)

    module_name, type_name = name.rsplit('.', 1)
    module = importlib.import_module(module_name)

    if not hasattr(module, type_name):
        raise ValueError('Can not find type %s in module %s' % (type_name, module))

    return getattr(module, type_name)
