#!/usr/bin/env python3
# encoding: utf-8
"""Unit tests for xmatters.common.
"""

import json
import logging
import sys
import unittest

from xmatters import Error
from xmatters import Pagination
from xmatters import PaginationLinks
from xmatters import ReferenceById
from xmatters import ReferenceByIdAndSelfLink
from xmatters import SelfLink
from xmatters import XmattersList

from tests import _LOG_FILENAME
from tests import _LOG_LEVEL

XLOGGER = logging.getLogger('xlogger')
XLOGGER.level = _LOG_LEVEL
XSTREAM_HANDLER = logging.StreamHandler(sys.stdout)
XLOGGER.addHandler(XSTREAM_HANDLER)
XFILE_HANDLER = logging.FileHandler(_LOG_FILENAME)
XLOGGER.addHandler(XFILE_HANDLER)

class ErrorTest(unittest.TestCase):
    """Collection of unit tests cases for the Error class
    """

    def setUp(self):
        XLOGGER.info("XLOGGER.info ErrorTest.setUp")
        self.code = 404
        self.reason = "Not Found"
        self.message = (
            "Could not find a person with id 0313142d3-4703-a90e-36cc5f5f6209")
        self.err_json_str = (
            '{"code":%d,"reason":"%s","message":"%s"}')%(
            self.code, self.reason, self.message)

    def tearDown(self):
        XLOGGER.debug("ErrorTest.tearDown")

    def test_Error(self):
        XLOGGER.debug("ErrorTest.test_Error: Start")
        obj1 = Error(self.code, self.reason, self.message)
        self.assertIsInstance(obj1, Error)
        self.assertEqual(obj1.code, self.code)
        self.assertEqual(obj1.reason, self.reason)
        self.assertEqual(obj1.message, self.message)
        self.assertRaises(
            TypeError, Error, self.message, self.code, self.reason)
        self.assertRaises(TypeError, Error, self.code, self.reason)
        obj2 = Error(
            code=self.code, reason=self.reason, message=self.message)
        self.assertIsInstance(obj2, Error)
        self.assertEqual(obj2.code, self.code)
        self.assertEqual(obj2.reason, self.reason)
        self.assertEqual(obj2.message, self.message)
        self.assertRaises(TypeError, Error,
                reason=self.code, code=self.reason, message=self.message)
        self.assertRaises(TypeError, Error,
                code=self.code, message=self.message)
        self.assertEqual(obj1, obj2)
        XLOGGER.debug("ErrorTest.test_Error: Success")

    def test_Error_from_json_obj(self):
        XLOGGER.debug("ErrorTest.test_Error_from_json_obj: Start")
        json_obj = json.loads(self.err_json_str)
        obj = Error.from_json_obj(json_obj)
        self.assertIsInstance(obj, Error)
        obj1 = Error(self.code, self.reason, self.message)
        self.assertEqual(obj, obj1)
        XLOGGER.debug("ErrorTest.test_Error_from_json_obj: Success")

    def test_Error_from_json_str(self):
        XLOGGER.debug("ErrorTest.test_Error_from_json_str: Start")
        obj = Error.from_json_str(self.err_json_str)
        self.assertIsInstance(obj, Error)
        obj1 = Error(self.code, self.reason, self.message)
        self.assertEqual(obj, obj1)
        XLOGGER.debug("ErrorTest.test_Error_from_json_str: Success")

class PaginationLinksTest(unittest.TestCase):
    """Collection of unit tests cases for the PaginationLinks class
    """

    def setUp(self):
        XLOGGER.debug("PaginationLinksTest.setUp")
        self.self = "/api/xm/1/people?offset=100&limit=100"
        self.previous = "/api/xm/1/people?offset=0&limit=100"
        self.next = "/api/xm/1/people?offset=200&limit=100"
        self.links_json_str = (
            '{"self": "%s", "previous": "%s", "next": "%s" }'
            )%(self.self, self.previous, self.next)
        self.min_links_json_str = (
            '{"self": "%s"}'
            )%(self.self)
        self.bad_links_json_str = (
            '{"next": "%s", "previous": "%s" }'
            )%(self.next, self.previous)

    def tearDown(self):
        XLOGGER.debug("PaginationLinksTest.tearDown")

    def test_PaginationLinks(self):
        XLOGGER.debug(
            "PaginationLinksTest.test_PaginationLinks: Start")
        obj1 = PaginationLinks(self.self, self.previous, self.next)
        self.assertIsInstance(obj1, PaginationLinks)
        self.assertEqual(obj1.self, self.self)
        self.assertEqual(obj1.previous, self.previous)
        self.assertEqual(obj1.next, self.next)
        obj2 = PaginationLinks(
            next_link=self.next, previous_link=self.previous,
            self_link=self.self)
        self.assertIsInstance(obj2, PaginationLinks)
        self.assertEqual(obj1, obj2)
        obj3 = PaginationLinks(self.self)
        self.assertIsInstance(obj3, PaginationLinks)
        self.assertEqual(obj3.self, self.self)
        self.assertIsNone(obj3.previous)
        self.assertIsNone(obj3.next)
        self.assertRaises(TypeError, PaginationLinks, 1)
        self.assertRaises(TypeError, PaginationLinks, 0, self.previous)
        XLOGGER.debug("PaginationLinksTest.test_PaginationLinks Success")

    def test_PaginationLinks_from_json_obj(self):
        XLOGGER.debug(
            "PaginationLinksTest.test_PaginationLinks_from_json_obj: Start")
        json_obj = json.loads(self.links_json_str)
        obj = PaginationLinks.from_json_obj(json_obj)
        self.assertIsInstance(obj, PaginationLinks)
        obj1 = PaginationLinks(self.self, self.previous, self.next)
        self.assertEqual(obj, obj1)
        XLOGGER.debug(
            "PaginationLinksTest.test_PaginationLinks_from_json_obj: Success")

    def test_PaginationLinks_from_json_str(self):
        XLOGGER.debug(
            "PaginationLinksTest.test_PaginationLinks_from_json_str: Start")
        obj = PaginationLinks.from_json_str(self.links_json_str)
        self.assertIsInstance(obj, PaginationLinks)
        self.assertRaises(TypeError, PaginationLinks.from_json_str, self.bad_links_json_str)
        obj1 = PaginationLinks(self.self, self.previous, self.next)
        self.assertEqual(obj, obj1)
        XLOGGER.debug(
            "PaginationLinksTest.test_PaginationLinks_from_json_str: Success")

#pylint:disable=too-many-instance-attributes
class PaginationTest(unittest.TestCase):
    """Collection of unit tests cases for the Pagination class
    """

    def setUp(self):
        XLOGGER.debug("PaginationTest.setUp")
        self.count = 100
        self.total = 235
        self.data_id1 = "8f2d98ed-eaa9-4b0b-b366-c1db06b27e1f"
        self.data_id2 = "8f2d98ed-eaa9-4b0b-b366-c1db06b27e1f"
        self.data = [{"id": self.data_id1},{"id": self.data_id2}]
        self.self = "/api/xm/1/people?offset=0&limit=100"
        self.previous = None
        self.next = "/api/xm/1/people?offset=100&limit=100"
        self.links_json_str = (
            '{"self": "%s", "next": "%s"}'
            )%(self.self, self.next)
        self.links = PaginationLinks.from_json_str('%s'%self.links_json_str)
        self.pagi_json_str = (
            '{"count": %d, "total": %d, '
            '"data": [{"id": "%s"},{"id": "%s"}], '
            '"links": %s}'
            )%(self.count, self.total, self.data_id1,
               self.data_id2, self.links_json_str)
        self.bad_json1 = (
            '{"count": %d}'
            )%(self.count)
        self.bad_json2 = (
            '{"count": %d, "total": %d}'
            )%(self.count, self.total)
        self.bad_json3 = (
            '{"count": %d, "total": %d, '
            '"data": [{"id": "%s"},{"id": "%s"}]}'
            )%(self.count, self.total, self.data_id1,
               self.data_id2)
        self.bad_json4 = (
            '{"data": %d, "links": %d, '
            '"count": [{"id": "%s"},{"id": "%s"}], '
            '"total": %s}'
            )%(self.count, self.total, self.data_id1,
               self.data_id2, self.links_json_str)

    def tearDown(self):
        XLOGGER.debug("PaginationTest.tearDown")

    def test_Pagination(self):
        XLOGGER.debug("PaginationTest.test_Pagination: Start")
        obj = Pagination(self.count, self.data, self.links, self.total)
        self.assertIsInstance(obj, Pagination)
        self.assertEqual(obj.count, self.count)
        self.assertEqual(obj.data, self.data)
        self.assertIsInstance(obj.links, PaginationLinks)
        self.assertEqual(obj.links, self.links)
        self.assertEqual(obj.total, self.total)
        self.assertRaises(TypeError, Pagination, self.count)
        self.assertRaises(TypeError, Pagination, self.count, self.data)
        self.assertRaises(TypeError, Pagination, self.count, self.data,
                          self.links)
        self.assertRaises(TypeError, Pagination, 'not an int', self.data,
                          self.links, self.total)
        self.assertRaises(TypeError, Pagination, self.count, 'not an object',
                          self.links, self.total)
        self.assertRaises(TypeError, Pagination, self.count, self.data,
                          'not a list', self.total)
        self.assertRaises(TypeError, Pagination, self.count, self.data,
                          self.links, 'not an int')
        XLOGGER.debug("PaginationTest.test_Pagination: Success")

    def test_Pagination_from_json_obj(self):
        XLOGGER.debug("PaginationTest.test_Pagination_from_json_obj: Start")
        json_obj = json.loads(self.pagi_json_str)
        obj = Pagination.from_json_obj(json_obj)
        self.assertIsInstance(obj, Pagination)
        obj1 = Pagination(self.count, self.data, self.links, self.total)
        self.assertEqual(obj, obj1)
        XLOGGER.debug("PaginationTest.test_Pagination_from_json_obj: Success")

    def test_Pagination_from_json_str(self):
        XLOGGER.debug("PaginationTest.test_Pagination_from_json_str: Start")
        obj = Pagination.from_json_str(self.pagi_json_str)
        self.assertIsInstance(obj, Pagination)
        obj1 = Pagination(self.count, self.data, self.links, self.total)
        self.assertEqual(obj, obj1)
        self.assertRaises(TypeError, Pagination.from_json_str, self.bad_json1)
        self.assertRaises(TypeError, Pagination.from_json_str, self.bad_json2)
        self.assertRaises(TypeError, Pagination.from_json_str, self.bad_json3)
        self.assertRaises(TypeError, Pagination.from_json_str, self.bad_json4)
        XLOGGER.debug("PaginationTest.test_Pagination_from_json_str: Success")

class SelfLinkTest(unittest.TestCase):
    """Collection of unit tests cases for the SelfLink class
    """

    def setUp(self):
        XLOGGER.debug("SelfLinkTest.setUp")
        self.self = "/api/xm/1/people/84a6dde7-82ad-4e64-9f4d-3b9001ad60de"
        self.self_json_str = ('{"self": "%s"}')%(self.self)
        self.bad_json1 = '{"self": 0}'
        self.bad_json2 = '{}'

    def tearDown(self):
        XLOGGER.debug("SelfLinkTest.tearDown")

    def test_SelfLink(self):
        XLOGGER.debug("Start test_SelfLink")
        obj = SelfLink(self.self)
        self.assertIsInstance(obj, SelfLink)
        self.assertEqual(obj.self, self.self)
        self.assertRaises(TypeError, SelfLink)
        self.assertRaises(TypeError, SelfLink, 0)
        XLOGGER.debug("test_SelfLink Successful")

    def test_SelfLink_from_json_obj(self):
        XLOGGER.debug("SelfLinkTest.test_SelfLink_from_json_obj: Start")
        json_obj = json.loads(self.self_json_str)
        obj = SelfLink.from_json_obj(json_obj)
        self.assertIsInstance(obj, SelfLink)
        self.assertEqual(obj.self, self.self)
        XLOGGER.debug("SelfLinkTest.test_SelfLink_from_json_obj: Success")

    def test_SelfLink_from_json_str(self):
        XLOGGER.debug("SelfLinkTest.test_SelfLink_from_json_str: Start")
        obj = SelfLink.from_json_str(self.self_json_str)
        self.assertIsInstance(obj, SelfLink)
        self.assertEqual(obj.self, self.self)
        self.assertRaises(TypeError, SelfLink.from_json_str, self.bad_json1)
        self.assertRaises(TypeError, SelfLink.from_json_str, self.bad_json2)
        XLOGGER.debug("SelfLinkTest.test_SelfLink_from_json_str: Success")

class ReferenceByIdTest(unittest.TestCase):
    """Collection of unit tests cases for the ReferenceById class
    """

    def setUp(self):
        XLOGGER.debug("ReferenceByIdTest.setUp")
        self.id = "/api/xm/1/people/84a6dde7-82ad-4e64-9f4d-3b9001ad60de"
        self.id_json_str = ('{"id": "%s"}')%(self.id)
        self.bad_json_str1 = '{"id": 0}'
        self.bad_json_str2 = "{}"

    def tearDown(self):
        XLOGGER.debug("ReferenceByIdTest.tearDown")

    def test_ReferenceById(self):
        XLOGGER.debug("ReferenceByIdTest.test_ReferenceById: Start")
        obj = ReferenceById(self.id)
        self.assertIsInstance(obj, ReferenceById)
        self.assertEqual(obj.id, self.id)
        self.assertRaises(TypeError, ReferenceById)
        self.assertRaises(TypeError, ReferenceById, 0)
        XLOGGER.debug("ReferenceByIdTest.test_ReferenceById: Success")

    def test_ReferenceById_from_json_obj(self):
        XLOGGER.debug(
            "ReferenceByIdTest.test_ReferenceById_from_json_obj: Start")
        json_obj = json.loads(self.id_json_str)
        obj = ReferenceById.from_json_obj(json_obj)
        self.assertIsInstance(obj, ReferenceById)
        obj1 = ReferenceById(self.id)
        self.assertEqual(obj, obj1)
        XLOGGER.debug(
            "ReferenceByIdTest.test_ReferenceById_from_json_obj: Success")

    def test_ReferenceById_from_json_str(self):
        XLOGGER.debug(
            "ReferenceByIdTest.test_ReferenceById_from_json_str: Start")
        obj = ReferenceById.from_json_str(self.id_json_str)
        self.assertIsInstance(obj, ReferenceById)
        obj1 = ReferenceById(self.id)
        self.assertEqual(obj, obj1)
        self.assertRaises(
            TypeError, ReferenceById.from_json_str, self.bad_json_str1)
        self.assertRaises(
            TypeError, ReferenceById.from_json_str, self.bad_json_str2)
        XLOGGER.debug(
            "ReferenceByIdTest.test_ReferenceById_from_json_str: Success")

class ReferenceByIdAndSelfLinkTest(unittest.TestCase):
    """Collection of unit tests cases for the ReferenceByIdAndSelfLink class
    """
    def setUp(self):
        XLOGGER.debug("ReferenceByIdAndSelfLinkTest.setUp")
        self.id = "f0c572a8-45ec-fe23-289c-df749cf19a5e"
        self.self = "/api/xm/1/sites/f0c572a8-45ec-fe23-289c-df749cf19a5e"
        self.previous = None
        self.next = None
        self.links_json_str = ('{"self": "%s"}')%(self.self)
        self.links =SelfLink.from_json_str(self.links_json_str)
        self.id_json_str = (
            '{"id": "%s", "links": %s}'
            )%(self.id, self.links_json_str)
        self.bad_json_str1 = (
            '{"id": "%s"}'
            )%(self.id)
        self.bad_json_str2 = (
            '{"links": %s}'
            )%(self.links_json_str)
        self.bad_json_str3 = (
            '{"id": 0, "links": %s}'
            )%(self.links_json_str)
        self.bad_json_str4 = (
            '{"id": "%s", "links": 0}'
            )%(self.id)

    def tearDown(self):
        XLOGGER.debug("ReferenceByIdAndSelfLinkTest.tearDown")

    def test_ReferenceByIdAndSelfLink(self):
        XLOGGER.debug(
            "ReferenceByIdAndSelfLinkTest.test_ReferenceByIdAndSelfLink: Start")
        obj = ReferenceByIdAndSelfLink(self.id, self.links)
        self.assertIsInstance(obj, ReferenceByIdAndSelfLink)
        self.assertEqual(obj.id, self.id)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links, self.links)
        self.assertRaises(TypeError, ReferenceByIdAndSelfLink, self.id)
        self.assertRaises(TypeError, ReferenceByIdAndSelfLink, 0,  self.links)
        self.assertRaises(TypeError, ReferenceByIdAndSelfLink, self.id, 0)
        XLOGGER.debug(
            "ReferenceByIdAndSelfLinkTest.test_ReferenceByIdAndSelfLink: Succe")

    def test_ReferenceByIdAndSelfLink_from_json_obj(self):
        XLOGGER.debug(
            "ReferenceByIdAndSelfLinkTest."
            "test_ReferenceByIdAndSelfLink_from_json_obj: Start")
        json_obj = json.loads(self.id_json_str)
        obj = ReferenceByIdAndSelfLink.from_json_obj(json_obj)
        self.assertIsInstance(obj, ReferenceByIdAndSelfLink)
        obj1 = ReferenceByIdAndSelfLink(self.id, self.links)
        self.assertEqual(obj, obj1)
        XLOGGER.debug(
            "ReferenceByIdAndSelfLinkTest."
            "test_ReferenceByIdAndSelfLink_from_json_obj: Success")

    def test_ReferenceByIdAndSelfLink_from_json_str(self):
        XLOGGER.debug(
            "ReferenceByIdAndSelfLinkTest."
            "test_ReferenceByIdAndSelfLink_from_json_str: Start")
        obj = ReferenceByIdAndSelfLink.from_json_str(self.id_json_str)
        self.assertIsInstance(obj, ReferenceByIdAndSelfLink)
        obj1 = ReferenceByIdAndSelfLink(self.id, self.links)
        self.assertEqual(obj, obj1)
        self.assertRaises(TypeError, ReferenceByIdAndSelfLink.from_json_str,
            self.bad_json_str1)
        self.assertRaises(TypeError, ReferenceByIdAndSelfLink.from_json_str,
            self.bad_json_str2)
        self.assertRaises(TypeError, ReferenceByIdAndSelfLink.from_json_str,
            self.bad_json_str3)
        self.assertRaises(TypeError, ReferenceByIdAndSelfLink.from_json_str,
            self.bad_json_str4)
        XLOGGER.debug(
            "ReferenceByIdAndSelfLinkTest."
            "test_ReferenceByIdAndSelfLink_from_json_str: Success")

if __name__ == "__main__":
    sys.argv = ['', 'XmattersListTest.test_TestList']
    unittest.main()
