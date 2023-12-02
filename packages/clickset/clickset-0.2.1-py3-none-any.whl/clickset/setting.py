import confuse
import click
import inspect
import typing

from collections import namedtuple
from enum import Enum

from .config import get_config

class ClickParams:
    __slots__ = ('args', 'kwargs')
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

# Create a list of confuse datatypes
# ... Source methods: confuse.Subview.as_*
# ... This is used to create an Enum type for selecting Setting get return values
_confuse_types = [
    name.replace('as_', '').upper()
    for name,value
    in
    inspect.getmembers(
        confuse.Subview,
        lambda obj: hasattr(obj, '__name__') and obj.__name__.startswith('as_')
    )
]

class Setting:
    """An application setting linked to both `confuse` and `click` libraries.

    Settings may be taken from the following sources:

    - in-app defaults (`default` keyword)
    - confuse config file values (at `path` location)
    - command line arguments (defined by `option`)
    - runtime override values (when a new value is set)
    """
    _click_options = []

    Types = Enum('Types', _confuse_types)

    def __init__(
        self,
        path:       str|None,
        /,
        config:     str               = "default",
        *,
        default:    str|int|bool|None = None,
        type:       Types|None        = None,
        get_args:   typing.Any|None   = None,
        option:     ClickParams|None  = None
    ):
        """
        :param path: A dot notation indicating a confuse storage path (e.g. "key1.key2") or None to indicate memory only storage
        :param default: The in-app default value for the setting
        :param config: The name of a global (singletion) configuraiton instance to use for storage
        :param type: A confuse automated template used for getting (`confuse.Subview.as_<type>()`)
        :param get_args: Arguments passed to the confuse `get()` function (or `as_<type>()`)
        :param option: Create a click option for this value
        """
        self._path     = path
        self._name     = None
        self._default  = default
        self._get_args = get_args

        if path is None:
            self._config = None
            self._value  = default
        else:
            self._config = get_config()
            self._value  = self._config

            for key in path.split('.'):
                self._value = self._value[key]

            if default is not None:
                self._value.set_default(default)

        if option is not None:
            option.kwargs['callback'] = self._click_option_set
            click_opt = click.option(*option.args, **option.kwargs)
            self._click_options.append(click_opt)

        if self._path is None:
            self._as = None
        else:
            if type is not None:
                self._as = getattr(self._value, f"as_{type.name.lower()}")
            else:
                self._as = self._value.get

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, objtype = None):
        if obj is None:
            return self
        else:
            if self._path is None:
                return self._value
            else:
                if self._get_args is None:
                    return self._as()
                else:
                    return self._as(self._get_args)

    def __set__(self, obj, value):
        if self._path is None:
            self._value = value
        else:
            self._value.set_memory(value)

    def __delete__(self, obj):
        if self._path is None:
            self._value = self._default
        else:
            self._value.delete_from_memory()

    @classmethod
    def options(cls, func):
        for option in cls._click_options:
            func = option(func)

        return func

    def _click_option_set(self, ctx, param, value):
        if value is not None:
            if self._path is None:
                self._value = value
            elif self._path is not None:
                self._value.set_cli(value)
        return value
