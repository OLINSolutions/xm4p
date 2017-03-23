#!/usr/bin/env python3
# encoding: utf-8
"""Unit tests for xmatters.common.
"""

import json
import logging
import sys
import unittest

from xmatters import XmattersBase
from xmatters import XmattersJSONEncoder
from xmatters import XmattersList

from tests import _LOG_FILENAME
from tests import _LOG_LEVEL

XLOGGER = logging.getLogger('xlogger')
XLOGGER.level = _LOG_LEVEL
XSTREAM_HANDLER = logging.StreamHandler(sys.stdout)
XLOGGER.addHandler(XSTREAM_HANDLER)
XFILE_HANDLER = logging.FileHandler(_LOG_FILENAME)
XLOGGER.addHandler(XFILE_HANDLER)

# pylint: disable=missing-docstring, invalid-name, no-member

class ErrorTest(XmattersBase):
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


class XmattersListTest(unittest.TestCase):
    """Collection of unit tests cases for the Error class
    """

    class TestList(XmattersList):
        base_class = ErrorTest

    class BadTestList1(XmattersList):
        pass

    class BadTestList2(XmattersList):
        base_class = object

    def setUp(self):
        XLOGGER.info("XLOGGER.info XmattersListTest.setUp")
        self.err = []
        self.err.append(ErrorTest(
            404, "Not Found",
            "Could not find a person with id 0313142d3-4703-a90e-36cc5f5f6209"))
        self.err.append(ErrorTest(
            200, "OK",
            "Found a person with id 0313142d3-4703-a90e-36cc5f5f6209"))
        self.err.append(ErrorTest(
            202, "Submitted",
            "Submitted search for person id 0313142d3-4703-a90e-36cc5f5f6209"))
        self.err_json_str = []
        self.err_json = []
        self.err_json_str.append((
            '{"code":%d,"reason":"%s","message":"%s"}')%(
            404, "Not Found",
            "Could not find a person with id 0313142d3-4703-a90e-36cc5f5f6209"))
        self.err_json.append(ErrorTest.from_json_str(self.err_json_str[0]))
        self.err_json_str.append((
            '{"code":%d,"reason":"%s","message":"%s"}')%(
            200, "OK",
            "Found a person with id 0313142d3-4703-a90e-36cc5f5f6209"))
        self.err_json.append(ErrorTest.from_json_str(self.err_json_str[1]))
        self.err_json_str.append((
            '{"code":%d,"reason":"%s","message":"%s"}')%(
            202, "Submitted",
            "Submitted search for person id 0313142d3-4703-a90e-36cc5f5f6209"))
        self.err_json.append(ErrorTest.from_json_str(self.err_json_str[2]))
        self.err_json_str1 = '[%s]'%(','.join(self.err_json_str))

    def tearDown(self):
        XLOGGER.debug("XmattersListTest.tearDown")

    def test_TestList(self):
        XLOGGER.debug("XmattersListTest.test_TestList: Start")
        tlobj = XmattersListTest.TestList.from_json_str(self.err_json_str1)
        self.assertIsInstance(tlobj, XmattersListTest.TestList)
        self.assertEqual(len(tlobj), 3)
        for tl in range(3):
            self.assertIsInstance(tlobj[tl], ErrorTest)
            XLOGGER.debug(
                "test_TestList: tlobj[%d]=%s, Equality is %s",
                tl, str(tlobj[tl]), (tlobj[tl] == self.err[tl]))
            self.assertEqual(tlobj[tl], self.err[tl])
            XLOGGER.debug(
                "test_TestList: tlobj[%d].json: %s",
                tl, tlobj[tl].json)
            self.assertEqual(tlobj[tl].json, self.err_json_str[tl])
            XLOGGER.debug(
                "test_TestList: json.dumps(tlobj[%d]): %s",
                tl,
                json.dumps(
                    tlobj[tl], separators=(',', ':'), cls=XmattersJSONEncoder))
        self.assertRaises(
            TypeError, XmattersListTest.BadTestList1.from_json_str,
            self.err_json_str1)
        self.assertRaises(
            TypeError, XmattersListTest.BadTestList2.from_json_str,
            self.err_json_str1)
        XLOGGER.debug("ErrorTest.test_TestList: Success")

if __name__ == "__main__":
    # sys.argv = ['', 'XmattersListTest.test_TestList']
    unittest.main()
