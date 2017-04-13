"""xmatters Device

This module represents a view of the xmatters Device that is used in both
recipient as well as user definitions.
The Device sub-classes contain both controlling
methods (typically static) for retrieving a list of Device instances, as well as
methods for manipulating instances of devices.

Device objects represent devices in xMatters.

Device objects include the fields defined in Recipient object in addition to
fields specific to device recipients.

The Device object is a base for specific types of devices such as email and
voice devices. When you retrieve a device, it contains the fields included
in Recipient object, Device object, and the specific type of device. 
See also:

    Recipient object (see recipients.py)
    Email device object
    Voice device object
    SMS device object
    Text Pager device object
    Apple Push device object
    Android Push device object
    BlackBerry Push device object
    Fax device object
    Public Address device object
    Generic device object

Ref:
    https://help.xmatters.com/xmAPI/?shell#device-objects

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from enum import Enum
import logging
from requests.exceptions import RequestException
from urllib.parse import quote_plus

from xmatters import PersonReference
from xmatters import Recipient
from xmatters import RecipientType
from xmatters import ReferenceById
from xmatters import XmattersBase
from xmatters import XmattersEntity
from xmatters import XmattersList

LOGGER = logging.getLogger('xlogger')

class DeviceType(Enum):
    """The type of a Device object"""
    ANDROID_PUSH = "ANDROID_PUSH"
    APPLE_PUSH = "APPLE_PUSH"
    BLACKBERRY_PUSH = "BLACKBERRY_PUSH"
    EMAIL = "EMAIL"
    FAX = "FAX"
    GENERIC = "GENERIC"
    TEXT_PAGER = "TEXT_PAGER"
    TEXT_PHONE = "TEXT_PHONE"
    VOICE = "VOICE"
    VOICE_IVR = "VOICE_IVR"

class PriorityThreshold(Enum):
    """The minimum priority that an event must have for it to be delivered to
        this device."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class TestStatus(Enum):
    """Whether the device has been tested."""
    UNTESTED = "UNTESTED"
    PENDING = "PENDING"
    TESTED = "TESTED"

class DeviceTimeframe(XmattersBase):
    """xMatters DeviceTimeframe representation
    
    Device timeframes objects list the timeframes that the device is active
    and able to receive notifications.

    Reference:
        https://help.xmatters.com/xmAPI/?python#device-timeframes-object

    Args:
        name (str): The name of the timeframe.
        start_time (str): The time of day that the timeframe begins.
            Example: “08:00”
        duration_in_minutes (int): The length of the timeframe in minutes.
        days (:obj:`list` of :obj:`str`): List of the days of the week this
            timeframe is active. Valid values include the following:
            “SU”, “MO”, “TU”, “WE”m “TH", “FR”, “SA”
        exclude_holidays (bool): True if the timeframe is not active on holidays
        timezone (str, optional): The time zone of the startTime value.
            Example: “US/Pacific”
    """
    _arg_names = _attr_names = [
        'name', 'start_time', 'duration_in_minutes', 'days',
        'exclude_holidays', 'timezone']
    _json_names = [
        'name', 'startTime', 'durationInMinutes', 'days',
        'excludeHolidays', 'timezone']
    _attr_types = [str, str, int, list, bool, str]

class DeviceTimeframeList(XmattersList):
    """xMatters DeviceTimeframe list representation

    Defines a Python list that also adds a member_type element to hold the
    XmattersBase subclass that represents the type of member

    Attributes:
        base_class (:obj:`class`): Type of XmatterBase subclass held in list
    """
    base_class = DeviceTimeframe

class Device(Recipient):
    """xMatters Device representation

    Contains fields common to recipients and all types of devices.
    See also Recipient object.

    Reference:
        https://help.xmatters.com/xmAPI/?shell#device-objects
        https://help.xmatters.com/xmAPI/index.html#recipient-object

    Args:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): The type of device.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        timeframes (:obj:`DeviceTimeframeList`, optional): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`, optional): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`, optional): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`, optional): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`, optional): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.

    Attributes:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): The type of device.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        timeframes (:obj:`DeviceTimeframeList`): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.
    """
    _common_arg_names = (
        Recipient._common_arg_names +
        ['default_device', 'delay', 'description', 'device_type', 'name',
         'owner', 'priority_threshold', 'provider', 'sequence',
         'test_status'])
    _common_arg_opt_names = Recipient._common_arg_opt_names + ['*timeframes']
    _common_attr_names = (
        Recipient._common_attr_names +
        ['default_device', 'delay', 'description', 'device_type', 'name',
         'owner', 'priority_threshold', 'provider', 'sequence',
         'test_status'])
    _common_attr_opt_names = Recipient._common_attr_opt_names + ['timeframes']
    _common_json_names = (
        Recipient._common_json_names +
        ['defaultDevice', 'delay', 'description', 'deviceType', 'name',
         'owner', 'priorityThreshold', 'provider', 'sequence',
         'testStatus'])
    _common_json_opt_names = Recipient._common_json_opt_names + ['timeframes']
    _common_attr_types = (
        Recipient._common_attr_types +
        [bool, int, str, DeviceType, str, PersonReference, PriorityThreshold,
         ReferenceById, str, TestStatus])
    _common_attr_opt_types = Recipient._common_attr_opt_types + [
        DeviceTimeframeList]

class EmailDevice(Device):
    """xMatters Email Device representation

    Email device objects include the fields of Recipient object and 
    Device object, as well as the following fields:
    See also Device and Recipient objects.

    Reference:
        https://help.xmatters.com/xmAPI/#email-device-object
        https://help.xmatters.com/xmAPI/?shell#device-objects
        https://help.xmatters.com/xmAPI/index.html#recipient-object

    Args:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): The type of device, EMAIL.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        email_address (str): The email address associated with the device.
            Your system administrator may restrict the domains that are allowed
            to be associated with an email device.
        timeframes (:obj:`DeviceTimeframeList`, optional): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`, optional): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`, optional): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`, optional): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`, optional): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.

    Attributes:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): The type of device, EMAIL.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        email_address (str): The email address associated with the device.
            Your system administrator may restrict the domains that are allowed
            to be associated with an email device.
        timeframes (:obj:`DeviceTimeframeList`): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.
    """
    _arg_names = (
        Device._common_arg_names +
        ['email_address'] +
        Device._common_arg_opt_names)
    _attr_names = (
        Device._common_attr_names +
       ['email_address'] +
        Device._common_attr_opt_names)
    _json_names = (
        Device._common_json_names +
       ['emailAddress'] +
        Device._common_json_opt_names)
    _attr_types = (
        Device._common_attr_types +
        [str] +
        Device._common_attr_opt_types)

class VoiceDevice(Device):
    """xMatters Voice Device representation

    Voice device objects include the fields of Recipient object and 
    Device object, as well as the following fields:
    See also Device and Recipient objects.

    Reference:
        https://help.xmatters.com/xmAPI/#voice-device-object
        https://help.xmatters.com/xmAPI/?shell#device-objects
        https://help.xmatters.com/xmAPI/index.html#recipient-object

    Args:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): The type of device, VOICE.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        phone_number (str): The phone numbers associated with this device.
            The phone number uses E.164 international format including country
            code and extension.  Example: +16045551234;ext=88
        timeframes (:obj:`DeviceTimeframeList`, optional): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`, optional): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`, optional): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`, optional): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`, optional): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.

    Attributes:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): The type of device, VOICE.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        phone_number (str): The phone numbers associated with this device.
            The phone number uses E.164 international format including country
            code and extension.  Example: +16045551234;ext=88
        timeframes (:obj:`DeviceTimeframeList`): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.
    """
    _arg_names = (
        Device._common_arg_names +
        ['phone_number'] +
        Device._common_arg_opt_names)
    _attr_names = (
        Device._common_attr_names +
       ['phone_number'] +
        Device._common_attr_opt_names)
    _json_names = (
        Device._common_json_names +
       ['phoneNumber'] +
        Device._common_json_opt_names)
    _attr_types = (
        Device._common_attr_types +
        [str] +
        Device._common_attr_opt_types)

class SMSDevice(Device):
    """xMatters SMS Device representation

    SMS devices receive text messages. SMS device objects nclude the fields of
    Recipient object and Device object, as well as the following fields:
    See also Device and Recipient objects.

    Reference:
        https://help.xmatters.com/xmAPI/#SMS-device-object
        https://help.xmatters.com/xmAPI/?shell#device-objects
        https://help.xmatters.com/xmAPI/index.html#recipient-object

    Args:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): For SMS (text message) devices,
            the device type is “TEXT_PHONE”.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        phone_number (str): The phone numbers associated with this device.
            The phone number uses E.164 international format including country
            code and extension. Example: +12505551212
        timeframes (:obj:`DeviceTimeframeList`, optional): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`, optional): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`, optional): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`, optional): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`, optional): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.

    Attributes:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): For SMS (text message) devices,
            the device type is “TEXT_PHONE”.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        phone_number (str): The phone numbers associated with this device.
            The phone number uses E.164 international format including country
            code and extension. Example: +12505551212
        timeframes (:obj:`DeviceTimeframeList`): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.
    """
    _arg_names = (
        Device._common_arg_names +
        ['phone_number'] +
        Device._common_arg_opt_names)
    _attr_names = (
        Device._common_attr_names +
       ['phone_number'] +
        Device._common_attr_opt_names)
    _json_names = (
        Device._common_json_names +
       ['phoneNumber'] +
        Device._common_json_opt_names)
    _attr_types = (
        Device._common_attr_types +
        [str] +
        Device._common_attr_opt_types)

class TextPagerDevice(Device):
    """xMatters Text Pager Device representation

    Text Pager device objects include the fields of
    Recipient object and Device object, as well as the following fields:
    See also Device and Recipient objects.

    Reference:
        https://help.xmatters.com/xmAPI/#text-pager-device-object
        https://help.xmatters.com/xmAPI/#device-objects
        https://help.xmatters.com/xmAPI/index.html#recipient-object

    Args:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): For text pager devices, the device
            type is “TEXT_PAGER”.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        pin (str): The PIN code for the pager.
        two_way_device (bool): True if the pager is capable of sending a return
            message in response to a notification. False if the pager can only
            receive notifications.
        timeframes (:obj:`DeviceTimeframeList`, optional): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`, optional): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`, optional): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`, optional): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`, optional): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.

    Attributes:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): For text pager devices, the device
            type is “TEXT_PAGER”.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        pin (str): The PIN code for the pager.
        two_way_device (bool): True if the pager is capable of sending a return
            message in response to a notification. False if the pager can only
            receive notifications.
        timeframes (:obj:`DeviceTimeframeList`): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.
    """
    _arg_names = (
        Device._common_arg_names +
        ['pin', 'two_way_device'] +
        Device._common_arg_opt_names)
    _attr_names = (
        Device._common_attr_names +
       ['pin', 'two_way_device'] +
        Device._common_attr_opt_names)
    _json_names = (
        Device._common_json_names +
       ['pin', 'twoWayDevice'] +
        Device._common_json_opt_names)
    _attr_types = (
        Device._common_attr_types +
        [str, bool] +
        Device._common_attr_opt_types)

class ApplePushDevice(Device):
    """xMatters Apple Push Device representation

    Apple push devices are Apple devices such as iPhones and iPads that use the
    xMatters mobile app. Push devices are added to xMatters automatically the
    first time they are used to log on to the system. They can be retrieved but
    not created with this API.
    Apple push device objects include the fields of Recipient object and Device
    object, as well as the following fields:

    Reference:
        https://help.xmatters.com/xmAPI/#apple-push-device-object
        https://help.xmatters.com/xmAPI/?shell#device-objects
        https://help.xmatters.com/xmAPI/index.html#recipient-object

    Args:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): For Apple push devices, the device
            type is “APPLE_PUSH”.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        account_id (str): The email address associated with the device.
        apn_token (str): The APN token associated with the device.
        alert_sound (str): The alert sound associated with the device.
        sound_status (str): The sound status of the device.
        sound_threshold (str): The sound threshold of the device.
        timeframes (:obj:`DeviceTimeframeList`, optional): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`, optional): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`, optional): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`, optional): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`, optional): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.

    Attributes:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): For Apple push devices, the device
            type is “APPLE_PUSH”.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        account_id (str): The email address associated with the device.
        apn_token (str): The APN token associated with the device.
        alert_sound (str): The alert sound associated with the device.
        sound_status (str): The sound status of the device.
        sound_threshold (str): The sound threshold of the device.
        timeframes (:obj:`DeviceTimeframeList`): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.
    """
    _arg_names = (
        Device._common_arg_names +
        ['account_id', 'apn_token', 'alert_sound',
         'sound_status', 'sound_threshold'] +
        Device._common_arg_opt_names)
    _attr_names = (
        Device._common_attr_names +
        ['account_id', 'apn_token', 'alert_sound',
         'sound_status', 'sound_threshold'] +
        Device._common_attr_opt_names)
    _json_names = (
        Device._common_json_names +
        ['accountId', 'apnToken', 'alertSound',
         'soundStatus', 'soundThreshold'] +
        Device._common_json_opt_names)
    _attr_types = (
        Device._common_attr_types +
        [str, str, str, str, str] +
        Device._common_attr_opt_types)

class AndroidPushDevice(Device):
    """xMatters Android Push Device representation

    Android push devices are devices such as Android phones that use the
    xMatters mobile app. Push devices are added to xMatters automatically the
    first time they are used to log on to the system. They can be retrieved but
    not created with this API.
    Android push device objects include the fields of Recipient object and
    Device object, as well as the following fields:

    Reference:
        https://help.xmatters.com/xmAPI/#android-push-device-object
        https://help.xmatters.com/xmAPI/?shell#device-objects
        https://help.xmatters.com/xmAPI/index.html#recipient-object

    Args:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): For Android push devices, the device
            type is “ANDROID_PUSH”.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        account_id (str): The account ID of the device.
        registration_id (str): The registration ID associated with the device.
        timeframes (:obj:`DeviceTimeframeList`, optional): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`, optional): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`, optional): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`, optional): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`, optional): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.

    Attributes:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): For Android push devices, the device
            type is “ANDROID_PUSH”.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        account_id (str): The account ID of the device.
        registration_id (str): The registration ID associated with the device.
        timeframes (:obj:`DeviceTimeframeList`): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.
    """
    _arg_names = (
        Device._common_arg_names +
        ['account_id', 'registration_id'] +
        Device._common_arg_opt_names)
    _attr_names = (
        Device._common_attr_names +
        ['account_id', 'registration_id'] +
        Device._common_attr_opt_names)
    _json_names = (
        Device._common_json_names +
        ['accountId', 'registrationId'] +
        Device._common_json_opt_names)
    _attr_types = (
        Device._common_attr_types +
        [str, str] +
        Device._common_attr_opt_types)

class BlackBerryPushDevice(Device):
    """xMatters BlackBerry Push Device representation

    BlackBerry push devices are BlackBerry phones that use the xMatters mobile
    app. Push devices are added to xMatters automatically the first time they
    are used to log on to the system. They can be retrieved but not created
    with this API.
    BlackBerry push device objects include the fields of Recipient object and
    Device object, as well as the following fields:

    Reference:
        https://help.xmatters.com/xmAPI/#blackberry-push-device-object
        https://help.xmatters.com/xmAPI/?shell#device-objects
        https://help.xmatters.com/xmAPI/index.html#recipient-object

    Args:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): For Android push devices, the device
            type is “ANDROID_PUSH”.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        account_id (str): The account ID of the device.
        registration_id (str): The registration ID associated with the device.
        timeframes (:obj:`DeviceTimeframeList`, optional): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`, optional): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`, optional): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`, optional): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`, optional): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.

    Attributes:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): For Android push devices, the device
            type is “ANDROID_PUSH”.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        account_id (str): The account ID of the device.
        registration_id (str): The registration ID associated with the device.
        timeframes (:obj:`DeviceTimeframeList`): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.
    """
    _arg_names = (
        Device._common_arg_names +
        ['account_id', 'registration_id'] +
        Device._common_arg_opt_names)
    _attr_names = (
        Device._common_attr_names +
        ['account_id', 'registration_id'] +
        Device._common_attr_opt_names)
    _json_names = (
        Device._common_json_names +
        ['accountId', 'registrationId'] +
        Device._common_json_opt_names)
    _attr_types = (
        Device._common_attr_types +
        [str, str] +
        Device._common_attr_opt_types)

class FaxDevice(Device):
    """xMatters Fax Device representation

    Fax device objects include the fields of
    Recipient object and Device object, as well as the following fields:
    See also Device and Recipient objects.

    Reference:
        https://help.xmatters.com/xmAPI/#fax-device-object
        https://help.xmatters.com/xmAPI/#device-objects
        https://help.xmatters.com/xmAPI/index.html#recipient-object

    Args:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): For fax devices, the type is “FAX”.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        phone_number (str): The phone number, not including country code, for
            the fax. The phone number follows the regular expression 
            pattern ^d{5, 20}$
            Example: 4035551919 (when country code is US)
            Note: This phone number format differs from the phone number format
            used for voice, public address, and SMS devices.
        country (str): The country code of the fax device.
        timeframes (:obj:`DeviceTimeframeList`, optional): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`, optional): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`, optional): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`, optional): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`, optional): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.

    Attributes:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): For fax devices, the type is “FAX”.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        phone_number (str): The phone number, not including country code, for
            the fax. The phone number follows the regular expression 
            pattern ^d{5, 20}$
            Example: 4035551919 (when country code is US)
            Note: This phone number format differs from the phone number format
            used for voice, public address, and SMS devices.
        country (str): The country code of the fax device.
        timeframes (:obj:`DeviceTimeframeList`): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.
    """
    _arg_names = (
        Device._common_arg_names +
        ['phone_number', 'country'] +
        Device._common_arg_opt_names)
    _attr_names = (
        Device._common_attr_names +
       ['phone_number', 'country'] +
        Device._common_attr_opt_names)
    _json_names = (
        Device._common_json_names +
       ['phoneNumber', 'country'] +
        Device._common_json_opt_names)
    _attr_types = (
        Device._common_attr_types +
        [str, str] +
        Device._common_attr_opt_types)

class PublicAddressDevice(Device):
    """xMatters PA Device representation

    Public address devices are one-way broadcast devices that play voice
    notifications but do not include response options. Public address device
    objects include the fields of Recipient object and Device object, as well
    as the following fields:
    See also Device and Recipient objects.

    Reference:
        https://help.xmatters.com/xmAPI/#public-address-device-object
        https://help.xmatters.com/xmAPI/#device-objects
        https://help.xmatters.com/xmAPI/index.html#recipient-object

    Args:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): For public address devices, the 
            device type is “VOICE_IVR”.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        phone_number (str): The phone numbers associated with this device. The
            phone number uses E.164 international format including country code
            and extension. 
            Example: +15555551212;ext=838
        timeframes (:obj:`DeviceTimeframeList`, optional): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`, optional): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`, optional): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`, optional): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`, optional): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.

    Attributes:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): For public address devices, the 
            device type is “VOICE_IVR”.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        phone_number (str): The phone numbers associated with this device. The
            phone number uses E.164 international format including country code
            and extension. 
            Example: +15555551212;ext=838
        timeframes (:obj:`DeviceTimeframeList`): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.
    """
    _arg_names = (
        Device._common_arg_names +
        ['phone_number'] +
        Device._common_arg_opt_names)
    _attr_names = (
        Device._common_attr_names +
       ['phone_number'] +
        Device._common_attr_opt_names)
    _json_names = (
        Device._common_json_names +
       ['phoneNumber'] +
        Device._common_json_opt_names)
    _attr_types = (
        Device._common_attr_types +
        [str] +
        Device._common_attr_opt_types)

class GenericDevice(Device):
    """xMatters Generic Device representation

    Generic device objects include the fields of
    Recipient object and Device object, as well as the following fields:
    See also Device and Recipient objects.

    Reference:
        https://help.xmatters.com/xmAPI/#generic-device-object
        https://help.xmatters.com/xmAPI/#device-objects
        https://help.xmatters.com/xmAPI/index.html#recipient-object

    Args:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): For generic devices, the device type
            is “GENERIC”.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        pin (str): The PIN of the device.
        timeframes (:obj:`DeviceTimeframeList`, optional): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`, optional): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`, optional): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`, optional): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`, optional): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.

    Attributes:
        id (str): A unique id that represents the recipient.
        target_name (str): For devices, the target name is the user name,
            followed by the | (pipe) character, followed by the device name.
            Example: “mmcbride|Work Phone”
        receipient_type (:Enum:`RecipientType`): This object's type, "Device".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        default_device (bool): True if this device can receive notifications
            when the person has no active devices.
        delay (int): The number of minutes to wait for a response on this
            device before contacting the next device.
        description (str): A system-generated description of the device.
        device_type (:Enum:`DeviceType`): For generic devices, the device type
            is “GENERIC”.
        name (str): The name of the device.
            Example: “Work Email”, or “Home Phone”
        owner (:obj:`PersonReference`): Link to the person who owns the device.
        priority_threshold (:Enum:`PriorityThreshold`): The minimum priority
            that an event must have for it to be delivered to this device.
        provider (:obj:`ReferenceById`): The name of the provider used to send
            notifications to this device.
        sequence (str): The order in which the device will be contacted,
            where 0 represents the first device contacted.
        test_status (:Enum:`TestStatus`): Whether the device has been tested.
        pin (str): The PIN of the device.
        timeframes (:obj:`DeviceTimeframeList`): The timeframes the
            device is active and able to receive notifications. This field is
            included when the query parameter ?embed=timeframes is included in
            supported requests.
        site (:obj:`ReferencebyIdAndSelfLink`): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`): A list of fields that
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.
    """
    _arg_names = (
        Device._common_arg_names +
        ['pin'] +
        Device._common_arg_opt_names)
    _attr_names = (
        Device._common_attr_names +
        ['pin'] +
        Device._common_attr_opt_names)
    _json_names = (
        Device._common_json_names +
        ['pin'] +
        Device._common_json_opt_names)
    _attr_types = (
        Device._common_attr_types +
        [str] +
        Device._common_attr_opt_types)

def main():
    """If stand-alone"""
    pass

if __name__ == '__main__':
    main()
