#!/usr/bin/env python3
# encoding: utf-8
"""Unit tests for xmatters.recipients.
"""

import json
import logging
import sys
import unittest

from xmatters import DynamicTeam
from xmatters import Group
from xmatters import PersonReference
from xmatters import Recipient
from xmatters import RecipientPointer
from xmatters import RecipientType
from xmatters import RecipientStatus
from xmatters import ReferenceByIdAndSelfLink
from xmatters import RolePagination
from xmatters import Person
from xmatters import SelfLink

from . import _LOG_FILENAME
from . import _LOG_LEVEL

XLOGGER = logging.getLogger('xlogger')
XLOGGER.level = _LOG_LEVEL
XSTREAM_HANDLER = logging.StreamHandler(sys.stdout)
XLOGGER.addHandler(XSTREAM_HANDLER)
XFILE_HANDLER = logging.FileHandler(_LOG_FILENAME)
XLOGGER.addHandler(XFILE_HANDLER)

# pylint: disable=missing-docstring, invalid-name, no-member
# pylint: disable=too-many-instance-attributes, too-many-lines

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
        self.bad_json_str1 = (
            '{"recipientType": "%s"}'
            )%(self.recipient_type_p)
        self.bad_json_str2 = (
            '{"id": %d, "recipientType": "%s"}'
            )%(0, self.recipient_type_p)

    def tearDown(self):
        XLOGGER.debug("RecipientPointerTest.tearDown")

    def test_RecipientPointer(self):
        XLOGGER.debug("RecipientPointerTest.test_RecipientPointer: Start")
        obj = RecipientPointer(self.id_p, self.recipient_type_p)
        self.assertIsInstance(obj, RecipientPointer)
        self.assertEqual(obj.id, self.id_p)
        self.assertEqual(obj.recipient_type, self.recipient_type_p)
        self.assertRaises(TypeError, RecipientPointer, 0)
        self.assertRaises(TypeError, RecipientPointer, self.recipient_type_p, 0)
        XLOGGER.debug("RecipientPointerTest.test_RecipientPointer: Success")

    def test_RecipientPointer_from_json_obj(self):
        XLOGGER.debug(
            "RecipientPointerTest.test_RecipientPointer_from_json_obj: Start")
        json_obj = json.loads(self.rp_p_json_str)
        obj = RecipientPointer.from_json_obj(json_obj)
        self.assertIsInstance(obj, RecipientPointer)
        obj1 = RecipientPointer(self.id_p, self.recipient_type_p)
        self.assertEqual(obj, obj1)
        XLOGGER.debug(
            "RecipientPointerTest.test_RecipientPointer_from_json_obj: Success")

    def test_RecipientPointer_from_json_str(self):
        XLOGGER.debug(
            "RecipientPointerTest.test_RecipientPointer_from_json_str: Start")
        obj = RecipientPointer.from_json_str(self.rp_p_json_str)
        self.assertIsInstance(obj, RecipientPointer)
        obj1 = RecipientPointer(self.id_p, self.recipient_type_p)
        self.assertEqual(obj, obj1)
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
        self.externally_owned_f = False
        self.externally_owned_t = True
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
            str(self.externally_owned_t).lower(), self.externalKeyT,
            self.locked, self.status.value, self.links_json_str)
        XLOGGER.debug(
            "RecipientTest.setUp - pr_json_str1: %s", self.pr_json_str1)
        self.pr_json_str2 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_f).lower())
        XLOGGER.debug(
            "RecipientTest.setUp - pr_json_str2: %s", self.pr_json_str2)
        self.bad_json1 = (
            '{"id": 0, "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(), self.externalKeyT,
            self.locked, self.status.value, self.links_json_str)
        self.bad_json2 = (
            '{"id": "%s", "targetName": 0, "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.id, self.recipient_type.value,
            str(self.externally_owned_t).lower(), self.externalKeyT,
            self.locked, self.status.value, self.links_json_str)
        self.bad_json3 = (
            '{"id": "%s", "targetName": "%s", "recipientType": 0, '
            '"externallyOwned": %s, "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.id, self.target_name,
            str(self.externally_owned_t).lower(), self.externalKeyT,
            self.locked, self.status.value, self.links_json_str)
        self.bad_json4 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": "0", "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.locked, self.status.value, self.links_json_str)
        self.bad_json5 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": 0, "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.locked, self.status.value, self.links_json_str)
        self.bad_json6 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": "%s", "locked": 0, '
            '"status": "%s", "links": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(), self.externalKeyT,
            self.status.value, self.links_json_str)
        self.bad_json7 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": "%s", "locked": [%s], '
            '"status": 0, "links": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(), self.externalKeyT,
            self.locked, self.links_json_str)
        self.bad_json8 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": 0}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(), self.externalKeyT,
            self.locked, self.status.value)
        self.bad_json9 = '{}'
        self.obj1 = None
        self.obj2 = None

    def tearDown(self):
        XLOGGER.debug("RecipientTest.tearDown")

    def test_Recipient(self):
        XLOGGER.debug("RecipientTest.test_Recipient: Start")
        obj = Recipient(
            self.id, self.target_name, self.recipient_type,
            self.externally_owned_t, self.externalKeyT, self.locked_list,
            self.status, self.links)
        self.obj1 = obj
        self.assertIsInstance(obj, Recipient)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.recipient_type, RecipientType)
        self.assertEqual(obj.recipient_type, self.recipient_type)
        self.assertEqual(obj.recipient_type.value, self.recipient_type.value)
        self.assertEqual(obj.externally_owned, self.externally_owned_t)
        self.assertEqual(obj.external_key, self.externalKeyT)
        self.assertEqual(obj.locked, self.locked_list)
        self.assertIsInstance(obj.status, RecipientStatus)
        self.assertEqual(obj.status, self.status)
        self.assertEqual(obj.status.value, self.status.value)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links, self.links)
        obj = Recipient(
            self.id, self.target_name, self.recipient_type,
            self.externally_owned_f)
        self.obj2 = obj
        self.assertIsInstance(obj, Recipient)
        self.assertRaises(TypeError, Recipient, self.id, self.target_name,
            self.recipient_type)
        self.assertRaises(TypeError, Recipient, self.id, self.target_name)
        self.assertRaises(TypeError, Recipient, self.id)
        self.assertRaises(TypeError, Recipient)
        self.assertRaises(TypeError, Recipient, 0, self.target_name,
            self.recipient_type, self.externally_owned_f)
        self.assertRaises(TypeError, Recipient, self.id, 0,
            self.recipient_type, self.externally_owned_f)
        self.assertRaises(TypeError, Recipient, self.id, self.target_name,
            0, self.externally_owned_f)
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
        self.assertEqual(obj.externally_owned, self.externally_owned_t)
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
        self.assertEqual(obj.externally_owned, self.externally_owned_f)
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
        self.recipient_type = RecipientType.DYNAMIC_TEAM
        self.externally_owned_f = False
        self.externally_owned_t = True
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
            '"externallyOwned": %s, "useEmergencyDevice": %s, '
            '"externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            str(self.useEmergencyDevice).lower(),
            self.externalKeyT, self.locked, self.status.value,
            self.links_json_str)
        XLOGGER.debug(
            "DynamicTeamTest.setUp - pr_json_str1: %s", self.pr_json_str1)
        self.pr_json_str2 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "useEmergencyDevice": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_f).lower(),
            str(self.useEmergencyDevice).lower())
        XLOGGER.debug(
            "DynamicTeamTest.setUp - pr_json_str2: %s", self.pr_json_str2)
        self.bad_json1 = (
            '{"targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "useEmergencyDevice": %s}'
            )%(self.target_name, self.recipient_type.value,
            str(self.externally_owned_f).lower(),
            str(self.useEmergencyDevice).lower())
        self.bad_json2 = (
            '{"id": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "useEmergencyDevice": %s}'
            )%(self.id, self.recipient_type.value,
            str(self.externally_owned_f).lower(),
            str(self.useEmergencyDevice).lower())
        self.bad_json3 = (
            '{"id": "%s", "targetName": "%s", '
            '"externallyOwned": %s, "useEmergencyDevice": %s}'
            )%(self.id, self.target_name,
            str(self.externally_owned_f).lower(),
            str(self.useEmergencyDevice).lower())
        self.bad_json4 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"useEmergencyDevice": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.useEmergencyDevice).lower())
        self.bad_json5 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_f).lower())
        self.bad_json6 = (
            '{"id": 0, "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "useEmergencyDevice": %s}'
            )%(self.target_name, self.recipient_type.value,
            str(self.externally_owned_f).lower(),
            str(self.useEmergencyDevice).lower())
        self.bad_json7 = (
            '{"id": "%s", "targetName": 0, "recipientType": "%s", '
            '"externallyOwned": %s, "useEmergencyDevice": %s}'
            )%(self.id, self.recipient_type.value,
            str(self.externally_owned_f).lower(),
            str(self.useEmergencyDevice).lower())
        self.bad_json8 = (
            '{"id": "%s", "targetName": "%s", "recipientType": 0, '
            '"externallyOwned": %s, "useEmergencyDevice": %s}'
            )%(self.id, self.target_name,
            str(self.externally_owned_f).lower(),
            str(self.useEmergencyDevice).lower())
        self.bad_json9 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": "0", "useEmergencyDevice": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.useEmergencyDevice).lower())
        self.bad_json10 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "useEmergencyDevice": "0"}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_f).lower())
        self.bad_json11 = '{}'
        self.obj1 = None
        self.obj2 = None


    def tearDown(self):
        XLOGGER.debug("DynamicTeamTest.tearDown")

    def test_DynamicTeam(self):
        XLOGGER.debug("DynamicTeamTest.test_DynamicTeam: Start")
        obj = DynamicTeam(
            self.id, self.target_name, self.recipient_type,
            self.externally_owned_t, self.useEmergencyDevice, self.externalKeyT,
            self.locked_list, self.status, self.links)
        self.obj1 = obj
        self.assertIsInstance(obj, DynamicTeam)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.recipient_type, RecipientType)
        self.assertEqual(obj.recipient_type, self.recipient_type)
        self.assertEqual(obj.recipient_type.value, self.recipient_type.value)
        self.assertEqual(obj.externally_owned, self.externally_owned_t)
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
            self.externally_owned_f, self.useEmergencyDevice)
        self.obj2 = obj
        self.assertIsInstance(obj, DynamicTeam)
        self.assertRaises(TypeError, DynamicTeam, self.id, self.target_name,
            self.recipient_type)
        self.assertRaises(TypeError, DynamicTeam, self.id, self.target_name)
        self.assertRaises(TypeError, DynamicTeam, self.id)
        self.assertRaises(TypeError, DynamicTeam)
        self.assertRaises(TypeError, DynamicTeam, 0, self.target_name,
            self.recipient_type, self.externally_owned_f)
        self.assertRaises(TypeError, DynamicTeam, self.id, 0,
            self.recipient_type, self.externally_owned_f)
        self.assertRaises(TypeError, DynamicTeam, self.id, self.target_name,
            0, self.externally_owned_f)
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
        self.assertEqual(obj.externally_owned, self.externally_owned_t)
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
        self.assertRaises(AssertionError, self.assertRaises,
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
        self.assertRaises(
            TypeError, DynamicTeam.from_json_str, self.bad_json10)
        self.assertRaises(
            TypeError, DynamicTeam.from_json_str, self.bad_json11)
        obj = DynamicTeam.from_json_str(self.pr_json_str2)
        self.assertIsInstance(obj, DynamicTeam)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.recipient_type, RecipientType)
        self.assertEqual(obj.recipient_type, self.recipient_type)
        self.assertEqual(obj.recipient_type.value, self.recipient_type.value)
        self.assertEqual(obj.externally_owned, self.externally_owned_f)
        self.assertEqual(obj.external_key, self.externalKeyF)
        XLOGGER.debug(
            "DynamicTeamTest.test_DynamicTeam_from_json_str: Success")

class GroupTest(unittest.TestCase):
    """Collection of unit tests cases for the Group class
    """

    def setUp(self):
        XLOGGER.debug("GroupTest.setUp")
        self.id = "438e9245-b32d-445f-916bd3e07932c892"
        self.target_name = "Oracle Administrators"
        self.recipient_type = RecipientType.GROUP
        self.externally_owned_f = False
        self.externally_owned_t = True
        self.allowDuplicates = False
        self.useDefaultDevices = True
        self.observedByAll = True
        self.description = "Oracle database administrators"
        self.site_id = "dbf90cbf-a745-a054-abf0-cb3b5b56e6bd"
        self.site_self = "/api/xm/1/sites/dbf90cbf-a745-a054-abf0-cb3b5b56e6bd"
        self.site_previous = None
        self.site_next = None
        self.site_links_json_str = ('{"self": "%s"}')%(self.site_self)
        self.site_links = SelfLink.from_json_str(self.site_links_json_str)
        self.site_json_str = (
            '{"id": "%s", "links": %s}'
            )%(self.site_id, self.site_links_json_str)
        self.site_obj = ReferenceByIdAndSelfLink.from_json_str(
            self.site_json_str)
        self.externalKeyT = (
            "%s%s")%(self.recipient_type.value, self.target_name)
        self.externalKeyF = None
        self.locked_list = ["externallyOwned", "externalKey"]
        self.locked = (', '.join('"' + itm + '"' for itm in self.locked_list))
        self.status = RecipientStatus.ACTIVE
        self.self = "/api/xm/1/groups/438e9245-b32d-445f-916bd3e07932c892"
        self.links_json_str = ('{"self": "%s"}')%(self.self)
        self.links =SelfLink.from_json_str(self.links_json_str)
        self.pr_json_str1 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "allowDuplicates": %s, "description": "%s",'
            ' "observedByAll": %s, "useDefaultDevices": %s, '
            '"site": %s, "externalKey": "%s", "locked": [%s], '
            '"status": "%s", "links": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            str(self.allowDuplicates).lower(),
            self.description,
            str(self.observedByAll).lower(),
            str(self.useDefaultDevices).lower(),
            self.site_json_str, self.externalKeyT, self.locked,
            self.status.value, self.links_json_str)
        XLOGGER.debug(
            "GroupTest.setUp - pr_json_str1: %s", self.pr_json_str1)
        self.pr_json_str2 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "allowDuplicates": %s, "description": "%s",'
            ' "observedByAll": %s, "useDefaultDevices": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_f).lower(),
            str(self.allowDuplicates).lower(),
            self.description,
            str(self.observedByAll).lower(),
            str(self.useDefaultDevices).lower())
        XLOGGER.debug(
            "GroupTest.setUp - pr_json_str2: %s", self.pr_json_str2)
        self.bad_json1 = (
            '{"targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "allowDuplicates": %s, "description": "%s",'
            ' "observedByAll": %s, "useDefaultDevices": %s}'
            )%(self.target_name, self.recipient_type.value,
            str(self.externally_owned_f).lower(),
            str(self.allowDuplicates).lower(),
            self.description,
            str(self.observedByAll).lower(),
            str(self.useDefaultDevices).lower())
        self.bad_json2 = (
            '{"id": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "allowDuplicates": %s, "description": "%s",'
            ' "observedByAll": %s, "useDefaultDevices": %s}'
            )%(self.id, self.recipient_type.value,
            str(self.externally_owned_f).lower(),
            str(self.allowDuplicates).lower(),
            self.description,
            str(self.observedByAll).lower(),
            str(self.useDefaultDevices).lower())
        self.bad_json3 = (
            '{"id": "%s", "targetName": "%s", '
            '"externallyOwned": %s, "allowDuplicates": %s, "description": "%s",'
            ' "observedByAll": %s, "useDefaultDevices": %s}'
            )%(self.id, self.target_name,
            str(self.externally_owned_f).lower(),
            str(self.allowDuplicates).lower(),
            self.description,
            str(self.observedByAll).lower(),
            str(self.useDefaultDevices).lower())
        self.bad_json4 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"allowDuplicates": %s, "description": "%s",'
            ' "observedByAll": %s, "useDefaultDevices": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.allowDuplicates).lower(),
            self.description,
            str(self.observedByAll).lower(),
            str(self.useDefaultDevices).lower())
        self.bad_json5 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "description": "%s",'
            ' "observedByAll": %s, "useDefaultDevices": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_f).lower(),
            self.description,
            str(self.observedByAll).lower(),
            str(self.useDefaultDevices).lower())
        self.bad_json6 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "allowDuplicates": %s,'
            ' "observedByAll": %s, "useDefaultDevices": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_f).lower(),
            str(self.allowDuplicates).lower(),
            str(self.observedByAll).lower(),
            str(self.useDefaultDevices).lower())
        self.bad_json7 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "allowDuplicates": %s, "description": "%s",'
            ' "useDefaultDevices": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_f).lower(),
            str(self.allowDuplicates).lower(),
            self.description,
            str(self.useDefaultDevices).lower())
        self.bad_json8 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "allowDuplicates": %s, "description": "%s",'
            ' "observedByAll": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_f).lower(),
            str(self.allowDuplicates).lower(),
            self.description,
            str(self.observedByAll).lower())
        self.bad_json9 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "allowDuplicates": "0", '
            '"description": "%s", '
            '"observedByAll": %s, "useDefaultDevices": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_f).lower(),
            self.description,
            str(self.observedByAll).lower(),
            str(self.useDefaultDevices).lower())
        self.bad_json10 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "allowDuplicates": %s, "description": 0,'
            ' "observedByAll": %s, "useDefaultDevices": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_f).lower(),
            str(self.allowDuplicates).lower(),
            str(self.observedByAll).lower(),
            str(self.useDefaultDevices).lower())
        self.bad_json11 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "allowDuplicates": %s, "description": "%s",'
            ' "observedByAll": "0", "useDefaultDevices": %s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_f).lower(),
            str(self.allowDuplicates).lower(),
            self.description,
            str(self.useDefaultDevices).lower())
        self.bad_json12 = (
            '{"id": "%s", "targetName": "%s", "recipientType": "%s", '
            '"externallyOwned": %s, "allowDuplicates": %s, "description": "%s",'
            ' "observedByAll": %s, "useDefaultDevices": "0"}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_f).lower(),
            str(self.allowDuplicates).lower(),
            self.description,
            str(self.observedByAll).lower())
        self.bad_json13 = '{}'

    def tearDown(self):
        XLOGGER.debug("GroupTest.tearDown")

    def test_Group(self):
        XLOGGER.debug("GroupTest.test_Group: Start")
        obj = Group(
            self.id, self.target_name, self.recipient_type,
            self.externally_owned_t, self.allowDuplicates, self.description,
            self.observedByAll, self.useDefaultDevices, self.site_obj,
            self.externalKeyT, self.locked_list, self.status, self.links)
        self.assertIsInstance(obj, Group)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.recipient_type, RecipientType)
        self.assertEqual(obj.recipient_type, self.recipient_type)
        self.assertEqual(obj.recipient_type.value, self.recipient_type.value)
        self.assertEqual(obj.externally_owned, self.externally_owned_t)
        self.assertEqual(obj.allow_duplicates, self.allowDuplicates)
        self.assertEqual(obj.description, self.description)
        self.assertEqual(obj.observed_by_all, self.observedByAll)
        self.assertIsInstance(obj.site, ReferenceByIdAndSelfLink)
        self.assertEqual(obj.site, self.site_obj)
        self.assertEqual(obj.external_key, self.externalKeyT)
        self.assertEqual(obj.locked, self.locked_list)
        self.assertIsInstance(obj.status, RecipientStatus)
        self.assertEqual(obj.status, self.status)
        self.assertEqual(obj.status.value, self.status.value)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links, self.links)
        obj2 = Group(
            self.id, self.target_name, self.recipient_type,
            self.externally_owned_f, self.allowDuplicates, self.description,
            self.observedByAll, self.useDefaultDevices)
        self.assertIsInstance(obj2, Group)
        self.assertRaises(TypeError, Group, self.id, self.target_name,
            self.recipient_type)
        self.assertRaises(TypeError, Group, self.id, self.target_name)
        self.assertRaises(TypeError, Group, self.id)
        self.assertRaises(TypeError, Group)
        self.assertRaises(TypeError, Group, 0, self.target_name,
            self.recipient_type, self.externally_owned_f)
        self.assertRaises(TypeError, Group, self.id, 0,
            self.recipient_type, self.externally_owned_f)
        self.assertRaises(TypeError, Group, self.id, self.target_name,
            0, self.externally_owned_f)
        self.assertRaises(TypeError, Group, self.id, self.target_name,
            self.recipient_type, self.links)
        XLOGGER.debug(
            "GroupTest.test_Group: Success")

    def test_Group_from_json_obj(self):
        XLOGGER.debug(
            "GroupTest.test_Group_from_json_obj: Start")
        json_obj = json.loads(self.pr_json_str1)
        obj = Group.from_json_obj(json_obj)
        self.assertIsInstance(obj, Group)
        obj1 = Group(
            self.id, self.target_name, self.recipient_type,
            self.externally_owned_t, self.allowDuplicates, self.description,
            self.observedByAll, self.useDefaultDevices, self.site_obj,
            self.externalKeyT, self.locked_list, self.status, self.links)
        self.assertEqual(obj, obj1)
        XLOGGER.debug(
            "GroupTest.test_Group_from_json_obj: Success")

    def test_Group_from_json_str(self):
        XLOGGER.debug(
            "GroupTest.test_Group_from_json_str: Start")
        obj = Group.from_json_str(self.pr_json_str1)
        self.assertIsInstance(obj, Group)
        obj1 = Group(
            self.id, self.target_name, self.recipient_type,
            self.externally_owned_t, self.allowDuplicates, self.description,
            self.observedByAll, self.useDefaultDevices, self.site_obj,
            self.externalKeyT, self.locked_list, self.status, self.links)
        self.assertEqual(obj, obj1)
        self.assertRaises(
            TypeError, Group.from_json_str, self.bad_json1)
        self.assertRaises(
            TypeError, Group.from_json_str, self.bad_json2)
        self.assertRaises(
            TypeError, Group.from_json_str, self.bad_json3)
        self.assertRaises(
            TypeError, Group.from_json_str, self.bad_json4)
        self.assertRaises(
            TypeError, Group.from_json_str, self.bad_json5)
        self.assertRaises(
            TypeError, Group.from_json_str, self.bad_json6)
        self.assertRaises(
            TypeError, Group.from_json_str, self.bad_json7)
        self.assertRaises(
            TypeError, Group.from_json_str, self.bad_json8)
        self.assertRaises(
            TypeError, Group.from_json_str, self.bad_json9)
        self.assertRaises(
            TypeError, Group.from_json_str, self.bad_json10)
        self.assertRaises(
            TypeError, Group.from_json_str, self.bad_json11)
        obj = Group.from_json_str(self.pr_json_str2)
        self.assertIsInstance(obj, Group)
        obj2 = Group(
            self.id, self.target_name, self.recipient_type,
            self.externally_owned_f, self.allowDuplicates, self.description,
            self.observedByAll, self.useDefaultDevices)
        self.assertEqual(obj, obj2)
        XLOGGER.debug(
            "GroupTest.test_Group_from_json_str: Success")

class PersonTest(unittest.TestCase):
    """Collection of unit tests cases for the Person class
    """

    def setUp(self):#pylint: disable=too-many-statements
        XLOGGER.debug("PersonTest.setUp")
        self.test_data = (
        '{'
        '"id":"ac06ca54-1709-432b-9050-11701710e01b",'
        '"targetName":"fleiter1234",'
        '"recipientType":"PERSON",'
        '"externallyOwned":true,'
        '"firstName":"Felix",'
        '"lastName":"Leiter",'
        '"language":"en",'
        '"timezone":"US/Pacific",'
        '"webLogin":"fleiter1234",'
        '"site":{'
        '"id":"7f84fa10-70a6-45f6-9cae-2185fcba8993",'
        '"links":{'
        '"self":"/api/xm/1/sites/7f84fa10-70a6-45f6-9cae-2185fcba8993"}'
        '},'
        '"phoneLogin":"fleiter1234",'
        '"properties":{"Department":"Finance","Job Title":"Analyst"},'
        '"roles":{"count":1,"total":1,"data":[{'
        '"id":"6ff659d1-353e-424c-8dd3-f8cba6fc15a0",'
        '"name":"Full Access User"}]'
        '},'
        '"externalKey":"PERSONfleiter1234",'
        '"locked":["externallyOwned","externalKey"],'
        '"status":"ACTIVE",'
        '"links":{'
        '"self":"/api/xm/1/people/ac06ca54-1709-432b-9050-11701710e01b"}'
        '}')
        XLOGGER.debug("PersonTest.setUp - self.test_data: %s", self.test_data)
        self.id = "ac06ca54-1709-432b-9050-11701710e01b"
        self.target_name = "fleiter1234"
        self.recipient_type = RecipientType.PERSON
        self.externally_owned_f = False
        self.externally_owned_t = True
        self.external_key = "PERSONfleiter1234"
        self.self = "/api/xm/1/people/ac06ca54-1709-432b-9050-11701710e01b"
        self.links_json_str = ('{"self":"%s"}')%(self.self)
        self.links =SelfLink.from_json_str(self.links_json_str)
        self.first_name = "Felix"
        self.last_name  = "Leiter"
        self.language = "en"
        self.timezone = "US/Pacific"
        self.web_login = "fleiter1234"
        self.phone_login = "fleiter1234"
        self.properties_json_str = (
            '{"Department":"Finance","Job Title":"Analyst"}')
        self.properties = dict([
            ("Department","Finance"),("Job Title","Analyst")
            ])
        self.roles_json_str = ('{"count":1,"total":1,"data":[%s]}')%(
            ('{"id":"6ff659d1-353e-424c-8dd3-f8cba6fc15a0",'
             '"name":"Full Access User"}'))
        self.roles = RolePagination.from_json_str(self.roles_json_str)
        self.site_id = "7f84fa10-70a6-45f6-9cae-2185fcba8993"
        self.site_self = "/api/xm/1/sites/7f84fa10-70a6-45f6-9cae-2185fcba8993"
        self.site_links_json_str = ('{"self":"%s"}')%(self.site_self)
        self.site_links = SelfLink.from_json_str(self.site_links_json_str)
        self.site_json_str = ('{"id":"%s","links":%s}')%(
            self.site_id, self.site_links_json_str)
        self.site = ReferenceByIdAndSelfLink.from_json_str(
            self.site_json_str)
        self.externalKeyT = (
            "%s%s")%(self.recipient_type.value, self.target_name)
        self.externalKeyF = None
        self.locked_list = ["externallyOwned","externalKey"]
        self.locked = (','.join('"' + itm + '"' for itm in self.locked_list))
        self.status = RecipientStatus.ACTIVE
        self.self = "/api/xm/1/people/ac06ca54-1709-432b-9050-11701710e01b"
        self.json_str1 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":"%s",'
            '"language":"%s","timezone":"%s","webLogin":"%s",'
            '"site":%s,"phoneLogin":"%s","properties":%s,"roles":%s,'
            '"externalKey":"%s","locked":[%s],"status":"%s","links":%s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site_json_str,
            self.phone_login,
            self.properties_json_str,
            self.roles_json_str,
            self.externalKeyT, self.locked,
            self.status.value, self.links_json_str)
        XLOGGER.debug("PersonTest.setUp - json_str1: %s", self.json_str1)
        self.json_str2 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":"%s",'
            '"language":"%s","timezone":"%s","webLogin":"%s","site":%s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site_json_str)
        XLOGGER.debug("PersonTest.setUp - json_str2: %s", self.json_str2)
        #Missing required field errors
        self.bad_json1 = (
            '{"targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":"%s",'
            '"language":"%s","timezone":"%s","webLogin":"%s",'
            '"site":%s}'
            )%(self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site_json_str)
        self.bad_json2 = (
            '{"id":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":"%s",'
            '"language":"%s","timezone":"%s","webLogin":"%s",'
            '"site":%s}'
            )%(self.id, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site_json_str)
        self.bad_json3 = (
            '{"id":"%s","targetName":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":"%s",'
            '"language":"%s","timezone":"%s","webLogin":"%s",'
            '"site":%s}'
            )%(self.id, self.target_name,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site_json_str)
        self.bad_json4 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"firstName":"%s","lastName":"%s",'
            '"language":"%s","timezone":"%s","webLogin":"%s",'
            '"site":%s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site_json_str)
        self.bad_json5 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"lastName":"%s",'
            '"language":"%s","timezone":"%s","webLogin":"%s",'
            '"site":%s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site_json_str)
        self.bad_json6 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s",'
            '"language":"%s","timezone":"%s","webLogin":"%s",'
            '"site":%s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site_json_str)
        self.bad_json7 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":"%s",'
            '"timezone":"%s","webLogin":"%s",'
            '"site":%s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.last_name,
            self.timezone,
            self.web_login,
            self.site_json_str)
        self.bad_json8 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":"%s",'
            '"language":"%s","webLogin":"%s",'
            '"site":%s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.last_name,
            self.language,
            self.web_login,
            self.site_json_str)
        self.bad_json9 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":"%s",'
            '"language":"%s","timezone":"%s",'
            '"site":%s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.site_json_str)
        self.bad_json10 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":"%s",'
            '"language":"%s","timezone":"%s","webLogin":"%s"}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.web_login)
        #Bad data type errors
        self.bad_json11 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":0, "lastName":"%s",'
            '"language":"%s","timezone":"%s","webLogin":"%s",'
            '"site":%s,"phoneLogin":"%s","properties":%s,"roles":%s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site_json_str,
            self.phone_login,
            self.properties_json_str,
            self.roles_json_str)
        self.bad_json12 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":0, '
            '"language":"%s","timezone":"%s","webLogin":"%s",'
            '"site":%s,"phoneLogin":"%s","properties":%s,"roles":%s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site_json_str,
            self.phone_login,
            self.properties_json_str,
            self.roles_json_str)
        self.bad_json13 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":"%s",'
            '"language":0, "timezone":"%s","webLogin":"%s",'
            '"site":%s,"phoneLogin":"%s","properties":%s,"roles":%s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.last_name,
            self.timezone,
            self.web_login,
            self.site_json_str,
            self.phone_login,
            self.properties_json_str,
            self.roles_json_str)
        self.bad_json14 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":"%s",'
            '"language":"%s","timezone":0, "webLogin":"%s",'
            '"site":%s,"phoneLogin":"%s","properties":%s,"roles":%s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.last_name,
            self.language,
            self.web_login,
            self.site_json_str,
            self.phone_login,
            self.properties_json_str,
            self.roles_json_str)
        self.bad_json15 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":"%s",'
            '"language":"%s","timezone":"%s","webLogin":0, '
            '"site":%s,"phoneLogin":"%s","properties":%s,"roles":%s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.site_json_str,
            self.phone_login,
            self.properties_json_str,
            self.roles_json_str)
        self.bad_json16 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":"%s",'
            '"language":"%s","timezone":"%s","webLogin":"%s",'
            '"site":0, "phoneLogin":"%s","properties":%s,"roles":%s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.phone_login,
            self.properties_json_str,
            self.roles_json_str)
        self.bad_json17 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":"%s",'
            '"language":"%s","timezone":"%s","webLogin":"%s",'
            '"site":%s,"phoneLogin":0, "properties":%s,"roles":%s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site_json_str,
            self.properties_json_str,
            self.roles_json_str)
        self.bad_json18 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":"%s",'
            '"language":"%s","timezone":"%s","webLogin":"%s",'
            '"site":%s,"phoneLogin":"%s","properties":0, "roles":%s}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site_json_str,
            self.phone_login,
            self.roles_json_str)
        self.bad_json19 = (
            '{"id":"%s","targetName":"%s","recipientType":"%s",'
            '"externallyOwned":%s,"firstName":"%s","lastName":"%s",'
            '"language":"%s","timezone":"%s","webLogin":"%s",'
            '"site":%s,"phoneLogin":"%s","properties":%s,"roles":0}'
            )%(self.id, self.target_name, self.recipient_type.value,
            str(self.externally_owned_t).lower(),
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site_json_str,
            self.phone_login,
            self.properties_json_str)
        self.bad_json20 = '{}'

    def tearDown(self):
        XLOGGER.debug("PersonTest.tearDown")

    def test_Person(self):
        XLOGGER.debug("PersonTest.test_Person: Start")
        obj = Person(
            self.id,
            self.target_name,
            self.recipient_type,
            self.externally_owned_t,
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site,
            self.phone_login,
            self.properties,
            self.roles,
            self.externalKeyT,
            self.locked_list,
            self.status,
            self.links)
        self.assertIsInstance(obj, Person)
        self.assertEqual(obj.id, self.id)
        self.assertEqual(obj.target_name, self.target_name)
        self.assertIsInstance(obj.recipient_type, RecipientType)
        self.assertEqual(obj.recipient_type, self.recipient_type)
        self.assertEqual(obj.recipient_type.value, self.recipient_type.value)
        self.assertEqual(obj.externally_owned, self.externally_owned_t)
        self.assertEqual(obj.first_name, self.first_name)
        self.assertEqual(obj.last_name, self.last_name)
        self.assertEqual(obj.language, self.language)
        self.assertEqual(obj.timezone, self.timezone)
        self.assertEqual(obj.web_login, self.web_login)
        self.assertIsInstance(obj.site, ReferenceByIdAndSelfLink)
        self.assertEqual(obj.site, self.site)
        self.assertEqual(obj.phone_login, self.phone_login)
        self.assertIsInstance(obj.properties, dict)
        self.assertEqual(obj.properties, self.properties)
        self.assertIsInstance(obj.roles, RolePagination)
        self.assertEqual(obj.roles, self.roles)
        self.assertEqual(obj.external_key, self.externalKeyT)
        self.assertEqual(obj.locked, self.locked_list)
        self.assertIsInstance(obj.status, RecipientStatus)
        self.assertEqual(obj.status, self.status)
        self.assertEqual(obj.status.value, self.status.value)
        self.assertIsInstance(obj.links, SelfLink)
        self.assertEqual(obj.links, self.links)
        obj2 = Person(
            self.id,
            self.target_name,
            self.recipient_type,
            self.externally_owned_t,
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site)
        self.assertIsInstance(obj2, Person)
        self.assertRaises(TypeError, Person)
        self.assertRaises(TypeError, Person, self.id)
        self.assertRaises(TypeError, Person, self.id, self.target_name)
        self.assertRaises(TypeError, Person, self.id, self.target_name,
            self.recipient_type)
        self.assertRaises(TypeError, Person, 0, self.target_name,
            self.recipient_type, self.externally_owned_f)
        self.assertRaises(TypeError, Person, self.id, 0,
            self.recipient_type, self.externally_owned_f)
        self.assertRaises(TypeError, Person, self.id, self.target_name,
            0, self.externally_owned_f)
        self.assertRaises(TypeError, Person, self.id, self.target_name,
            self.recipient_type, self.links)
        XLOGGER.debug(
            "PersonTest.test_Person: Success")

    def test_Person_from_json_obj(self):
        XLOGGER.debug(
            "PersonTest.test_Person_from_json_obj: Start")
        json_obj = json.loads(self.json_str2)
        obj = Person.from_json_obj(json_obj)
        self.assertIsInstance(obj, Person)
        obj2 = Person(
            self.id,
            self.target_name,
            self.recipient_type,
            self.externally_owned_t,
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site)
        self.assertEqual(obj, obj2)
        XLOGGER.debug(
            "PersonTest.test_Person_from_json_obj: Success")

    def test_Person_from_json_str(self):
        XLOGGER.debug(
            "PersonTest.test_Person_from_json_str: Start")
        obj = Person.from_json_str(self.json_str1)
        self.assertIsInstance(obj, Person)
        XLOGGER.debug(
            "PersonTest.test_Person_from_json_str: obj: %s",
            repr(obj))
        XLOGGER.debug(
            "PersonTest.test_Person_from_json_str: json.dumps(obj): %s",
            obj.json)
        assert self.json_str1 == obj.json
        obj1 = Person(
            self.id,
            self.target_name,
            self.recipient_type,
            self.externally_owned_t,
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site,
            self.phone_login,
            self.properties,
            self.roles,
            self.externalKeyT,
            self.locked_list,
            self.status,
            self.links)
        self.assertEqual(obj, obj1)
        XLOGGER.debug(
            "PersonTest.test_Person_from_json_str: Creating test_data")
        test_data = Person.from_json_str(self.test_data)
        self.assertIsInstance(test_data, Person)
        self.assertEqual(obj, test_data)
        jstr = obj.json
        XLOGGER.debug(
            "PersonTest.test_Person_from_json_str:  obj.json: %s",
            jstr)
        XLOGGER.debug(
            "PersonTest.test_Person_from_json_str: test_data: %s",
            self.test_data)
        assert jstr == self.test_data
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json1)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json2)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json3)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json4)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json5)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json6)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json7)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json8)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json9)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json10)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json11)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json12)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json13)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json14)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json15)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json16)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json17)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json18)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json19)
        self.assertRaises(
            TypeError, Person.from_json_str, self.bad_json20)
        obj = Person.from_json_str(self.json_str2)
        self.assertIsInstance(obj, Person)
        obj2 = Person(
            self.id,
            self.target_name,
            self.recipient_type,
            self.externally_owned_t,
            self.first_name,
            self.last_name,
            self.language,
            self.timezone,
            self.web_login,
            self.site)
        self.assertEqual(obj, obj2)
        XLOGGER.debug(
            "PersonTest.test_Person_from_json_str: Success")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
