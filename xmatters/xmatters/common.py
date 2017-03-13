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

    def _setattr(self, name, value):
        if isinstance(value, dict):
            print('XmattersBase._setattr - value is instance of dict')
            newType = self.type_dict()[name]
            print('XmattersBase._setattr - newType: %s'%(newType.__name__))
            newValue = newType(value)
            print('XmattersBase._setattr - newValue(%s): %s'%(
                newValue.__class__.__name__, str(newValue)))
            setattr(self, name, newValue)
        else:
            print('XmattersBase._setattr - value IS NOT instance of dict')
            setattr(self, name, value)

    def _preprocess_arg_names(self, names):
        arg_names = []
        req_args = []
        for arg in names:
            arg_names.append(arg if arg[0] is not '*' else arg[1:])
            req_args.append(arg[0] is not '*')
        return arg_names, req_args

    def _build_dicts(self, arg_names, req_args,
                     attr_names, attr_types, json_names):
        setattr(self, '__arg_dict', dict(zip(arg_names, attr_names)))
        setattr(self, '__req_args_dict', dict(zip(arg_names, req_args)))
        setattr(self, '__attr_dict', dict(zip(attr_names, json_names)))
        setattr(self, '__type_dict', dict(zip(attr_names, attr_types)))
        setattr(self, '__json_dict', dict(zip(json_names, attr_names)))

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
            TypeError: The wrong number of arguments were specified, or
                the type of the value is not correct, or 
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
        arg_names, req_args = self._preprocess_arg_names(arg_names)
        # Initialize attributes
        for name in attr_names:
            setattr(self, name, None)
        # Create lookup dictionaries
        self._build_dicts(
            arg_names, req_args,
            attr_names, attr_types, json_names)
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
        if (args and len(args) == 1 and type(args[0]) is dict):
            for dictionary in args:
                for key in dictionary:
                    if key in json_names:
                        print('Using args as dict to set %s from %s to %s'%(
                             self.json_dict()[key], key, dictionary[key]))
                        self._setattr(self.json_dict()[key], dictionary[key])
        elif args and len(args) == (len(attr_names) - numkw):
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
        elif args and len(args) != (len(attr_names) - numkw):
            raise TypeError((
                "Initializing class %s. Invalid number of positional and "
                "keyword arguments. Expecting %d but received %d")%(
                    cls.__name__, len(attr_names), len(args) + numkw))
        # Process keyword args
        for key in kwargs:
            if key in arg_names:
                attr_name = self.arg_dict()[key]
                if type(kwargs[key]) is not self.type_dict()[attr_name]:
                    raise TypeError((
                        "Initializing class %s. Keyword argument '%s' "
                        "should be a %s, but a %s was found")%(
                        cls.__name__, key, str(self.type_dict()[attr_name]),
                        str(type(kwargs[key]))))
                print('Using kwargs to set %s from %s to %s'%(
                    self.arg_dict()[key], key, kwargs[key]))
                self._setattr(self.arg_dict()[key], kwargs[key])
        # Final check for required arguments
        missing_args = []
        for key in arg_names:
            if self.req_args_dict()[key]:
                if getattr(self, self.arg_dict()[key]) is None:
                    missing_args.append(self.arg_dict()[key])
        if missing_args:
            raise TypeError("Initializing class %s. Missing arguments: %s."%(
                cls.__name__, ",".join(missing_args)))

    def arg_dict(self) -> dict:
        return getattr(self, '__arg_dict')

    def req_args_dict(self) -> dict:
        return getattr(self, '__req_args_dict')

    def attr_dict(self) -> dict:
        return getattr(self, '__attr_dict')

    def json_dict(self) -> dict:
        return getattr(self, '__json_dict')

    def type_dict(self) -> dict:
        return getattr(self,'__type_dict')

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
    
    @classmethod
    def from_json_obj(cls, json_self: object):
        """Creates and initializes an instance of a Error.

        Args:
            cls (:class:`Error`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a Error.

        Returns:
            Error: An instance populated with json_self.
        """
        new_obj = cls(json_self)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Creates and initializes an instance of a Error.

        Args:
            cls (:class:`Error`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a Error.

        Returns:
            Error: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self, *initial_data, **kwargs):
        super().__init__(*initial_data, **kwargs)
        
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
    
    @classmethod
    def from_json_obj(cls, json_self: object):
        """Creates and initializes an instance of a PaginationLinks.

        Args:
            cls (:class:`PaginationLinks`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a PaginationLink.

        Returns:
            PaginationLinks: An instance populated with json_self.
        """
        new_obj = cls(json_self['links'] if 'links' in json_self else json_self)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Creates and initializes an instance of a PaginationLinks.

        Args:
            cls (:class:`PaginationLinks`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a PaginationLink.

        Returns:
            PaginationLinks: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self, *initial_data, **kwargs):
        super().__init__(*initial_data, **kwargs)


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
        count (int, optional): The number of items in this page of results.
        data (:obj:`list` of :obj:`JSON`, optional):
            An array of the paginated object.
        links (:obj:`PaginationLinks`, optional): Links to the current,
            previous, and next pages of results.
        total (int, optional): The total number of items in the result set.

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

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Creates and initializes an instance of a Pagination.

        Args:
            cls (:class:`Pagination`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a Pagination.

        Returns:
            Pagination: An instance populated with json_self.
        """
        new_obj = cls(json_self)
#        new_obj = cls(
#            json_self['count'] if 'count' in json_self else None,
#            json_self['data'] if 'data' in json_self else [],
#            (PaginationLinks.from_json_obj(json_self['links'])
#             if 'links' in json_self else PaginationLinks()),
#            json_self['total'] if 'total' in json_self else None)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Creates and initializes an instance of a Pagination.

        Args:
            cls (:class:`Pagination`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a Pagination.

        Returns:
            Pagination: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self, *initial_data, **kwargs):
        super().__init__(*initial_data, **kwargs)
#    def __init__(
#            self, count: int = None, data: [] = None,
#            links: PaginationLinks = None, total: int = None):
#        self.count: int = count
#        self.data: [] = data if data is not None else []
#        self.links: PaginationLinks = links
#        self.total: int = total

class SelfLink(object):
    """xmatters SelfLink representation

    A link that can be used to reference this object in the xmatters API.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#selfLink

    Args:
        link (str, optional): A link that can be used to access this resource
            with a GET request.

    Attributes:
        self (str): A link that can be used to access this resource
            with a GET request.
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build an SelfLink instance from a JSON object

        Args:
            cls (:class:`SelfLink`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a SelfLink.

        Returns:
            SelfLink: An instance populated with json_self.
        """
        new_obj = cls(json_self['self'] if 'self' in json_self else None)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build an SelfLink instance from a JSON payload string

        Args:
            cls (:class:`SelfLink`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a SelfLink.

        Returns:
            SelfLink: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self, link: str = None):
        self.self: str = link

class ReferenceById(object):
    """xmatters ReferenceById representation

    The identifier of a resource.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#referenceByID-object

    Args:
        ref_id (str, optional): The identifier of a resource.

    Attributes:
        id (str): The identifier of a resource.
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build an ReferenceById instance from a JSON object

        Args:
            cls (:class:`ReferenceById`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a ReferenceById.

        Returns:
            ReferenceById: An instance populated with json_self.
        """
        new_obj = cls(json_self['id'] if 'id' in json_self else None)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build an ReferenceById instance from a JSON payload string

        Args:
            cls (:class:`ReferenceById`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a ReferenceById.

        Returns:
            ReferenceById: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self, ref_id: str = None):
        self.id: str = ref_id

class ReferenceByIdAndSelfLink(object):
    """xmatters ReferenceByIdAndSelfLink representation

    The identifier of a resource and a SelfLink object that contains a URL
    to the resource.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#referenceByIdAndSelfLink-object

    Args:
        ref_id (str, optional): URI to next page of results.
        links (:obj:`SelfLink`, optional): A link that can be used to
            retrieve the person using this API.

    Attributes:
        id (str): The unique identifier of the person.
        links (:obj:`SelfLink`): A link that can be used to retrieve the person
            using this API.
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build an ReferenceByIdAndSelfLink instance from a JSON object

        Args:
            cls (:class:`ReferenceByIdAndSelfLink`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a ReferenceByIdAndSelfLink.

        Returns:
            ReferenceByIdAndSelfLink: An instance populated with json_self.
        """
        new_obj = cls(
            json_self['id'] if 'id' in json_self else None,
            (SelfLink.from_json_obj(json_self['links'])
             if 'links' in json_self else SelfLink())
            )
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build a ReferenceByIdAndSelfLink instance from JSON payload str

        Args:
            cls (:class:`ReferenceByIdAndSelfLink`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a ReferenceByIdAndSelfLink.

        Returns:
            ReferenceByIdAndSelfLink: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self, ref_id: str = None, links: SelfLink = None):
        self.id: str = ref_id
        self.links: SelfLink = links

def main():
    """In case we ever need to run this stand-alone"""
    pass

if __name__ == '__main__':
    main()
