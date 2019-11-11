import importlib

from traffic import utils
from backends.logger import Logger


# thx to @andgein
class Configurator:
    DEFAULT_SETTINGS_MODULE_NAME = 'settings'

    def __init__(self, settings_module_name=None):
        self._logger = Logger(self)
        self.settings_module_name = self.DEFAULT_SETTINGS_MODULE_NAME if settings_module_name is None else settings_module_name
        self.settings_module = importlib.import_module(self.settings_module_name)

    def _get_settings_variable(self, setting_name, default_value=None, may_missing=False):
        if hasattr(self.settings_module, setting_name):
            return getattr(self.settings_module, setting_name)
        if may_missing:
            return default_value
        raise ValueError('Specify variable %s in settings file (%s)' % (setting_name, self.settings_module_name))

    # TODO: add support for recursive parsing of settings objects
    def _get_settings_object(self, setting_name, may_missing=False, recursive=False):
        object_spec = self._get_settings_variable(setting_name, may_missing=may_missing)
        if object_spec is None:
            return None

        # If you don't need args and kwargs,
        # you can use just 'module.name.class_name' instead of { 'type': 'module.name.class_name' }
        if type(object_spec) is str:
            object_spec = {'type': object_spec}

        if type(object_spec) is not dict:
            raise ValueError('Variable %s in settings file (%s) should be dict or str, not %s' % (
                setting_name,
                self.settings_module_name,
                type(object_spec)
            ))
        
        object_type_name = self._get_dict_value(object_spec, 'type', setting_name)
        object_args = object_spec.get('args', ())
        object_kwargs = object_spec.get('kwargs', {})

        try:
            object_type = utils.import_type(object_type_name)
        except ValueError as e:
            raise ValueError('Can not find type %s for initializing %s: %s' % (
                object_type_name,
                setting_name,
                e
            ))

        self._logger.info('Creating %s with arguments %s and kwarguments %s' % (
            object_type.__name__,
            object_args,
            object_kwargs
        ))
        return object_type(*object_args, **object_kwargs)

    def _get_dict_value(self, dict_object, param, setting_name):
        try:
            return dict_object[param]
        except KeyError:
            raise ValueError('Variable %s in settings file (%s) should has key "%s"' % (
                setting_name,
                self.settings_module_name,
                param
            ))

    def get_flag_format(self):
        return self._get_settings_variable('FLAG_FORMAT')
        
    def get_database(self):
        return self._get_settings_object('DATABASE')
        
    def get_slicer(self):
        return self._get_settings_object('SLICER')

<<<<<<< HEAD
    def get_webapp(self):
        return self._get_settings_object('WEBAPP')
=======
    def get_crawler(self):
        return self._get_settings_object('CRAWLER')
>>>>>>> 49a034757fc7927653f24e1fceb1483d0d847774
