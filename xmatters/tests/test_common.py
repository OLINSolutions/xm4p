#!/usr/bin/env python3
# encoding: utf-8
"""Unit tests for EventAuditReport.xmatters.common.
"""

import json
import logging
import sys
import unittest

from xmatters import Error
from xmatters import PaginationLinks
from xmatters import Pagination
from xmatters import SelfLink
from xmatters import ReferenceById
from xmatters import ReferenceByIdAndSelfLink

from . import _log_filename
from . import _log_level

XLOGGER = logging.getLogger('XLOGGER')
XLOGGER.level = _log_level
XSTREAM_HANDLER = logging.StreamHandler(sys.stdout)
XLOGGER.addHandler(XSTREAM_HANDLER)
XFILE_HANDLER = logging.FileHandler(_log_filename)
XLOGGER.addHandler(XFILE_HANDLER)

# pylint: disable=missing-docstring, invalid-name, no-member

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
            '{"code" : %d,"reason" : "%s","message" : '
            '"%s"}')%(self.code, self.reason, self.message)

    def tearDown(self):
        XLOGGER.debug("ErrorTest.tearDown")

    def test_Error_from_positional_args(self):
        XLOGGER.debug("Start test_Error_from_positional_args")
        obj = Error(self.code, self.reason, self.message)
        self.assertIsInstance(obj, Error)
        self.assertEqual(obj.code, self.code)
        self.assertEqual(obj.reason, self.reason)
        self.assertEqual(obj.message, self.message)
        XLOGGER.debug('argdict: ' + str(obj.argdict))
        self.assertRaises(TypeError, Error, self.message, self.code, self.reason)
        self.assertRaises(TypeError, Error, self.code, self.reason)
        XLOGGER.debug("test_Error_from_positional_args Successful")

    def test_Error_from_kw_args(self):
        XLOGGER.debug("Start test_Error_from_kw_args")
        obj = Error(
            code=self.code, reason=self.reason, message=self.message)
        self.assertIsInstance(obj, Error)
        self.assertEqual(obj.code, self.code)
        self.assertEqual(obj.reason, self.reason)
        self.assertEqual(obj.message, self.message)
        XLOGGER.debug('argdict: ' + str(obj.argdict))
        with self.assertRaises(TypeError) as cm:
            obj = Error(
                reason=self.code, code=self.reason, message=self.message)
        XLOGGER.debug(cm.exception.args)
        with self.assertRaises(TypeError) as cm:
            obj = Error(
                code=self.code, message=self.message)
        XLOGGER.debug(cm.exception.args)
        XLOGGER.debug("test_Error_from_kw_args Successful")

    def test_Error_from_json_obj(self):
        XLOGGER.debug("Start test_Error_from_json_obj")
        json_obj = json.loads(self.err_json_str)
        obj = Error.from_json_obj(json_obj)
        self.assertIsInstance(obj, Error)
        self.assertEqual(obj.code, self.code)
        self.assertEqual(obj.reason, self.reason)
        self.assertEqual(obj.message, self.message)
        XLOGGER.debug("test_Error_from_json_obj Successful")

    def test_Error_from_json_str(self):
        XLOGGER.debug("Start test_Error_from_json_str")
        obj = Error.from_json_str(self.err_json_str)
        self.assertIsInstance(obj, Error)
        self.assertEqual(obj.code, self.code)
        self.assertEqual(obj.reason, self.reason)
        self.assertEqual(obj.message, self.message)
        XLOGGER.debug("test_Error_from_json_str Successful")

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

    def test_PaginationLinks_from_kw_args(self):
        XLOGGER.debug("Start test_PaginationLinks_from_kw_args")
        obj = PaginationLinks(
            next_link=self.next, previous_link=self.previous,
            self_link=self.self)
        self.assertIsInstance(obj, PaginationLinks)
        self.assertEqual(obj.self, self.self)
        self.assertEqual(obj.previous, self.previous)
        self.assertEqual(obj.next, self.next)
        XLOGGER.debug('argdict: ' + str(obj.argdict))
        XLOGGER.debug("test_PaginationLinks_from_kw_args Successful")

    def test_PaginationLinks_from_positional_args(self):
        XLOGGER.debug("Start test_PaginationLinks_from_positional_args")
        obj = PaginationLinks(self.self, self.previous, self.next)
        self.assertIsInstance(obj, PaginationLinks)
        self.assertEqual(obj.self, self.self)
        self.assertEqual(obj.previous, self.previous)
        self.assertEqual(obj.next, self.next)
        XLOGGER.debug('argdict: ' + str(obj.argdict))
        obj = PaginationLinks(self.self)
        self.assertIsInstance(obj, PaginationLinks)
        self.assertEqual(obj.self, self.self)
        self.assertIsNone(obj.previous)
        self.assertIsNone(obj.next)
        self.assertRaises(TypeError, PaginationLinks, 1)
        self.assertRaises(TypeError, PaginationLinks, 0, self.previous)
        XLOGGER.debug("test_PaginationLinks_from_positional_args Successful")

    def test_PaginationLinks_from_json_obj(self):
        XLOGGER.debug("Start test_PaginationLinks_from_json_obj")
        json_obj = json.loads(self.links_json_str)
        obj = PaginationLinks.from_json_obj(json_obj)
        self.assertIsInstance(obj, PaginationLinks)
        self.assertEqual(obj.self, self.self)
        self.assertEqual(obj.previous, self.previous)
        self.assertEqual(obj.next, self.next)
        XLOGGER.debug("test_PaginationLinks_from_json_obj Successful")

    def test_PaginationLinks_from_json_str(self):
        XLOGGER.debug("Start test_PaginationLinks_from_json_str")
        obj = PaginationLinks.from_json_str(self.links_json_str)
        self.assertIsInstance(obj, PaginationLinks)
        self.assertEqual(obj.self, self.self)
        self.assertEqual(obj.previous, self.previous)
        self.assertEqual(obj.next, self.next)
        self.assertRaises(TypeError, PaginationLinks.from_json_str, self.bad_links_json_str)
        XLOGGER.debug("test_PaginationLinks_from_json_str Successful")

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
        XLOGGER.debug("Start test_Pagination")
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
        XLOGGER.debug("test_Pagination Successful")

    def test_Pagination_from_json_obj(self):
        XLOGGER.debug("Start test_Pagination_from_json_obj")
        json_obj = json.loads(self.pagi_json_str)
        obj = Pagination.from_json_obj(json_obj)
        self.assertIsInstance(obj, Pagination)
        self.assertEqual(obj.count, self.count)
        self.assertEqual(obj.data, self.data)
        self.assertIsInstance(obj.links, PaginationLinks)
        self.assertEqual(obj.links.self, self.links.self)
        self.assertEqual(obj.links.next, self.links.next)
        self.assertEqual(obj.total, self.total)
        XLOGGER.debug("test_Pagination_from_json_obj Successful")

    def test_Pagination_from_json_str(self):
        XLOGGER.debug("Start test_Pagination_from_json_str")
        obj = Pagination.from_json_str(self.pagi_json_str)
        self.assertIsInstance(obj, Pagination)
        self.assertEqual(obj.count, self.count)
        self.assertEqual(obj.data, self.data)
        self.assertIsInstance(obj.links, PaginationLinks)
        self.assertEqual(obj.links.self, self.links.self)
        self.assertEqual(obj.links.next, self.links.next)
        self.assertEqual(obj.total, self.total)
        self.assertRaises(TypeError, Pagination.from_json_str, self.bad_json1)
        self.assertRaises(TypeError, Pagination.from_json_str, self.bad_json2)
        self.assertRaises(TypeError, Pagination.from_json_str, self.bad_json3)
        self.assertRaises(TypeError, Pagination.from_json_str, self.bad_json4)
        XLOGGER.debug("test_Pagination_from_json_str Successful")

class SelfLinkTest(unittest.TestCase):
    """Collection of unit tests cases for the SelfLink class
    """

    def setUp(self):
        XLOGGER.debug("SelfLinkTest.setUp")
        self.self = "/api/xm/1/people/84a6dde7-82ad-4e64-9f4d-3b9001ad60de"
        self.self_json_str = ('{"self": "%s"}')%(self.self)
        self.bad_json1 = ('{"slf": "%s"}')%(self.self)
        self.bad_json2 = ('{"self": %d}')%(0)

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
        XLOGGER.debug("Start test_SelfLink_from_json_obj")
        json_obj = json.loads(self.self_json_str)
        obj = SelfLink.from_json_obj(json_obj)
        self.assertIsInstance(obj, SelfLink)
        self.assertEqual(obj.self, self.self)
        XLOGGER.debug("test_SelfLink_from_json_obj Successful")

    def test_SelfLink_from_json_str(self):
        XLOGGER.debug("Start test_SelfLink_from_json_str")
        obj = SelfLink.from_json_str(self.self_json_str)
        self.assertIsInstance(obj, SelfLink)
        self.assertEqual(obj.self, self.self)
        self.assertRaises(TypeError, SelfLink.from_json_str, self.bad_json1)
        self.assertRaises(TypeError, SelfLink.from_json_str, self.bad_json2)
        XLOGGER.debug("test_SelfLink_from_json_str Successful")

class ReferenceByIdTest(unittest.TestCase):
    """Collection of unit tests cases for the ReferenceById class
    """

    def setUp(self):
        XLOGGER.debug("ReferenceByIdTest.setUp")
        self.id = "/api/xm/1/people/84a6dde7-82ad-4e64-9f4d-3b9001ad60de"
        self.id_json_str = ('{"id": "%s"}')%(self.id)

    def tearDown(self):
        XLOGGER.debug("ReferenceByIdTest.tearDown")

    def test_ReferenceById(self):
        XLOGGER.debug("Start test_ReferenceById")
        obj = ReferenceById(self.id)
        self.assertIsInstance(obj, ReferenceById)
        self.assertEqual(obj.id, self.id)
        XLOGGER.debug("test_ReferenceById Successful")

    def test_ReferenceById_from_json_obj(self):
        XLOGGER.debug("Start test_ReferenceById_from_json_obj")
        json_obj = json.loads(self.id_json_str)
        obj = ReferenceById.from_json_obj(json_obj)
        self.assertIsInstance(obj, ReferenceById)
        self.assertEqual(obj.id, self.id)
        XLOGGER.debug("test_ReferenceById_from_json_obj Successful")

    def test_ReferenceById_from_json_str(self):
        XLOGGER.debug("Start test_ReferenceById_from_json_str")
        obj = ReferenceById.from_json_str(self.id_json_str)
        self.assertIsInstance(obj, ReferenceById)
        self.assertEqual(obj.id, self.id)
        XLOGGER.debug("test_ReferenceById_from_json_str Successful")

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

    def tearDown(self):
        XLOGGER.debug("ReferenceByIdAndSelfLinkTest.tearDown")

    def test_ReferenceByIdAndSelfLink(self):
        XLOGGER.debug("Start test_ReferenceByIdAndSelfLink")
        obj = ReferenceByIdAndSelfLink(self.id, self.links)
        self.assertIsInstance(obj, ReferenceByIdAndSelfLink)
        self.assertEqual(obj.id, self.id)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links, self.links)
        XLOGGER.debug("test_ReferenceByIdAndSelfLink Successful")

    def test_ReferenceByIdAndSelfLink_from_json_obj(self):
        XLOGGER.debug("Start test_ReferenceByIdAndSelfLink_from_json_obj")
        json_obj = json.loads(self.id_json_str)
        obj = ReferenceByIdAndSelfLink.from_json_obj(json_obj)
        self.assertIsInstance(obj, ReferenceByIdAndSelfLink)
        self.assertEqual(obj.id, self.id)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links.self, self.links.self)
        XLOGGER.debug("test_ReferenceByIdAndSelfLink_from_json_obj Successful")

    def test_ReferenceByIdAndSelfLink_from_json_str(self):
        XLOGGER.debug("Start test_ReferenceByIdAndSelfLink_from_json_str")
        obj = ReferenceByIdAndSelfLink.from_json_str(self.id_json_str)
        self.assertIsInstance(obj, ReferenceByIdAndSelfLink)
        self.assertEqual(obj.id, self.id)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links.self, self.links.self)
        XLOGGER.debug("test_ReferenceByIdAndSelfLink_from_json_str Successful")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
