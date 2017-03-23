# -*- coding: utf-8 -*-
"""xMatters Base Objects

Starting point for most objects used throughout the xMatters API.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from enum import Enum
import json
import logging
import types

LOGGER = logging.getLogger('xlogger')

class XmattersList(list):
    """xMatters specific list representation

    Defines a Python list that also adds an attribute to hold the
    XmattersBase subclass that represents the type of list element.

    Attributes:
        base_class (:obj:`class`): Type of XmatterBase subclass held in list
    """

    base_class = None

    @property
    def json(self) -> str:
        """Returns the JSON representation of the current object"""
        return json.dumps(self)

    def __init__(self, *args):
        """Creates and initializes an instance.

        Args:
            *args
                See https://docs.python.org/3/library/stdtypes.html#list
                Optional iterable

        Returns:
            list: An initialized and possibly empty list

        Raises:
            TypeError: base_class is not a sub-class of XmattersBase
        """
        bcname = self.base_class.__name__ if self.base_class else "None"
        LOGGER.debug(
            "XmattersList.__new__ - Class = %s, self.base_class = %s.",
            self.__class__.__name__, bcname)
        super().__init__(*args)
        if not issubclass(self.base_class, XmattersBase):
            raise TypeError((
                "Initializing class XmattersList. base_class is a %s, "
                "and not a subclass of XmattersBase")%(
                bcname))

    @classmethod
    def from_json_obj(cls, json_self):
        """Creates and initializes an XmattersList subclass.

        Args:
            cls (class): XmattersList subclass to instantiate.
            json_self (:list: of :obj:`JSON`): JSON string containing an array
                of instances of a JSON representation of cls.

        Returns:
            object: An instance of cls populated with json_self.
        """
        bcname = cls.base_class.__name__ if cls.base_class else "None"
        LOGGER.debug(
            ("XmattersList.from_json_obj - cls = %s, %s.base_class = %s, "
             "json_self = %s."),
            cls.__name__, cls.__name__, bcname, json_self)
        bc_default = [
            cls.base_class(jobj) #pylint:disable=not-callable
            for jobj in json_self]
        new_obj = cls(bc_default)
        LOGGER.debug(
            "XmattersList.from_json_obj - Created new objects: %s",
            str(new_obj))
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Creates and initializes an XmattersList subclass.

        Args:
            cls (class): XmattersList subclass to instantiate.
            json_self (:str:`JSON`): JSON string containing an array
                of instances of a JSON representation of base_class

        Returns:
            object: An instance of cls populated with json_self.
        """
        bcname = cls.base_class.__name__ if cls.base_class else "None"
        LOGGER.debug(
            ("XmattersList.from_json_str - cls = %s, %s.base_class = %s, "
             "json_self = %s."),
            cls.__name__, cls.__name__, bcname, json_self)
        objs = json.loads(json_self)
        LOGGER.debug(
            "XmattersList.from_json_str - created objs: %s", str(objs))
        return cls.from_json_obj(objs)

class XmattersJSONEncoder(json.JSONEncoder):
    """xMatters object JSON encoder

    Used to create a data element convertable to JSON
    """
    def default(self, obj):
        LOGGER.debug(
            "XmattersJSONEncoder.default: type of obj: %s",
            type(obj).__name__)
        if issubclass(type(obj), Enum):
            LOGGER.debug(
                "XmattersJSONEncoder.default: type of obj: %s, %s",
                type(obj).__name__, obj.value)
            serial = obj.value
            return serial

        if issubclass(type(obj), XmattersBase):
            LOGGER.debug(
                "XmattersJSONEncoder.default: %s is an XmattersBase subclass",
                type(obj).__name__)
            LOGGER.debug(
                "XmattersJSONEncoder.default: contents: %s",
                str(obj.__dict__))
            LOGGER.debug(
                "XmattersJSONEncoder.default: obj.jsondict: %s",
                str(obj.jsondict))
            serial = dict(
                (k, getattr(obj, v)) for k, v in obj.jsondict.items() if getattr(obj,v) is not None)
            LOGGER.debug(
                "XmattersJSONEncoder.default: contents: %s",
                str(serial))
            return serial

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

class XmattersBase(object):
    """xMatters object representation

    Used to create a Python object that represents the JSON oriented
    payloads defined in the xMatters API.
    This base class provides helper and utility methods to generalize
    the creation of such objects by simply defining the attribute names,
    JSON field names, associated types, and whether the atribute is required.

    Args:
        *args
            Variable length argument list.
            Must follow the order of types.
        **kwargs
            Arbitrary keyword arguments.
            Must follow the appropriate type for the named arg

    Attributes:
        argdict (:obj:`dict` of :obj:`str`): Attribute names indexed by
            argument names
        reqargs (:obj:`dict` of :obj:`bool`): Required flag (bool) indexed by
            argument names
        attrdict (:obj:`dict` of :obj:`str`): JSON names indexed by
            attribute names
        typedict (:obj:`dict` of :obj:`class`): Argument type indexed by
            attribute names
        jsondict(:obj:`dict` of :obj:`str`): Attrib names indexed by JSON names
    """

    @property
    def json(self) -> str:
        """Returns the JSON representation of the current object"""
        #d = dict((v, getattr(self, k)) for k, v in self.jsondict.items())
        return json.dumps(self, separators=(',', ':'), cls=XmattersJSONEncoder)

    @property
    def argdict(self) -> dict:
        """:obj:`dict` of :obj:`str`: Argument to member name dictionary"""
        return getattr(self, '__arg_dict')

    @property
    def reqargs(self) -> dict:
        """:obj:`dict` of :obj:`bool`: Argument to required flag dictionary"""
        return getattr(self, '__req_args_dict')

    @property
    def attrdict(self) -> dict:
        """:obj:`dict` of :obj:`str`: Attribute to argument name dictionary"""
        return getattr(self, '__attr_dict')

    @property
    def typedict(self) -> dict:
        """:obj:`dict` of :obj:`class` Attribute to argument type dictionary"""
        return getattr(self,'__type_dict')

    @property
    def jsondict(self) -> dict:
        """:obj:`dict` of :obj:`str`: Attribute to JSON name dictionary"""
        return getattr(self, '__json_dict')

    def _setattr(self, name, value):
        """Convert dictionaries to their class instance based on typedict"""
        if issubclass(self.typedict[name], Enum):
            new_type = self.typedict[name]
            value = new_type(value)
            LOGGER.debug(
                ("XmattersBase._setattr - value is subclass of Enum. "
                 "new_type: %s, value(%s): %s"),
                new_type.__name__, value.__class__.__name__, str(value))
        elif issubclass(self.typedict[name], XmattersList):
            new_type = self.typedict[name]
            value = new_type.from_json_obj(value)
            LOGGER.debug(
                ("XmattersBase._setattr - value is subclass of XmattersList. "
                 "new_type: %s, value(%s): %s"),
                new_type.__name__, value.__class__.__name__, str(value))
        elif isinstance(value, dict):
            if not isinstance(self.typedict[name], dict):
                new_type = self.typedict[name]
                value = new_type(value)
                LOGGER.debug(
                    ("XmattersBase._setattr - value is instance of dict. "
                     "new_type: %s, value(%s): %s"),
                    new_type.__name__, value.__class__.__name__, str(value))
            else:
                LOGGER.debug(
                    ("XmattersBase._setattr - value and target type of dict. "
                     "value(%s): %s"),
                    value.__class__.__name__, str(value))
        else:
            LOGGER.debug('XmattersBase._setattr: value IS NOT instance of dict')
        setattr(self, name, value)

    def _process_arg_names(self, names:list): #pylint:disable=no-self-use
        """dict, dict: Builds name and req'd field dicts from tagged names"""
        arg_names = []
        req_args = []
        for arg in names:
            arg_names.append(arg if arg[0] != '*' else arg[1:])
            req_args.append(arg[0] != '*')
        return arg_names, req_args

    def _build_arg_dicts(self, arg_names, req_args, attr_names):
        """Creates the internal member lookup dictionaries"""
        setattr(self, '__arg_dict', dict(zip(arg_names, attr_names)))
        setattr(self, '__req_args_dict', dict(zip(arg_names, req_args)))

    def _build_attr_dicts(self, attr_names, attr_types, json_names):
        """Creates the internal member lookup dictionaries"""
        setattr(self, '__attr_dict', dict(zip(attr_names, json_names)))
        setattr(self, '__type_dict', dict(zip(attr_names, attr_types)))
        setattr(self, '__json_dict', dict(zip(json_names, attr_names)))

    def __debug_input_args(self, args): #pylint:disable=no-self-use
        if args:
            LOGGER.debug(
                "XmattersBase.__debug_input_args type(args): %s = %s",
                str(type(args)), str(args))
            LOGGER.debug(
                "XmattersBase.__debug_input_args args(%d): %s:%s",
                len(args) if args is not None else 0,
                str(type(args[0]) if args is not None else 'None'),
                str(args[0]) if args is not None else 'None')

    def _is_proper_type(self, attr, value) -> bool:
        """bool: True if value is the proper type expected by attr"""
        attr_type = self.typedict[attr]
        value_type = type(value)
        is_xtype = issubclass(attr_type, XmattersBase) and value_type is dict
        is_enum = issubclass(attr_type, Enum) and value_type is str
        is_list = issubclass(attr_type, list) and value_type is list
        return is_xtype or is_enum or is_list or value_type is attr_type

    def __process_dictionary_args(self, json_names, args):
        for dictionary in args:
            for key in dictionary:
                if key in json_names:
                    if not self._is_proper_type(self.jsondict[key],
                                                dictionary[key]):
                        LOGGER.debug(
                            ("XmattersBase.__process_dictionary_args TypeError:"
                             " Initializing class %s. JSON Attribute %s "
                             "should be a %s, but a %s was found"),
                            self.__class__.__name__, key,
                            str(self.typedict[self.jsondict[key]]),
                            str(type(dictionary[key])))
                        raise TypeError((
                            "Initializing class %s. JSON Attribute %s "
                            "should be a %s, but a %s was found")%(
                            self.__class__.__name__, key,
                            str(self.typedict[self.jsondict[key]]),
                            str(type(dictionary[key]))))
                    LOGGER.debug(
                        ("XmattersBase.__process_dictionary_args Using args as"
                         " dict to set %s from %s to %s"),
                        self.jsondict[key], key, dictionary[key])
                    self._setattr(self.jsondict[key], dictionary[key])

    def __process_positional_args(self, attr_names, attr_types, args):
        key = 0
        for value in args:
            if not isinstance(value,attr_types[key]):
                LOGGER.debug(("XmattersBase.__process_positional_args TypeError"
                    ": Initializing class %s. Attribute at position %d (%s) "
                    "should be a %s, but a %s was found"),
                    self.__class__.__name__, key, attr_names[key],
                    str(attr_types[key]), str(type(value)))
                raise TypeError((
                    "Initializing class %s. Attribute at position %d (%s) "
                    "should be a %s, but a %s was found")%(
                    self.__class__.__name__, key, attr_names[key],
                    str(attr_types[key]), str(type(value))))
            LOGGER.debug(
                ("XmattersBase.__process_positional_args Using positional arg "
                 "%d to set %s to %s"),
                key, attr_names[key], str(value))
            self._setattr(attr_names[key], value)
            key += 1

    def __process_keyword_args(self, arg_names, kwargs):
        for key in kwargs:
            if key in arg_names:
                attr_name = self.argdict[key]
                if not isinstance(kwargs[key], self.typedict[attr_name]):
                    LOGGER.debug(("XmattersBase.__process_keyword_args - "
                        "TypeError: Initializing class %s. Keyword argument "
                        "'%s' should be a %s, but a %s was found"),
                        self.__class__.__name__, key,
                        str(self.typedict[attr_name]),
                        str(type(kwargs[key])))
                    raise TypeError((
                        "Initializing class %s. Keyword argument '%s' "
                        "should be a %s, but a %s was found")%(
                        self.__class__.__name__, key,
                        str(self.typedict[attr_name]),
                        str(type(kwargs[key]))))
                LOGGER.debug(
                    ("XmattersBase.__process_keyword_args - "
                     "Using kwargs to set %s from %s to %s"),
                    self.argdict[key], key, kwargs[key])
                self._setattr(self.argdict[key], kwargs[key])

    def __confirm_required_args(self, arg_names):
        """Final check for required arguments"""
        missing_args = []
        for key in arg_names:
            if self.reqargs[key]:
                if getattr(self, self.argdict[key]) is None:
                    missing_args.append(self.argdict[key])
        if missing_args:
            LOGGER.debug(
                ("XmattersBase.__confirm_required_args - "
                 "TypeError: Initializing class %s. Missing arguments: %s."),
                self.__class__.__name__, ",".join(missing_args))
            raise TypeError("Initializing class %s. Missing arguments: %s."%(
                self.__class__.__name__, ",".join(missing_args)))

    def __init__(self, *args, **kwargs):
        """Creates and initializes an instance.

        Args:
            *args
                Variable length argument list.
                Must follow the order of types.
            **kwargs
                Arbitrary keyword arguments.
                Must follow the appropriate type for the named arg

        Returns:
            object: An initialized instance

        Raises:
            TypeError: The type of an argument value is not correct, or
                a required argument is missing
        """
        cls = self.__class__
        clsname = cls.__name__
        LOGGER.debug('XmattersBase.__init__ - self.__class__.__name__: %s',
            clsname)
        # Get arguments and attribute information from subclass
        arg_names = cls._arg_names #pylint:disable=no-member, protected-access
        attr_names = cls._attr_names #pylint:disable=no-member, protected-access
        attr_types = cls._attr_types #pylint:disable=no-member, protected-access
        json_names = cls._json_names #pylint:disable=no-member, protected-access
        # Fixup argument names and build required arguments array
        arg_names, req_args = self._process_arg_names(arg_names)
        LOGGER.debug(
            ('XmattersBase.__init__ - \n\targ_names: %s\n\tattr_names: %s'
             '\n\tattr_types: %s\n\tjson_names: %s'),
            str(arg_names), str(attr_names), str(attr_types), str(json_names))
        # Create and initialize attributes
        for name in attr_names:
            setattr(self, name, None)
        # Create lookup dictionaries
        self._build_arg_dicts(arg_names, req_args, attr_names)
        self._build_attr_dicts(attr_names, attr_types, json_names)
        # debug input args
        self.__debug_input_args(args)
        # Process positional args
        numkw = len(kwargs) if kwargs else 0
        if numkw > 0:
            LOGGER.debug('XmattersBase.__init__ - numkw: %d', numkw)
        # First check if arguments come in as a dictionary
        if args and len(args) == 1 and isinstance(args[0], dict):
            self.__process_dictionary_args(json_names, args)
        # Next check if the args are passed in as raw values
        elif args:
            self.__process_positional_args(attr_names, attr_types, args)
        # Process keyword args
        self.__process_keyword_args(arg_names, kwargs)
        # Final check for required arguments
        self.__confirm_required_args(arg_names)

    def __eq__(self, other):
        for key, value in self.__dict__.items():
            if not key:
                return NotImplemented

            if key not in self.attrdict:
                continue

            if key not in other.__dict__:
                return False

            if other.__dict__[key] != value:
                return False
        return True

    def __ne__(self, other):
        return not self == other

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Creates and initializes an instance of cls.

        Args:
            cls (class): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a Error.

        Returns:
            oject: An instance of cls populated with json_self.
        """
        new_obj = cls(json_self)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Creates and initializes an instance of a cls.

        Args:
            cls (class): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a cls.

        Returns:
            object: An instance of cls populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

def main():
    """In case we ever need to run this stand-alone"""
    pass

if __name__ == '__main__':
    main()
