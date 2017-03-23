#!/usr/bin/env python3
# encoding: utf-8
"""Unit tests for xmatters.events.
"""

import json
import logging
import sys
import unittest

from xmatters import Conference
from xmatters import ConferenceHostType
from xmatters import Event
from xmatters import EventPriority
from xmatters import EventStatus
from xmatters import FormReference
from xmatters import RecipientList
from xmatters import RecipientPagination
from xmatters import ResponseAction
from xmatters import ResponseContribution
from xmatters import ResponseOption
from xmatters import ResponseOptionList
from xmatters import ResponseOptionPagination

from tests import _LOG_FILENAME
from tests import _LOG_LEVEL

XLOGGER = logging.getLogger('xlogger')
XLOGGER.level = _LOG_LEVEL
XSTREAM_HANDLER = logging.StreamHandler(sys.stdout)
XLOGGER.addHandler(XSTREAM_HANDLER)
XFILE_HANDLER = logging.FileHandler(_LOG_FILENAME)
XLOGGER.addHandler(XFILE_HANDLER)

# pylint: disable=missing-docstring, invalid-name, no-member
# pylint: disable=too-many-instance-attributes, too-many-lines

class ConferenceTest(unittest.TestCase):
    """Collection of unit tests cases for the Conference class
    """

    def setUp(self):
        XLOGGER.debug("ConferenceTest.setUp")
        self.bridge_id = "67955226"
        self.type = ConferenceHostType.BRIDGE
        self.json_str = ('{"bridgeId":"%s","type":"%s"}'
            )%(self.bridge_id, self.type.value)
        self.bad_json1 = ('{"bridgeId":"%s"}')%(self.bridge_id)
        self.bad_json2 = ('{"type":"%s"}')%(self.type.value)
        self.bad_json3 = ('{"bridgeId":%d,"type":"%s"}')%(0, self.type.value)
        self.bad_json4 = ('{"bridgeId":"%s","type":%d}')%(self.bridge_id, 0,)

    def tearDown(self):
        XLOGGER.debug("ConferenceTest.tearDown")

    def test_class(self):
        XLOGGER.debug("test_class: Start")
        obj = Conference(self.bridge_id, self.type)
        self.assertIsInstance(obj, Conference)
        self.assertEqual(obj.bridge_id, self.bridge_id)
        self.assertEqual(obj.type, self.type)
        self.assertRaises(TypeError, Conference, "")
        self.assertRaises(TypeError, Conference, "", "")
        self.assertRaises(TypeError, Conference, 0, "")
        self.assertRaises(TypeError, Conference, "", 0)
        XLOGGER.debug("test_class: Success")

    def test_from_json_obj(self):
        XLOGGER.debug("test_from_json_obj: Start")
        json_obj = json.loads(self.json_str)
        obj = Conference.from_json_obj(json_obj)
        self.assertIsInstance(obj, Conference)
        XLOGGER.debug(
            "test_from_json_obj: Success")

    def test_from_json_str(self):
        XLOGGER.debug(
            "test_from_json_str: Start")
        obj = Conference.from_json_str(self.json_str)
        self.assertIsInstance(obj, Conference)
        obj1 = Conference(self.bridge_id, self.type)
        self.assertEqual(obj, obj1)
        self.assertRaises(TypeError, Conference.from_json_str, self.bad_json1)
        self.assertRaises(TypeError, Conference.from_json_str, self.bad_json2)
        self.assertRaises(TypeError, Conference.from_json_str, self.bad_json3)
        self.assertRaises(TypeError, Conference.from_json_str, self.bad_json4)
        XLOGGER.debug(
            "test_from_json_str: Success")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
