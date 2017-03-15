# -*- coding: utf-8 -*-
"""xmatters Common Objects

Common objects used throughout the xmatters API.

Reference:
    https://help.xmatters.com/xmAPI/index.html#common-objects

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

import json

class XmattersBase(object):

    @property
    def argdict(self) -> dict:
        """:obj:`dict` of :obj:`str`: Argument to member name dictionary"""
        return getattr(self, '__arg_dict')

    @property
    def reqargs(self) -> dict:
        """:obj:`dict` of :obj:`str`: Argument to required flag dictionary"""
        return getattr(self, '__req_args_dict')

    @property
    def attrdict(self) -> dict:
        """:obj:`dict` of :obj:`str`: Attribute to argument name dictionary"""
        return getattr(self, '__attr_dict')

    @property
    def typedict(self) -> dict:
        """:obj:`dict` of :obj:`str`: Attribute to argument type dictionary"""
        return getattr(self,'__type_dict')

    @property
    def jsondict(self) -> dict:
        """:obj:`dict` of :obj:`str`: Attribute to JSON name dictionary"""
        return getattr(self, '__json_dict')

    def _setattr(self, name, value):
        """Convert dictionaries to their class instance based on typedict"""
        if isinstance(value, dict):
            print('XmattersBase._setattr - value is instance of dict')
            newType = self.typedict[name]
            print('XmattersBase._setattr - newType: %s'%(newType.__name__))
            value = newType(value)
            print('XmattersBase._setattr - value(%s): %s'%(
                value.__class__.__name__, str(value)))
        else:
            print('XmattersBase._setattr - value IS NOT instance of dict')
        setattr(self, name, value)

    def _process_arg_names(self, names: list) -> (dict, dict):
        """(dict, dict): Builds name and req'd field dicts from tagged names"""
        arg_names = []
        req_args = []
        for arg in names:
            arg_names.append(arg if arg[0] is not '*' else arg[1:])
            req_args.append(arg[0] is not '*')
        return arg_names, req_args

    def _build_dicts(self, arg_names, req_args,
                     attr_names, attr_types, json_names):
        """Creates the internal member lookup dictionaries"""
        setattr(self, '__arg_dict', dict(zip(arg_names, attr_names)))
        setattr(self, '__req_args_dict', dict(zip(arg_names, req_args)))
        setattr(self, '__attr_dict', dict(zip(attr_names, json_names)))
        setattr(self, '__type_dict', dict(zip(attr_names, attr_types)))
        setattr(self, '__json_dict', dict(zip(json_names, attr_names)))

    def _is_proper_type(self, attr, value) -> bool:
        """bool: True if value is the proper type expected by attr"""
        return type(value) is self.attrdict[attr]
    
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
        # Get arguments and attribute information from subclass
        cls = self.__class__
        print('XmattersBase.__init__ - cls.__name__: %s'%(cls.__name__))
        arg_names = cls._arg_names
        print('XmattersBase.__init__ - cls._arg_names: %s'%str(arg_names))
        attr_names = cls._attr_names
        print('XmattersBase.__init__ - cls._attr_names: %s'%str(attr_names))
        attr_types = cls._attr_types
        print('XmattersBase.__init__ - cls._attr_types: %s'%str(attr_types))
        json_names = cls._json_names
        print('XmattersBase.__init__ - cls._json_names: %s'%str(json_names))
        # Fixup argument names and build required arguments array
        arg_names, req_args = self._process_arg_names(arg_names)
        # Create and initialize attributes
        for name in attr_names:
            setattr(self, name, None)
        # Create lookup dictionaries
        self._build_dicts(
            arg_names, req_args,
            attr_names, attr_types, json_names)
        # debug input args
        if args:
            print('type(args): %s'%str(type(args)))
            print('args(%d): %s:%s'%(
                len(args) if args is not None else 0,
                str(type(args[0]) if args is not None else 'None'),
                str(args[0]) if args is not None else 'None'))
            print(dir(args))
            print((type(args[0]) 
                if args is not None and 
                    len(args) == 1 else 'n/a'))
        # Process positional args
        numkw = len(kwargs) if kwargs else 0
        print('numkw: %d'%numkw)
        # First check if arguments come in as a dictionary
        if (args and len(args) == 1 and type(args[0]) is dict):
            for dictionary in args:
                for key in dictionary:
                    if key in json_names:
                        if self._is_proper_type(self.jsondict[key],
                                                dictionary[key]):
                            print('Using args as dict to set %s from %s to %s'%(
                                self.jsondict[key], key, dictionary[key]))
                            self._setattr(self.jsondict[key], dictionary[key])
                        else:
                            raise TypeError((
                                "Initializing class %s. JSON Attribute %s "
                                "should be a %s, but a %s was found")%(
                                cls.__name__, key,
                                str(self.typedict[self.jsondict[key]]), 
                                str(type(dictionary[key]))))
        # Next check if the args are passed in as raw values
        elif args:
            key = 0
            for value in args:
                if type(value) is not attr_types[key]:
                    raise TypeError((
                        "Initializing class %s. Attribute at position %d (%s) "
                        "should be a %s, but a %s was found")%(
                        cls.__name__, key, attr_names[key],
                        str(attr_types[key]), str(type(value))))
                print('Using positional arg %d to set %s to %s'%(
                    key, attr_names[key], str(value)))
                self._setattr(attr_names[key], value)
                key += 1
        # Process keyword args
        for key in kwargs:
            if key in arg_names:
                attr_name = self.argdict[key]
                if type(kwargs[key]) is not self.typedict[attr_name]:
                    raise TypeError((
                        "Initializing class %s. Keyword argument '%s' "
                        "should be a %s, but a %s was found")%(
                        cls.__name__, key, str(self.typedict[attr_name]),
                        str(type(kwargs[key]))))
                print('Using kwargs to set %s from %s to %s'%(
                    self.argdict[key], key, kwargs[key]))
                self._setattr(self.argdict[key], kwargs[key])
        # Final check for required arguments
        missing_args = []
        for key in arg_names:
            if self.reqargs[key]:
                if getattr(self, self.argdict[key]) is None:
                    missing_args.append(self.argdict[key])
        if missing_args:
            raise TypeError("Initializing class %s. Missing arguments: %s."%(
                cls.__name__, ",".join(missing_args)))

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


class Error(XmattersBase):
    """xmatters Error object representation

    Describes an error.
    For a complete list of error response codes, see HTTP response codes.
    https://help.xmatters.com/xmAPI/index.html#HTTP-response-codes

    Reference:
        https://help.xmatters.com/xmAPI/index.html#error-object

    Args:
        code (int): The HTTP error code.
        reason (str): A description of the error code.
        message (str): A description of specific err that occurred.

    Attributes:
        code (int): The HTTP error code.
        reason (str): A description of the error code.
        message (str): A description of the specific error that occurred.
    """

    _arg_names = _attr_names = _json_names = ['code', 'reason', 'message']
    _attr_types = [int, str, str]


class PaginationLinks(XmattersBase):
    """xmatters PaginationLinks object representation

    Provides links to cur, prev, and next pages of a paginated result set.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#paginationLinks

    Args:
        self_link (str): URI to the parent object.
        previous_link (str, optional): URI to the previous page of results.
        next_link (str, optional): URI to next page of results.

    Attributes:
        self (str): URI to the parent object.
        previous (str): URI to the previous page of results.
        next (str): URI to next page of results.
    """

    _arg_names = ['self_link', '*previous_link', '*next_link']
    _attr_names = _json_names = ['self', 'previous', 'next']
    _attr_types = [str, str, str]


class Pagination(XmattersBase):
    """xmatters Pagination object representation

    A page of results. Use the links in the links field to retrieve the rest
    of the result set. See also Results pagination.
    This Class really is a pattern that is followed when the xmatters
    API is returning a paginated set of results.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#pagination-object
        https://help.xmatters.com/xmAPI/index.html#results-pagination

    Args:
        count (int): The number of items in this page of results.
        data (:obj:`list` of :obj:`JSON`): An array of the paginated object.
        links (:obj:`PaginationLinks`): Links to the current,
            previous, and next pages of results.
        total (int): The total number of items in the result set.

    Attributes:
        count (int): The number of items in this page of results.
        data (:obj:`list` of :obj:`JSON`): An array of the paginated object.
        links (:obj:`PaginationLinks`): Links to the current, previous, and
            next pages of results.
        total (int): The total number of items in the result set.
    """
    _arg_names = _attr_names = _json_names = [
        'count', 'data', 'links', 'total']
    _attr_types = [int, list, PaginationLinks, int]


class SelfLink(XmattersBase):
    """xmatters SelfLink representation

    A link that can be used to reference this object in the xmatters API.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#selfLink

    Args:
        link (str): A link that can be used to access this resource
            with a GET request.

    Attributes:
        self (str): A link that can be used to access this resource
            with a GET request.
    """
    _arg_names = ['self_link']
    _attr_names = _json_names = ['self']
    _attr_types = [str]


class ReferenceById(XmattersBase):
    """xmatters ReferenceById representation

    The identifier of a resource.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#referenceByID-object

    Args:
        ref_id (str): The identifier of a resource.

    Attributes:
        id (str): The identifier of a resource.
    """
    _arg_names = _attr_names = _json_names = ['id']
    _attr_types = [str]


class ReferenceByIdAndSelfLink(XmattersBase):
    """xmatters ReferenceByIdAndSelfLink representation

    The identifier of a resource and a SelfLink object that contains a URL
    to the resource.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#referenceByIdAndSelfLink-object

    Args:
        id (str): URI to next page of results.
        links (:obj:`SelfLink`): A link that can be used to
            retrieve the person using this API.

    Attributes:
        id (str): The unique identifier of the person.
        links (:obj:`SelfLink`): A link that can be used to retrieve the person
            using this API.
    """
    _arg_names = _attr_names = _json_names = ['id', 'links']
    _attr_types = [str, SelfLink]


def main():
    """In case we ever need to run this stand-alone"""
    pass

if __name__ == '__main__':
    main()
