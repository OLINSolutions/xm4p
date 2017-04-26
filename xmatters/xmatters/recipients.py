# -*- coding: utf-8 -*-
"""xMatters Recipient Objects

Recipient objects used throughout the xMatters API.

Reference:
    https://help.xmatters.com/xmAPI/index.html#recipient-object
    https://help.xmatters.com/xmAPI/index.html#dynamic-team-object
    https://help.xmatters.com/xmAPI/index.html#group-object

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from enum import Enum
import logging

from xmatters import XmattersBase
from xmatters import XmattersList
from xmatters import SelfLink
from xmatters import ReferenceByIdAndSelfLink
from xmatters import Pagination
from xmatters import PaginationLinks

LOGGER = logging.getLogger('xlogger')

class RecipientPointer(XmattersBase):
    """xMatters RecipientPointer representation

    A reference to a recipient.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#recipientpointer-object

    Args:
        id (str): The unique identifier or target name of the
            group member.
        recipient_type (str, optional): The type of the group member.

    Attributes:
        id (str): The unique identifier or target name of the group member.
        recipient_type (str, optional): The type of the group member.
            Providing this optional field allows xmatters to process your
            request more efficiently and improves performance.
            Use one of the following values:
            “PERSON”
            “GROUP”
            “DEVICE”
    """
    _arg_names = ['id', '*recipient_type']
    _attr_names = ['id', 'recipient_type']
    _json_names = ['id', 'recipientType']
    _attr_types = [str, str]


class PersonReference(XmattersBase):
    """xMatters PersonReference representation

    Refers to a person in xMatters.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#person-reference-object

    Args:
        id (str): The unique identifier of the person.
        target_name (str): The user id of the person.
        links (:obj:`SelfLink`): A link that can be used to retrieve the person
            using this API.

    Attributes:
        id (str): The unique identifier of the person.
        target_name (str): The user id of the person.
        links (:obj:`SelfLink`): A link that can be used to retrieve the person
            using this API.
    """
    _arg_names = _attr_names = ['id', 'target_name', 'links']
    _json_names = ['id', 'targetName', 'links']
    _attr_types = [str, str, SelfLink]

class RecipientType(Enum):
    """The type of a Recipient object"""
    GROUP = "GROUP"
    PERSON = "PERSON"
    DEVICE = "DEVICE"
    DYNAMIC_TEAM = "DYNAMIC_TEAM"

class RecipientStatus(Enum):
    """The status of a Recipient object

    Whether the recipient is active. Inactive recipients do not receive
    notifications. Use one of the following values.
    """
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class Recipient(XmattersBase):
    """xMatters Recipient representation

    A recipient is a user, group, device or dynamic team in xMatters that can
    receive notifications. The recipient object provides a base for Group
    object, Device object, Person object, and Dynamic team object.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#recipient-object

    Args:
        id (str): A unique id that represents the recipient.
        target_name (str): The common name of the recipient.
        receipient_type (:Enum:`RecipientType`): The type of this object.
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
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
        id (str): A unique identifier that represents the recipient.
        target_name (str): The common name of the recipient.
        receipient_type (:Enum:`RecipientType`): The type of this object.
        externally_owned (bool): True if the object is managed by an external
            system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        external_key (str): Identifies a resource in an external system.
        locked (:obj:`list` of :obj:`str`): A list of fields that cannot be
            modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`): Whether the recipient is active.
            Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`): A link that can be used to access the object
            from within the API. This link is not included with Dynamic Team
            Recipients because they cannot yet be directly manipulated with
            this API.
    """
    _common_arg_names = [
        'id', 'target_name', 'recipient_type', 'externally_owned']
    _common_arg_opt_names = ['*external_key', '*locked', '*status', '*links']
    _arg_names = _common_arg_names + _common_arg_opt_names
    _common_attr_names = [
        'id', 'target_name', 'recipient_type', 'externally_owned']
    _common_attr_opt_names = ['external_key', 'locked', 'status', 'links']
    _attr_names = _common_attr_names + _common_attr_opt_names
    _common_json_names = [
        'id', 'targetName', 'recipientType', 'externallyOwned']
    _common_json_opt_names = ['externalKey', 'locked', 'status', 'links']
    _json_names = _common_json_names + _common_json_opt_names
    _common_attr_types = [str, str, RecipientType, bool]
    _common_attr_opt_types = [str, list, RecipientStatus, SelfLink]
    _attr_types =_common_attr_types + _common_attr_opt_types

class DynamicTeam(Recipient):
    """xMatters DynamicTeam representation

    A dynamic team is a set of users that are automatically generated based on
    a common attribute such as their skills, location, or other attributes.
    Dynamic teams cannot be accessed and manipulated directly with the xMatters
    API. However, when a dynamic team is a member of a group it is included in
    the returned list of group members.
    A dynamic team is based on the Recipient object but does not include the
    status field (because dynamic teams are always active) and does not include
    the links field (because dynamic teams cannot be accessed with the xMatters
    API).

    Reference:
        https://help.xmatters.com/xmAPI/index.html#recipient-object
        https://help.xmatters.com/xmAPI/index.html#dynamic-team-object

    Args:
        id (str): A unique id that represents the recipient.
        target_name (str): The common name of the recipient.
        receipient_type (:Enum:`RecipientType`): The type of this object.
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        use_emergency_device (bool): True if the dynamic team is configured to
            contact failsafe devices when no other devices are configured to
            receive notifications.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`, optional): A list of fields that
            cannot be modified in the xMatters user interface.
        status (:Enum:`RecipientStatus`, optional): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Dynamic Teams are always active.
        links (:obj:`SelfLink`, optional): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.

    Attribute:
        recipient_type (str): For dynamic teams, this value is “DYNAMIC_TEAM”.
            (Property overridden.)
        status (:Enum:`RecipientStatus`, optional): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Dynamic Teams are always active.
            (Property overridden.)
        use_emergency_device (bool): True if the dynamic team is configured to
            contact failsafe devices when no other devices are configured to
            receive notifications.
    """
    _arg_names = (
        Recipient._common_arg_names + ['use_emergency_device'] +
        Recipient._common_arg_opt_names)
    _attr_names = (
        Recipient._common_attr_names + ['use_emergency_device'] +
        Recipient._common_attr_opt_names)
    _json_names = (
        Recipient._common_json_names + ['useEmergencyDevice'] +
        Recipient._common_json_opt_names)
    _attr_types = (
        Recipient._common_attr_types + [bool] +
        Recipient._common_attr_opt_types)

    @property
    def recipient_type(self) -> RecipientType:
        """:obj:`RecipientType`: Always DYNAMIC_TEAM"""
        return RecipientType.DYNAMIC_TEAM

    @recipient_type.setter
    def recipient_type(self, value):
        """Ignore, don't do anything with value"""
        pass

    @property
    def status(self) -> RecipientStatus:
        """:obj:`RecipientStatus`: Always ACTIVE"""
        return RecipientStatus.ACTIVE

    @status.setter
    def status(self, value):
        """Ignore, don't do anything with value"""
        pass

class Group(Recipient):
    """xMatters Group representation

    Group objects include the fields defined in Recipient object in addition to
    fields specific to group recipients.
    To view information about group supervisors and group observers, log on to
    the xMatters user interface and view the group.
    See also Recipient object.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#recipient-object
        https://help.xmatters.com/xmAPI/index.html#group-object

    Args:
        id (str): A unique id that represents the recipient.
        target_name (str): The Group name.
        receipient_type (:Enum:`RecipientType`): This object's type, "Group".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xMatters
            user interface by most users.
        allow_duplicates (bool): True if recipients can receive more than one
            notification for the same event.
        description (str): A description of the group.
        observed_by_all (bool): True if users can locate and send notifications
            to the group regardless of their role. If this value is false, only
            users who have the selected roles can observe the group. To view or
            set the list of group observer roles, log on to the xMatters user
            interface and edit the group.
        use_default_devices (bool): True if group recipients may be notified on
            their default device when they do not have a device with an active
            timeframe.
        site (:obj:`ReferencebyIdAndSelfLink`, optional): Contains a link you
            can use to access the site the group uses for holidays.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`, optional): A list of fields that
            cannot be modified in the xMatters user interface.
        status (:Enum:`RecipientStatus`, optional): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`, optional): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.

    Attributes:
        allow_duplicates (bool): True if recipients can receive more than one
            notification for the same event.
        description (str): A description of the group.
        observed_by_all (bool): True if users can locate and send notifications
            to the group regardless of their role. If this value is false, only
            users who have the selected roles can observe the group. To view or
            set the list of group observer roles, log on to the xmatters user
            interface and edit the group.
        use_default_devices (bool): True if group recipients may be notified on
            their default device when they do not have a device with an active
            timeframe.
        site (:obj:`ReferencebyIdAndSelfLink`): Contains a link you can use to
            access the site the group uses for holidays.
    """
    _arg_names = (
        Recipient._common_arg_names +
        ['allow_duplicates', 'description', 'observed_by_all',
         'use_default_devices', '*site'] +
        Recipient._common_arg_opt_names)
    _attr_names = (
        Recipient._common_attr_names +
       ['allow_duplicates', 'description', 'observed_by_all',
         'use_default_devices', 'site'] +
        Recipient._common_attr_opt_names)
    _json_names = (
        Recipient._common_json_names +
       ['allowDuplicates', 'description', 'observedByAll',
         'useDefaultDevices', 'site'] +
        Recipient._common_json_opt_names)
    _attr_types = (
        Recipient._common_attr_types +
        [bool, str, bool, bool, ReferenceByIdAndSelfLink] +
        Recipient._common_attr_opt_types)

class Role(XmattersBase):
    """xMatters Role representation

    Refers to a role in xMatters.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#role-object

    Args:
        id (str): The unique identifier of the role.
        name (str): The name of the role.

    Attributes:
        id (str): The unique identifier of the role.
        name (str): The name of the role.
    """
    _arg_names = _attr_names = _json_names = ['id', 'name']
    _attr_types = [str, str]

class RoleList(XmattersList):
    """xMatters Role list representation

    Defines a Python list that also adds a member_type element to hold the
    XmattersBase subclass that represents the type of member

    Attributes:
        base_class (:obj:`class`): Type of XmatterBase subclass held in list
    """
    base_class = Role

class RolePagination(Pagination):
    """xMatters Pagination of Role object

    Reference:
        https://help.xmatters.com/xmAPI/index.html#role-object
        https://help.xmatters.com/xmAPI/index.html#pagination-object

    Args:
        count (int): The number of items in this page of results.
        total (int): The total number of items in the result set.
        data (:obj:`RoleList`): A list of Role objects.
        links (:obj:`PaginationLinks`, optional): Links to the current,
            previous, and next pages of results.

    Attributes:
        count (int): The number of items in this page of results.
        total (int): The total number of items in the result set.
        data (:obj:`RoleList`): A list of Role objects.
        links (:obj:`PaginationLinks`): Links to the current, previous, and
            next pages of results.

    """
    _arg_names = ['count', 'total', 'data', '*links']
    _attr_names = _json_names = ['count', 'total', 'data', 'links']
    _attr_types = [int, int, RoleList, PaginationLinks]

class Person(Recipient):
    """xMatters Person representation

    Describes a person in xMatters. A person object is a Recipient object with
    a recipientType of PERSON.
    A Person object contains the attributes of the Recipient object as well as
    the attributes described here.
    The Person object includes a list of the person’s roles when the
    ?embed=roles query parameter is used with the request.
    See also: Recipient object.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#recipient-object
        https://help.xmatters.com/xmAPI/index.html#person-object

    Args:
        id (str): A unique id that represents the recipient.
        target_name (str): The user's targeted identifier.
        receipient_type (:Enum:`RecipientType`): This object's type, "Person".
        externally_owned (bool): True if the object is managed by an
            external system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xMatters
            user interface by most users.
        first_name (str): The first name of the person.
        last_name (str): The last name of the person.
        language (str): The person’s default language.
        timezone (str): The person’s time zone. Example: “US/Eastern”
        web_login (str): The identifier the person can use to log in to the
            xMatters user interface. This is often identical to the
            targetName value.
        site (:obj:`ReferenceByIdAndSelfLink`): A link to a resource that you
            can use to find out information about the site to which the
            person is assigned.
        phone_login (str, optional): An access code that the person can use to
            identify themselves when they phone in to xMatters to retrieve
            messages.
        properties (dict, optional): A list of the custom fields and
            attributes that are defined for this person.
        roles (:obj:`RolePagination`, optional): A list of the user’s roles.
            This optional field is included when the request uses the
            ?embed=roles query parameter.
        external_key (str, optional): Ids a resource in an external system.
        locked (:obj:`list` of :obj:`str`, optional): A list of fields that
            cannot be modified in the xMatters user interface.
        status (:Enum:`RecipientStatus`, optional): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Note: this field is not included with dynamic teams because they
            are always active.
        links (:obj:`SelfLink`, optional): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.

    Attributes:
        first_name (str): The first name of the person.
        last_name (str): The last name of the person.
        language (str): The person’s default language.
        timezone (str): The person’s time zone. Example: “US/Eastern”
        web_login (str): The identifier the person can use to log in to the
            xMatters user interface. This is often identical to the
            targetName value.
        site (:obj:`ReferenceByIdAndSelfLink`): A link to a resource that you
            can use to find out information about the site to which the
            person is assigned.
        phone_login (str): An access code that the person can use to identify
            themselves when they phone in to xMatters to retrieve messages.
        properties (dict): A list of the custom fields and attributes
            that are defined for this person.
        roles (:obj:`RolePagination`): A list of the user’s roles.
            This optional field is included when the request uses the
            ?embed=roles query parameter.
    """
    _arg_names = (
        Recipient._common_arg_names +
        ['first_name', 'last_name', 'language', 'timezone', 'web_login',
         'site', '*phone_login', '*properties', '*roles'] +
        Recipient._common_arg_opt_names)
    _attr_names = (
        Recipient._common_attr_names +
        ['first_name', 'last_name', 'language', 'timezone', 'web_login',
         'site', 'phone_login', 'properties', 'roles'] +
        Recipient._common_attr_opt_names)
    _json_names = (
        Recipient._common_json_names +
       ['firstName', 'lastName', 'language', 'timezone', 'webLogin',
        'site', 'phoneLogin', 'properties', 'roles'] +
        Recipient._common_json_opt_names)
    _attr_types = (
        Recipient._common_attr_types +
        [str, str, str, str, str,
         ReferenceByIdAndSelfLink, str, dict, RolePagination] +
        Recipient._common_attr_opt_types)

def main():
    """If stand-alone"""
    pass

if __name__ == '__main__':
    main()
