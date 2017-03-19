#!/usr/bin/env python3
# encoding: utf-8
"""Unit tests for EventAuditReport.xmatters.recipients.
"""

import json
import logging
import sys
import unittest

from xmatters import DynamicTeam
from xmatters import PersonReference
from xmatters import Recipient
from xmatters import RecipientPointer
from xmatters import RecipientType
from xmatters import RecipientStatus
from xmatters import SelfLink

from . import _log_filename
from . import _log_level

XLOGGER = logging.getLogger('xlogger')
XLOGGER.level = _log_level
XSTREAM_HANDLER = logging.StreamHandler(sys.stdout)
XLOGGER.addHandler(XSTREAM_HANDLER)
XFILE_HANDLER = logging.FileHandler(_log_filename)
XLOGGER.addHandler(XFILE_HANDLER)

# pylint: disable=missing-docstring, invalid-name, no-member
# pylint: disable=too-many-instance-attributes

class RecipientPointerTest(unittest.TestCase):
    """Collection of unit tests cases for the RecipientPointer class
    """

    def setUp(self):
        XLOGGER.debug("RecipientPointerTest.setUp")
        self.id_p = "438e9245-b32d-445f-916bd3e07932c892"
        self.recipient_type_p = "PERSON"
        self.rp_p_json_str = (
            '{"id": "%s", "recipientType": "%s"}'
            )%(self.id_p, self.recipient_type_p)
        self.id_g = "f0c572a8-45ec-fe23-289c-df749cf19a5e"
        self.recipient_type_g = "GROUP"
        self.rp_g_json_str = (
            '{"id": "%s", "recipientType": "%s"}'
            )%(self.id_g, self.recipient_type_g)
        self.id_d = "8f2d98ed-eaa9-4b0b-b366-c1db06b27e1f"
        self.recipient_type_d = "DEVICE"
        self.rp_d_json_str = (
            '{"id": "%s", "recipientType": "%s"}'
            )%(self.id_d, self.recipient_type_d)
        self.bad_json_str1 = (
            '{"recipientType": "%s"}'
            )%(self.recipient_type_d)
        self.bad_json_str2 = (
            '{"id": %d, "recipientType": "%s"}'
            )%(0, self.recipient_type_d)

    def tearDown(self):
        XLOGGER.debug("RecipientPointerTest.tearDown")

    def test_RecipientPointer(self):
        XLOGGER.debug("RecipientPointerTest.test_RecipientPointer: Start")
        obj = RecipientPointer(self.id_p, self.recipient_type_p)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_p)
        self.assertEqual(obj.recipient_type, self.recipient_type_p)
        obj = RecipientPointer(self.id_g, self.recipient_type_g)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_g)
        self.assertEqual(obj.recipient_type, self.recipient_type_g)
        obj = RecipientPointer(self.id_d, self.recipient_type_d)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_d)
        self.assertEqual(obj.recipient_type, self.recipient_type_d)
        self.assertRaises(TypeError, RecipientPointer, 0)
        self.assertRaises(TypeError, RecipientPointer, self.recipient_type_d, 0)
        XLOGGER.debug("RecipientPointerTest.test_RecipientPointer: Success")

    def test_RecipientPointer_from_json_obj(self):
        XLOGGER.debug(
            "RecipientPointerTest.test_RecipientPointer_from_json_obj: Start")
        json_obj = json.loads(self.rp_p_json_str)
        obj = RecipientPointer.from_json_obj(json_obj)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_p)
        self.assertEqual(obj.recipient_type, self.recipient_type_p)
        json_obj = json.loads(self.rp_g_json_str)
        obj = RecipientPointer.from_json_obj(json_obj)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_g)
        self.assertEqual(obj.recipient_type, self.recipient_type_g)
        json_obj = json.loads(self.rp_d_json_str)
        obj = RecipientPointer.from_json_obj(json_obj)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_d)
        self.assertEqual(obj.recipient_type, self.recipient_type_d)
        XLOGGER.debug(
            "RecipientPointerTest.test_RecipientPointer_from_json_obj: Success")

    def test_RecipientPointer_from_json_str(self):
        XLOGGER.debug(
            "RecipientPointerTest.test_RecipientPointer_from_json_str: Start")
        obj = RecipientPointer.from_json_str(self.rp_p_json_str)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_p)
        self.assertEqual(obj.recipient_type, self.recipient_type_p)
        obj = RecipientPointer.from_json_str(self.rp_g_json_str)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_g)
        self.assertEqual(obj.recipient_type, self.recipient_type_g)
        obj = RecipientPointer.from_json_str(self.rp_d_json_str)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_d)
        self.assertEqual(obj.recipient_type, self.recipient_type_d)
        self.assertRaises(TypeError, RecipientPointer.from_json_str, self.bad_json_str1)
        self.assertRaises(TypeError, RecipientPointer.from_json_str, self.bad_json_str2)
        XLOGGER.debug(
            "RecipientPointerTest.test_RecipientPointer_from_json_str: Success")

class PersonReferenceTest(unittest.TestCase):
    """Collection of unit tests cases for the PersonReference class
    """

    def setUp(self):
        XLOGGER.debug("PersonReferenceTest.setUp")
        self.id = "481086d8-357a-4279-b7d5-d7dce48fcd12"
        self.target_name = "mmcbride"
        self.self = "/api/xm/1/people/481086d8-357a-4279-b7d5-d7dce48fcd12"
        self.links_json_str = ('{"self": "%s"}')%(self.self)
        self.links =SelfLink.from_json_str(self.links_json_str)
        self.pr_json_str = (
            '{"id": "%s", "targetName": "%s", "links": %s}'
            )%(self.id, self.target_name, self.links_json_str)
        self.bad_json_str1 = (
            '{"id": "%s", "targetName": "%s"}'
            )%(self.id, self.target_name)
        self.bad_json_str2 = (
            '{"id": "%s", "links": %s}'
            )%(self.id, self.links_json_str)
        self.bad_json_str3 = (
            '{"targetName": "%s", "links": %s}'
            )%(self.target_name, self.links_json_str)
        self.bad_json_str4 = (
            '{"id": %d, "targetName": "%s", "links": %s}'
            )%(0, self.target_name, self.links_json_str)
        self.bad_json_str5 = (
            '{"id": "%s", "targetName": %d, "links": %s}'
            )%(self.id, 0, self.links_json_str)
        self.bad_json_str6 = (
            '{"id": "%s", "targetName": "%s", "links": %d}'
            )%(self.id, self.target_name, 0)

    def tearDown(self):
        XLOGGER.debug("PersonReferenceTest.tearDown")

    def test_PersonReference(self):
        XLOGGER.debug("PersonReferenceTest.test_PersonReference: Start")
        obj = PersonReference(self.id, self.target_name, self.links)
        self.assertIsInstance(obj, PersonReference)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links, self.links)
        self.assertRaises(TypeError, PersonReference, self.id, self.target_name)
        self.assertRaises(TypeError, PersonReference, self.id)
        self.assertRaises(TypeError, PersonReference, 0, self.target_name, self.links)
        self.assertRaises(TypeError, PersonReference, self.id, 0, self.links)
        self.assertRaises(TypeError, PersonReference, self.id, self.target_name, 0)
        XLOGGER.debug(
            "PersonReferenceTest.test_PersonReference: Success")

    def test_PersonReference_from_json_obj(self):
        XLOGGER.debug(
            "PersonReferenceTest.test_PersonReference_from_json_obj: Start")
        json_obj = json.loads(self.pr_json_str)
        obj = PersonReference.from_json_obj(json_obj)
        self.assertIsInstance(obj, PersonReference)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links.self, self.links.self)
        XLOGGER.debug(
            "PersonReferenceTest.test_PersonReference_from_json_obj: Success")

    def test_PersonReference_from_json_str(self):
        XLOGGER.debug(
            "PersonReferenceTest.test_PersonReference_from_json_str: Start")
        obj = PersonReference.from_json_str(self.pr_json_str)
        self.assertIsInstance(obj, PersonReference)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links.self, self.links.self)
        self.assertRaises(TypeError, PersonReference.from_json_str,
            self.bad_json_str1)
        self.assertRaises(TypeError, PersonReference.from_json_str,
            self.bad_json_str2)
        self.assertRaises(TypeError, PersonReference.from_json_str,
            self.bad_json_str3)
        self.assertRaises(TypeError, PersonReference.from_json_str,
            self.bad_json_str4)
        self.assertRaises(TypeError, PersonReference.from_json_str,
            self.bad_json_str5)
        self.assertRaises(TypeError, PersonReference.from_json_str,
            self.bad_json_str6)
        XLOGGER.debug(
            "PersonReferenceTest.test_PersonReference_from_json_str: Success")

class RecipientTest(unittest.TestCase):
    """Collection of unit tests cases for the PersonReference class
    """

    def setUp(self):
        XLOGGER.debug("RecipientTest.setUp")
        self.id = "481086d8-357a-4279-b7d5-d7dce48fcd12"
        self.target_name = "mmcbride"
        self.recipient_type = RecipientType.GROUP
        self.externallyOwnedF = False
        self.externallyOwnedT = True
        self.externalKeyT = (
            "%s%s")%(self.recipient_type.value, self.target_name)
        self.externalKeyF = None
        self.locked_list = ["externallyOwned", "externalKey"]
        self.locked = (','.join('"' + itm + '"' for itm in self.locked_list))
        self.status = RecipientStatus.ACTIVE
        self.self = "/api/xm/1/people/9407eb2e-8eb2-43d9-88a8-875237af941d"
        self.links_json_str = ('{"self": "%s"}')%(self.self)
        self.links =SelfLink.from_json_str(self.links_json_str)
        self.pr_json_str1 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externallyOwnedT).lower(), self.externalKeyT,
            self.locked, self.status.value, self.links_json_str)
        XLOGGER.debug(
            "RecipientTest.setUp - pr_json_str1: %s", self.pr_json_str1)
        self.pr_json_str2 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externallyOwnedF).lower())
        XLOGGER.debug(
            "RecipientTest.setUp - pr_json_str2: %s", self.pr_json_str2)
        self.bad_json1 = (
            '{"id": 0, "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.target_name, self.recipient_type.value,
            str(self.externallyOwnedT).lower(), self.externalKeyT,
            self.locked, self.status.value, self.links_json_str)
        self.bad_json2 = (
            '{"id": "%s", "targetName": 0, "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.id, self.recipient_type.value,
            str(self.externallyOwnedT).lower(), self.externalKeyT,
            self.locked, self.status.value, self.links_json_str)
        self.bad_json3 = (
            '{"id": "%s", "targetName": "%s", "recipientType": 0, '
            '"externallyOwned": %s, "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.id, self.target_name,
            str(self.externallyOwnedT).lower(), self.externalKeyT,
            self.locked, self.status.value, self.links_json_str)
        self.bad_json4 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": "0", "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externallyOwnedT).lower(),
            self.locked, self.status.value, self.links_json_str)
        self.bad_json5 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": 0, "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externallyOwnedT).lower(),
            self.locked, self.status.value, self.links_json_str)
        self.bad_json6 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": "%s", "locked": 0, '
            '"status": "%s", "links": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externallyOwnedT).lower(), self.externalKeyT,
            self.status.value, self.links_json_str)
        self.bad_json7 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": "%s", "locked": [%s], '
            '"status": 0, "links": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externallyOwnedT).lower(), self.externalKeyT,
            self.locked, self.links_json_str)
        self.bad_json8 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": 0}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externallyOwnedT).lower(), self.externalKeyT,
            self.locked, self.status.value)
        self.bad_json9 = '{}'

    def tearDown(self):
        XLOGGER.debug("RecipientTest.tearDown")

    def test_Recipient(self):
        XLOGGER.debug("RecipientTest.test_Recipient: Start")
        obj = Recipient(
            self.id, self.target_name, self.recipient_type,
            self.externallyOwnedT, self.externalKeyT, self.locked_list,
            self.status, self.links)
        self.obj1 = obj
        self.assertIsInstance(obj, Recipient)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.recipient_type, RecipientType)
        self.assertEqual(obj.recipient_type, self.recipient_type)
        self.assertEqual(obj.recipient_type.value, self.recipient_type.value)
        self.assertEqual(obj.externally_owned, self.externallyOwnedT)
        self.assertEqual(obj.external_key, self.externalKeyT)
        self.assertEqual(obj.locked, self.locked_list)
        self.assertIsInstance(obj.status, RecipientStatus)
        self.assertEqual(obj.status, self.status)
        self.assertEqual(obj.status.value, self.status.value)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links, self.links)
        obj = Recipient(
            self.id, self.target_name, self.recipient_type,
            self.externallyOwnedF)
        self.obj2 = obj
        self.assertIsInstance(obj, Recipient)
        self.assertRaises(TypeError, Recipient, self.id, self.target_name,
            self.recipient_type)
        self.assertRaises(TypeError, Recipient, self.id, self.target_name)
        self.assertRaises(TypeError, Recipient, self.id)
        self.assertRaises(TypeError, Recipient)
        self.assertRaises(TypeError, Recipient, 0, self.target_name, 
            self.recipient_type, self.externallyOwnedF)
        self.assertRaises(TypeError, Recipient, self.id, 0, 
            self.recipient_type, self.externallyOwnedF)
        self.assertRaises(TypeError, Recipient, self.id, self.target_name, 
            0, self.externallyOwnedF)
        self.assertRaises(TypeError, Recipient, self.id, self.target_name, 
            self.recipient_type, self.links)
        XLOGGER.debug(
            "RecipientTest.test_Recipient: Success")

    def test_Recipient_from_json_obj(self):
        XLOGGER.debug(
            "RecipientTest.test_Recipient_from_json_obj: Start")
        json_obj = json.loads(self.pr_json_str1)
        obj = Recipient.from_json_obj(json_obj)
        self.assertIsInstance(obj, Recipient)
        XLOGGER.debug(
            "RecipientTest.test_Recipient_from_json_obj: Success")

    def test_Recipient_from_json_str(self):
        XLOGGER.debug(
            "RecipientTest.test_Recipient_from_json_str: Start")
        obj = Recipient.from_json_str(self.pr_json_str1)
        self.assertIsInstance(obj, Recipient)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.recipient_type, RecipientType)
        self.assertEqual(obj.recipient_type, self.recipient_type)
        self.assertEqual(obj.recipient_type.value, self.recipient_type.value)
        self.assertEqual(obj.externally_owned, self.externallyOwnedT)
        self.assertEqual(obj.external_key, self.externalKeyT)
        self.assertEqual(obj.locked, self.locked_list)
        self.assertIsInstance(obj.status, RecipientStatus)
        self.assertEqual(obj.status, self.status)
        self.assertEqual(obj.status.value, self.status.value)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links.self, self.links.self)
        self.assertRaises(TypeError, Recipient.from_json_str, self.bad_json1)
        self.assertRaises(TypeError, Recipient.from_json_str, self.bad_json2)
        self.assertRaises(TypeError, Recipient.from_json_str, self.bad_json3)
        self.assertRaises(TypeError, Recipient.from_json_str, self.bad_json4)
        self.assertRaises(TypeError, Recipient.from_json_str, self.bad_json5)
        self.assertRaises(TypeError, Recipient.from_json_str, self.bad_json6)
        self.assertRaises(TypeError, Recipient.from_json_str, self.bad_json7)
        self.assertRaises(TypeError, Recipient.from_json_str, self.bad_json8)
        self.assertRaises(TypeError, Recipient.from_json_str, self.bad_json9)
        obj = Recipient.from_json_str(self.pr_json_str2)
        self.assertIsInstance(obj, Recipient)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.recipient_type, RecipientType)
        self.assertEqual(obj.recipient_type, self.recipient_type)
        self.assertEqual(obj.recipient_type.value, self.recipient_type.value)
        self.assertEqual(obj.externally_owned, self.externallyOwnedF)
        self.assertEqual(obj.external_key, self.externalKeyF)
        XLOGGER.debug(
            "RecipientTest.test_Recipient_from_json_str: Success")

class DynamicTeamTest(unittest.TestCase):
    """Collection of unit tests cases for the DynamicTeam class
    """

    def setUp(self):
        XLOGGER.debug("DynamicTeamTest.setUp")
        self.id = "481086d8-357a-4279-b7d5-d7dce48fcd12"
        self.target_name = "mmcbride"
        self.recipient_type = RecipientType.GROUP
        self.externallyOwnedF = False
        self.externallyOwnedT = True
        self.useEmergencyDevice = True
        self.externalKeyT = (
            "%s%s")%(self.recipient_type.value, self.target_name)
        self.externalKeyF = None
        self.locked_list = ["externallyOwned", "externalKey"]
        self.locked = (','.join('"' + itm + '"' for itm in self.locked_list))
        self.status = RecipientStatus.ACTIVE
        self.self = "/api/xm/1/people/9407eb2e-8eb2-43d9-88a8-875237af941d"
        self.links_json_str = ('{"self": "%s"}')%(self.self)
        self.links =SelfLink.from_json_str(self.links_json_str)
        self.pr_json_str1 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "useEmergencyDevice: %s, '
            '"externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externallyOwnedT).lower(),
            str(self.useEmergencyDevice).lower(),
            self.externalKeyT, self.locked, self.status.value, 
            self.links_json_str)
        XLOGGER.debug(
            "DynamicTeamTest.setUp - pr_json_str1: %s", self.pr_json_str1)
        self.pr_json_str2 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "useEmergencyDevice: %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externallyOwnedF).lower(),
            str(self.useEmergencyDevice).lower())
        XLOGGER.debug(
            "RecipientTest.setUp - pr_json_str2: %s", self.pr_json_str2)
        self.bad_json1 = (
            '{"id": 0, "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.target_name, self.recipient_type.value,
            str(self.externallyOwnedT).lower(), self.externalKeyT,
            self.locked, self.status.value, self.links_json_str)
        self.bad_json2 = (
            '{"id": "%s", "targetName": 0, "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.id, self.recipient_type.value,
            str(self.externallyOwnedT).lower(), self.externalKeyT,
            self.locked, self.status.value, self.links_json_str)
        self.bad_json3 = (
            '{"id": "%s", "targetName": "%s", "recipientType": 0, '
            '"externallyOwned": %s, "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.id, self.target_name,
            str(self.externallyOwnedT).lower(), self.externalKeyT,
            self.locked, self.status.value, self.links_json_str)
        self.bad_json4 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": "0", "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externallyOwnedT).lower(),
            self.locked, self.status.value, self.links_json_str)
        self.bad_json5 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": 0, "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externallyOwnedT).lower(),
            self.locked, self.status.value, self.links_json_str)
        self.bad_json6 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": "%s", "locked": 0, '
            '"status": "%s", "links": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externallyOwnedT).lower(), self.externalKeyT,
            self.status.value, self.links_json_str)
        self.bad_json7 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": "%s", "locked": [%s], '
            '"status": 0, "links": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externallyOwnedT).lower(), self.externalKeyT,
            self.locked, self.links_json_str)
        self.bad_json8 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": 0}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externallyOwnedT).lower(), self.externalKeyT,
            self.locked, self.status.value)
        self.bad_json9 = '{}'


    def tearDown(self):
        XLOGGER.debug("DynamicTeamTest.tearDown")

    def test_DynamicTeam(self):
        XLOGGER.debug("DynamicTeamTest.test_DynamicTeam: Start")
        obj = DynamicTeam(
            self.id, self.target_name, self.recipient_type,
            self.externallyOwnedT, self.useEmergencyDevice, self.externalKeyT,
            self.locked_list, self.status, self.links)
        self.obj1 = obj
        self.assertIsInstance(obj, DynamicTeam)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.recipient_type, RecipientType)
        self.assertEqual(obj.recipient_type, self.recipient_type)
        self.assertEqual(obj.recipient_type.value, self.recipient_type.value)
        self.assertEqual(obj.externally_owned, self.externallyOwnedT)
        self.assertEqual(obj.use_emergency_device, self.useEmergencyDevice)
        self.assertEqual(obj.external_key, self.externalKeyT)
        self.assertEqual(obj.locked, self.locked_list)
        self.assertIsInstance(obj.status, RecipientStatus)
        self.assertEqual(obj.status, self.status)
        self.assertEqual(obj.status.value, self.status.value)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links, self.links)
        obj = DynamicTeam(
            self.id, self.target_name, self.recipient_type,
            self.externallyOwnedF, self.useEmergencyDevice)
        self.obj2 = obj
        self.assertIsInstance(obj, DynamicTeam)
        self.assertRaises(TypeError, DynamicTeam, self.id, self.target_name,
            self.recipient_type)
        self.assertRaises(TypeError, DynamicTeam, self.id, self.target_name)
        self.assertRaises(TypeError, DynamicTeam, self.id)
        self.assertRaises(TypeError, DynamicTeam)
        self.assertRaises(TypeError, DynamicTeam, 0, self.target_name, 
            self.recipient_type, self.externallyOwnedF)
        self.assertRaises(TypeError, DynamicTeam, self.id, 0, 
            self.recipient_type, self.externallyOwnedF)
        self.assertRaises(TypeError, DynamicTeam, self.id, self.target_name, 
            0, self.externallyOwnedF)
        self.assertRaises(TypeError, DynamicTeam, self.id, self.target_name, 
            self.recipient_type, self.links)
        XLOGGER.debug(
            "DynamicTeamTest.test_DynamicTeam: Success")

    def test_DynamicTeam_from_json_obj(self):
        XLOGGER.debug(
            "DynamicTeamTest.test_DynamicTeam_from_json_obj: Start")
        json_obj = json.loads(self.pr_json_str1)
        obj = DynamicTeam.from_json_obj(json_obj)
        self.assertIsInstance(obj, DynamicTeam)
        XLOGGER.debug(
            "DynamicTeamTest.test_DynamicTeam_from_json_obj: Success")

    def test_DynamicTeam_from_json_str(self):
        XLOGGER.debug(
            "DynamicTeamTest.test_DynamicTeam_from_json_str: Start")
        obj = DynamicTeam.from_json_str(self.pr_json_str1)
        self.assertIsInstance(obj, DynamicTeam)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.recipient_type, RecipientType)
        self.assertEqual(obj.recipient_type, self.recipient_type)
        self.assertEqual(obj.recipient_type.value, self.recipient_type.value)
        self.assertEqual(obj.externally_owned, self.externallyOwnedT)
        self.assertEqual(obj.external_key, self.externalKeyT)
        self.assertEqual(obj.locked, self.locked_list)
        self.assertIsInstance(obj.status, RecipientStatus)
        self.assertEqual(obj.status, self.status)
        self.assertEqual(obj.status.value, self.status.value)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links.self, self.links.self)
        self.assertRaises(
            TypeError, DynamicTeam.from_json_str, self.bad_json1)
        self.assertRaises(
            TypeError, DynamicTeam.from_json_str, self.bad_json2)
        self.assertRaises(
            TypeError, DynamicTeam.from_json_str, self.bad_json3)
        self.assertRaises(
            TypeError, DynamicTeam.from_json_str, self.bad_json4)
        self.assertRaises(
            TypeError, DynamicTeam.from_json_str, self.bad_json5)
        self.assertRaises(
            TypeError, DynamicTeam.from_json_str, self.bad_json6)
        self.assertRaises(
            TypeError, DynamicTeam.from_json_str, self.bad_json7)
        self.assertRaises(
            TypeError, DynamicTeam.from_json_str, self.bad_json8)
        self.assertRaises(
            TypeError, DynamicTeam.from_json_str, self.bad_json9)
        obj = DynamicTeam.from_json_str(self.pr_json_str2)
        self.assertIsInstance(obj, DynamicTeam)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.recipient_type, RecipientType)
        self.assertEqual(obj.recipient_type, self.recipient_type)
        self.assertEqual(obj.recipient_type.value, self.recipient_type.value)
        self.assertEqual(obj.externally_owned, self.externallyOwnedF)
        self.assertEqual(obj.external_key, self.externalKeyF)
        XLOGGER.debug(
            "DynamicTeamTest.test_DynamicTeam_from_json_str: Success")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
