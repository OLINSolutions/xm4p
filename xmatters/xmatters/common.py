# -*- coding: utf-8 -*-
"""xMatters Common Objects

Common objects used throughout the xMatters API.

Reference:
    https://help.xmatters.com/xmAPI/index.html#common-objects

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

import logging

from xmatters import XmattersBase
from xmatters import XmattersList

LOGGER = logging.getLogger('xlogger')

class Error(XmattersBase):
    """xMatters Error object representation

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
    """xMatters PaginationLinks object representation

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
    """xMatters Pagination object representation

    A page of results. Use the links in the links field to retrieve the rest
    of the result set. See also Results pagination.
    This Class really is a pattern that is followed when the xMatters
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
    """xMatters SelfLink representation

    A link that can be used to reference this object in the xMatters API.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#selfLink

    Args:
        self (str): A link that can be used to access this resource
            with a GET request.

    Attributes:
        self (str): A link that can be used to access this resource
            with a GET request.
    """
    _arg_names = ['self']
    _attr_names = _json_names = ['self']
    _attr_types = [str]


class ReferenceById(XmattersBase):
    """xMatters ReferenceById representation

    The identifier of a resource.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#referenceByID-object

    Args:
        id (str): The identifier of a resource.

    Attributes:
        id (str): The identifier of a resource.
    """
    _arg_names = _attr_names = _json_names = ['id']
    _attr_types = [str]


class ReferenceByIdAndSelfLink(XmattersBase):
    """xMatters ReferenceByIdAndSelfLink representation

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
