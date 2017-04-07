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

class ResponseOptionTest(unittest.TestCase):
    """Collection of unit tests cases for the ResponseOption class
    """

    def setUp(self):
        XLOGGER.debug("ResponseOptionTest.setUp")
        self.test_data = (
            '{'
            '"text":"Reject",'
            '"description":"Reject",'
            '"prompt":"I cannot assist",'
            '"number":2,'
            '"joinConference":false,'
            '"action":"STOP_NOTIFYING_USER",'
            '"contribution":"NONE"'
            '}')
        self.number = 2
        self.text = "Reject"
        self.description = "Reject"
        self.prompt = "I cannot assist"
        self.action = ResponseAction.STOP_NOTIFYING_USER
        self.contribution = ResponseContribution.NONE
        self.join_conference = False
        self.json_str = (
            '{'
            '"number":%d,"text":"%s","description":"%s","prompt":"%s",'
            '"action":"%s","contribution":"%s","joinConference":%s'
            '}')%(
            self.number, self.text, self.description, self.prompt,
            self.action.value, self.contribution.value,
            str(self.join_conference).lower()
            )
        self.bad_json1 = (
            '{'
            '"text":"%s","description":"%s","prompt":"%s",'
            '"action":"%s","contribution":"%s","joinConference":%s'
            '}')%(
            self.text, self.description, self.prompt,
            self.action.value, self.contribution.value,
            str(self.join_conference).lower()
            )
        self.bad_json2 = (
            '{'
            '"number":%d,"description":"%s","prompt":"%s",'
            '"action":"%s","contribution":"%s","joinConference":%s'
            '}')%(
            self.number, self.description, self.prompt,
            self.action.value, self.contribution.value,
            str(self.join_conference).lower()
            )
        self.bad_json3 = (
            '{'
            '"number":%d,"text":"%s","prompt":"%s",'
            '"action":"%s","contribution":"%s","joinConference":%s'
            '}')%(
            self.number, self.text, self.prompt,
            self.action.value, self.contribution.value,
            str(self.join_conference).lower()
            )
        self.bad_json4 = (
            '{'
            '"number":%d,"text":"%s","description":"%s",'
            '"action":"%s","contribution":"%s","joinConference":%s'
            '}')%(
            self.number, self.text, self.description,
            self.action.value, self.contribution.value,
            str(self.join_conference).lower()
            )
        self.bad_json5 = (
            '{'
            '"number":%d,"text":"%s","description":"%s","prompt":"%s",'
            '"contribution":"%s","joinConference":%s'
            '}')%(
            self.number, self.text, self.description, self.prompt,
            self.contribution.value,
            str(self.join_conference).lower()
            )
        self.bad_json6 = (
            '{'
            '"number":%d,"text":"%s","description":"%s","prompt":"%s",'
            '"action":"%s","joinConference":%s'
            '}')%(
            self.number, self.text, self.description, self.prompt,
            self.action.value,
            str(self.join_conference).lower()
            )
        self.bad_json7 = (
            '{'
            '"number":%d,"text":"%s","description":"%s","prompt":"%s",'
            '"action":"%s","contribution":"%s"'
            '}')%(
            self.number, self.text, self.description, self.prompt,
            self.action.value, self.contribution.value
            )
        self.bad_json8 = (
            '{'
            '"number":"0","text":"%s","description":"%s","prompt":"%s",'
            '"action":"%s","contribution":"%s","joinConference":%s'
            '}')%(
            self.text, self.description, self.prompt,
            self.action.value, self.contribution.value,
            str(self.join_conference).lower()
            )
        self.bad_json9 = (
            '{'
            '"number":%d,"text":0,"description":"%s","prompt":"%s",'
            '"action":"%s","contribution":"%s","joinConference":%s'
            '}')%(
            self.number, self.description, self.prompt,
            self.action.value, self.contribution.value,
            str(self.join_conference).lower()
            )
        self.bad_json10 = (
            '{'
            '"number":%d,"text":"%s","description":0,"prompt":"%s",'
            '"action":"%s","contribution":"%s","joinConference":%s'
            '}')%(
            self.number, self.text, self.prompt,
            self.action.value, self.contribution.value,
            str(self.join_conference).lower()
            )
        self.bad_json11 = (
            '{'
            '"number":%d,"text":"%s","description":"%s","prompt":0,'
            '"action":"%s","contribution":"%s","joinConference":%s'
            '}')%(
            self.number, self.text, self.description,
            self.action.value, self.contribution.value,
            str(self.join_conference).lower()
            )
        self.bad_json12 = (
            '{'
            '"number":%d,"text":"%s","description":"%s","prompt":"%s",'
            '"action":0,"contribution":"%s","joinConference":%s'
            '}')%(
            self.number, self.text, self.description, self.prompt,
            self.contribution.value,
            str(self.join_conference).lower()
            )
        self.bad_json13 = (
            '{'
            '"number":%d,"text":"%s","description":"%s","prompt":"%s",'
            '"action":"%s","contribution":0,"joinConference":%s'
            '}')%(
            self.number, self.text, self.description, self.prompt,
            self.action.value,
            str(self.join_conference).lower()
            )
        self.bad_json14 = (
            '{'
            '"number":%d,"text":"%s","description":"%s","prompt":"%s",'
            '"action":"%s","contribution":"%s","joinConference":"0"'
            '}')%(
            self.number, self.text, self.description, self.prompt,
            self.action.value, self.contribution.value
            )

    def tearDown(self):
        XLOGGER.debug("ResponseOptionTest.tearDown")

    def test_class(self):
        XLOGGER.debug("test_class: Start")
        obj = ResponseOption(
            self.text, self.description, self.prompt, self.number,
            self.join_conference, self.action, self.contribution)
        self.assertIsInstance(obj, ResponseOption)
        self.assertEqual(obj.number, self.number)
        self.assertEqual(obj.text, self.text)
        self.assertEqual(obj.description, self.description)
        self.assertEqual(obj.prompt, self.prompt)
        self.assertEqual(obj.action, self.action)
        self.assertEqual(obj.contribution, self.contribution)
        self.assertEqual(obj.join_conference, self.join_conference)
        self.assertRaises(TypeError, ResponseOption, "")
        self.assertRaises(TypeError, ResponseOption, "", "")
        self.assertRaises(TypeError, ResponseOption, "", "", "")
        self.assertRaises(TypeError, ResponseOption, "", "", "", 0)
        self.assertRaises(
            TypeError, ResponseOption, "", "", "", 0, False)
        self.assertRaises(
            TypeError, ResponseOption, "", "", "", 0, False,
            ResponseAction.STOP_NOTIFYING_USER)
        self.assertRaises(
            TypeError, ResponseOption, 0, "", "", 0, False,
            ResponseAction.STOP_NOTIFYING_USER,
            ResponseContribution.NONE)
        self.assertRaises(
            TypeError, ResponseOption, "", 0, "", 0, False,
            ResponseAction.STOP_NOTIFYING_USER,
            ResponseContribution.NONE)
        self.assertRaises(
            TypeError, ResponseOption, "", "", 0, 0, False,
            ResponseAction.STOP_NOTIFYING_USER,
            ResponseContribution.NONE)
        self.assertRaises(
            TypeError, ResponseOption, "", "", "", "", False,
            ResponseAction.STOP_NOTIFYING_USER,
            ResponseContribution.NONE)
        self.assertRaises(
            TypeError, ResponseOption, "", "", "", 0, "",
            ResponseAction.STOP_NOTIFYING_USER,
            ResponseContribution.NONE)
        self.assertRaises(
            TypeError, ResponseOption, "", "", "", 0, False,
            0,
            ResponseContribution.NONE)
        self.assertRaises(
            TypeError, ResponseOption, "", "", "", 0, False,
            ResponseAction.STOP_NOTIFYING_USER,
            0)
        XLOGGER.debug("test_class: Success")

    def test_from_json_obj(self):
        XLOGGER.debug("test_from_json_obj: Start")
        json_obj = json.loads(self.json_str)
        obj = ResponseOption.from_json_obj(json_obj)
        self.assertIsInstance(obj, ResponseOption)
        XLOGGER.debug(
            "test_from_json_obj: Success")

    def test_from_json_str(self):
        XLOGGER.debug(
            "test_from_json_str: Start")
        obj = ResponseOption.from_json_str(self.json_str)
        self.assertIsInstance(obj, ResponseOption)
        obj1 = ResponseOption(
            self.text, self.description, self.prompt, self.number,
            self.join_conference, self.action, self.contribution)
        self.assertEqual(obj, obj1)
        jstr = obj.json
        XLOGGER.debug("test_from_json_str:  obj.json: %s", jstr)
        XLOGGER.debug("test_from_json_str: test_data: %s", self.test_data)
        self.assertEqual(jstr, self.test_data)
        self.assertRaises(
            TypeError, ResponseOption.from_json_str, self.bad_json1)
        self.assertRaises(
            TypeError, ResponseOption.from_json_str, self.bad_json2)
        self.assertRaises(
            TypeError, ResponseOption.from_json_str, self.bad_json3)
        self.assertRaises(
            TypeError, ResponseOption.from_json_str, self.bad_json4)
        self.assertRaises(
            TypeError, ResponseOption.from_json_str, self.bad_json5)
        self.assertRaises(
            TypeError, ResponseOption.from_json_str, self.bad_json6)
        self.assertRaises(
            TypeError, ResponseOption.from_json_str, self.bad_json7)
        self.assertRaises(
            TypeError, ResponseOption.from_json_str, self.bad_json8)
        self.assertRaises(
            TypeError, ResponseOption.from_json_str, self.bad_json9)
        self.assertRaises(
            TypeError, ResponseOption.from_json_str, self.bad_json10)
        self.assertRaises(
            TypeError, ResponseOption.from_json_str, self.bad_json11)
        self.assertRaises(
            TypeError, ResponseOption.from_json_str, self.bad_json12)
        self.assertRaises(
            TypeError, ResponseOption.from_json_str, self.bad_json13)
        self.assertRaises(
            TypeError, ResponseOption.from_json_str, self.bad_json14)
        XLOGGER.debug(
            "test_from_json_str: Success")

class EventTest(unittest.TestCase):
    """Collection of unit tests cases for the Event class
    """

    def setUp(self):
        XLOGGER.debug("Event.setUp")
        self.test_data = (
            '{'
            '"bypassPhoneIntro":false,'
            '"created":"2017-03-05T11:58:20.579+0000",'
            '"escalationOverride":false,'
            '"eventId":"739027",'
            '"expirationInMinutes":180,'
            '"form":{"id":"469f7a2a-accc-4e22-a093-daf9566c7ac4"},'
            '"id":"ba730262-bcc0-4e73-bbcb-c6867ff6bbe0",'
            '"incident":"INCIDENT_ID-739027",'
            '"notificationAuditCount":9,'
            '"overrideDeviceRestrictions":false,'
            '"priority":"MEDIUM",'
            '"recipients":{"count":1,'
            '"data":[{"allowDuplicates":true,'
            '"description":"",'
            '"externallyOwned":true,'
            '"id":"6890d43d-40e8-4229-817d-710435be2162",'
            '"links":{"self":"/api/xm/1/groups/6890d43d-40e8-4229-817d-'
            '710435be2162"},'
            '"locked":["allowDuplicates",'
            '"status",'
            '"targetName",'
            '"useDefaultDevices"],'
            '"observedByAll":true,'
            '"recipientType":"GROUP",'
            '"site":{"id":"715dd300-c014-4ff1-aa7a-3d0831eca232",'
            '"links":{"self":"/api/xm/1/sites/715dd300-c014-4ff1-aa7a-'
            '3d0831eca232"}},'
            '"status":"ACTIVE",'
            '"targetName":"IBMSUPP",'
            '"targeted":true,'
            '"useDefaultDevices":false}],'
            '"links":{"self":"/api/xm/1/events/ba730262-bcc0-4e73-bbcb-'
            'c6867ff6bbe0/recipients?targeted=true&offset=0&limit=100"},'
            '"total":1},'
            ' "requirePhonePassword":false,'
            ' "responseOptions":{"count":2,'
            '"data":[{"action":"ASSIGN_TO_USER",'
            '"contribution":"POSITIVE",'
            '"description":"Accept",'
            '"joinConference":false,'
            '"number":2,'
            '"prompt":"Accept",'
            '"text":"Accept"},'
            '{"action":"ESCALATE",'
             '"contribution":"NEGATIVE",'
            '"description":"Decline",'
            '"joinConference":false,'
            '"number":4,'
            '"prompt":"Decline",'
            '"text":"Decline"}],'
            '"total":2},'
            '"status":"TERMINATED_EXTERNAL",'
            '"submitter":{"id":"b2f65f85-c967-44f5-9a53-bce632bfd270",'
            '"links":{"self":"/api/xm/1/people/b2f65f85-c967-44f5-9a53-bce632bfd270"},'
            '"targetName":"XM_APIP"},'
            '"terminated":"2017-03-05T12:02:11.604+0000"'
            '}')

    def tearDown(self):
        XLOGGER.debug("Event.tearDown")

    def test_from_json_str(self):
        XLOGGER.debug("test_from_json_str: Start")
        obj = Event.from_json_str(self.test_data)
        self.assertIsInstance(obj, Event)
        jstr = obj.json
        XLOGGER.debug("test_from_json_str: jstr: %s", jstr)
        obj2 = Event.from_json_str(jstr)
        self.assertIsInstance(obj2, Event)
        assert obj == obj2


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
