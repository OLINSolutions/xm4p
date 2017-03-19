# -*- coding: utf-8 -*-
"""xmatters Recipient Objects

Recipient objects used throughout the xmatters API.

Reference:
    https://help.xmatters.com/xmAPI/index.html#recipient-object
    https://help.xmatters.com/xmAPI/index.html#dynamic-team-object
    https://help.xmatters.com/xmAPI/index.html#group-object

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from enum import Enum
import json
import logging

from xmatters import XmattersBase
from xmatters import SelfLink
from xmatters import ReferenceByIdAndSelfLink
from xmatters import Pagination
from xmatters import PaginationLinks

LOGGER = logging.getLogger('xlogger')

class RecipientPointer(XmattersBase):
    """xmatters RecipientPointer representation

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
    """xmatters PersonReference representation

    Refers to a person in xmatters.

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
    PEOPLE = "PEOPLE"
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
    """xmatters Recipient representation

    A recipient is a user, group, device or dynamic team in xmatters that can
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
    """xmatters DynamicTeam representation

    A dynamic team is a set of users that are automatically generated based on
    a common attribute such as their skills, location, or other attributes.
    Dynamic teams cannot be accessed and manipulated directly with the xmatters
    API. However, when a dynamic team is a member of a group it is included in
    the returned list of group members.
    A dynamic team is based on the Recipient object but does not include the
    status field (because dynamic teams are always active) and does not include
    the links field (because dynamic teams cannot be accessed with the xmatters
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
            cannot be modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`, optional): Whether the recipient is
            active. Inactive recipients do not receive notifications.
            Dynamic Teams are always active.
        links (:obj:`SelfLink`, optional): A link that can be used to access the
            object from within the API. This link is not included with Dynamic
            Team Recipients because they cannot yet be directly manipulated with
            this API.

    Attribute:
        id (str): A unique identifier that represents the dynamic team.
        target_name (str): The name of the dynamic team.
        recipient_type (str): For dynamic teams, this value is “DYNAMIC_TEAM”.
        externally_owned (bool): True if the object is managed by an external
            system. False by default.
            A field is externally owned when it is managed by an external
            system. Externally-owned objects cannot be deleted in the xmatters
            user interface by most users.
        external_key (str): Identifies a resource in an external system.
        use_emergency_device (bool): True if the dynamic team is configured to
            contact failsafe devices when no other devices are configured to
            receive notifications.
        locked (:obj:`list` of :obj:`str`): A list of fields that cannot be
            modified in the xmatters user interface.
        status (:Enum:`RecipientStatus`): Whether the recipient is active.
            Inactive recipients do not receive notifications.
            Dynamic Teams are always active.
        links (:obj:`SelfLink`): A link that can be used to access the object
            from within the API. 
            Not included with Dynamic Team Recipients because they cannot yet
            be directly manipulated wih this API.
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

    def __init__(self, *args, **kwargs):
        """Creates and initializes an instance.

        Args:
            *args
                Variable length argument list.
                Must follow the order of types.
            **kwargs
                Arbitrary keyword arguments.
                Must follow the appropriate type for the named arg

        Returns:
            object: An initialized instance

        Raises:
            TypeError: The type of an argument value is not correct, or
                a required argument is missing
        """
        super().__init__(*args, **kwargs)
        if self.recipient_type is None:
            self.recipient_type = RecipientType.DYNAMIC_TEAM
        if self.status is None:
            self.status = RecipientStatus.ACTIVE

class Group(Recipient):
    """xmatters Group representation

    Group objects include the fields defined in Recipient object in addition to
    fields specific to group recipients.
    To view information about group supervisors and group observers, log on to
    the xmatters user interface and view the group.
    See also Recipient object.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#recipient-object
        https://help.xmatters.com/xmAPI/index.html#group-object

    Args:

    Attributes:
        allow_duplicates (bool): True if recipients can receive more than one
            notification for the same event.
        description (str): A description of the group.
        observed_by_all (bool): True if users can locate and send notifications
            to the group regardless of their role. If this value is false, only
            users who have the selected roles can observe the group. To view or
            set the list of group observer roles, log on to the xmatters user
            interface and edit the group.
        recipient_type (str): For groups, the recipient type field is “GROUP”.
        site (:obj:`ReferencebyIdAndSelfLink`): Contains a link you can use to
            access the site the group uses for holidays.
        target_name (str): For groups, the target name is the group name.
        use_default_devices (bool): True if group recipients may be notified on
            their default device when they do not have a device with an active
            timeframe.
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build a Group instance from a JSON object

        Args:
            cls (:class:`Group`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a Group.

        Returns:
            Group: An instance populated with json_self.
        """
        new_obj = cls()
        Recipient._init_from_json_obj(new_obj, json_self)
        new_obj.allow_duplicates = (
            json_self['allowDuplicates']
            if 'allowDuplicates' in json_self else None)
        new_obj.description = (
            json_self['description'] if 'description' in json_self else None)
        new_obj.observed_by_all = (
            json_self['observedByAll']
            if 'observedByAll' in json_self else None)
        new_obj.site = (
            ReferenceByIdAndSelfLink.from_json_obj(json_self['site'])
            if 'site' in json_self else ReferenceByIdAndSelfLink())
        new_obj.use_default_devices = (
            json_self['useDefaultDevices']
            if 'useDefaultDevices' in json_self else None)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build a Group instance from a JSON payload string

        Args:
            cls (:class:`Group`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a Group.

        Returns:
            Group: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self):
        super().__init__()
        self.recipient_type = "GROUP"
        self.allow_duplicates: bool = None
        self.description: str = None
        self.observed_by_all: bool = None
        self.site: ReferenceByIdAndSelfLink = None
        self.use_default_devices: bool = None

class Role(object):
    """xmatters Role representation

    Refers to a role in xmatters.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#role-object

    Args:

    Attributes:
        id (str): The unique identifier of the role.
        name (str): The name of the role.
    """

    @staticmethod
    def from_role_array(role_array: []):
        """Build an array of Role instances from a JSON object

        Args:
            json_array (:obj:`list` of :obj:`JSON`): JSON array of Roles.

        Returns:
            list: Array of Roles from json_array.
        """
        roles = []
        for role in role_array:
            roles.append(Role.from_json_obj(role))
        return roles

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build a Role instance from a JSON object

        Args:
            cls (:class:`Role`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a Role.

        Returns:
            Role: An instance populated with json_self.
        """
        new_obj = cls()
        new_obj.id = json_self['id'] if 'id' in json_self else None
        new_obj.id = json_self['name'] if 'name' in json_self else None
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build a Role instance from a JSON payload string

        Args:
            cls (:class:`Role`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a Role.

        Returns:
            Role: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self):
        self.id: str = None
        self.name: str = None

class RolePagination(Pagination):
    """xmatters Pagination of Role object

    Reference:
        https://help.xmatters.com/xmAPI/index.html#role-object
        https://help.xmatters.com/xmAPI/index.html#pagination-object

    Args:

    Attributes:
        count (int): The number of items in this page of results.
        data (:obj:`list` of :obj:`Role`): An array of the paginated object.
        links (:obj:`PaginationLinks`): Links to the current, previous, and
            next pages of results.
        total (int): The total number of items in the result set.

    """
    @classmethod
    def from_json_obj(cls, json_self: object):
        """Creates and initializes an instance of a RolePagination.

        Args:
            cls (:class:`RolePagination`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a RolePagination.

        Returns:
            RolePagination: An instance populated with json_self.
        """
        new_obj = cls(
            json_self['count'] if 'count' in json_self else None,
            (Role.from_role_array(json_self['data']) if 'data' in json_self
             else []),
            (PaginationLinks.from_json_obj(json_self['links'])
             if 'links' in json_self else PaginationLinks()),
            json_self['total'] if 'self' in json_self else None)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Creates and initializes an instance of a Pagination.

        Args:
            cls (:class:`Pagination`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a Pagination.

        Returns:
            Pagination: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(
            self, rp_count: int = None, rp_data: [] = None,
            rp_links: PaginationLinks = None, rp_total: int = None):
        super().__init__(rp_count, None, rp_links, rp_total)
        self.data = rp_data

class Person(Recipient):
    """xmatters Person representation

    Describes a person in xmatters. A person object is a Recipient object with
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

    Attributes:
        first_name (str): The first name of the person.
        language (str): The person’s default language.
        last_name (str): The last name of the person.
        phone_login (str): An access code that the person can use to identify
            themselves when they phone in to xmatters to retrieve messages.
        properties (:obj:`JSON`): A list of the custom fields and attributes
            that are defined for this person.
        roles (:obj:`RolePagination`, optional): A list of the user’s roles.
            This optional field is included when the request uses the
            ?embed=roles query parameter.
        site (:obj:`ReferenceByIdAndSelfLink`): A link to a resource that you
            can use to find out information about the site to which the
            person is assigned.
        timezone (str): The person’s time zone. Example: “US/Eastern”
        web_login (str): The identifier the person can use to log in to the
            xmatters user interface. This is often identical to the
            targetName value.
    """

    @classmethod
    def from_json_obj(cls, json_self: object):
        """Build a Person instance from a JSON object

        Args:
            cls (:class:`Person`): Class to instantiate.
            json_self (:obj:`JSON`): JSON object of a Person.

        Returns:
            Person: An instance populated with json_self.
        """
        new_obj = cls()
        Recipient._init_from_json_obj(new_obj, json_self)
        new_obj.first_name = (
            json_self['firstName']
            if 'firstName' in json_self else None)
        new_obj.language = (
            json_self['language'] if 'language' in json_self else None)
        new_obj.last_name = (
            json_self['lastName']
            if 'lastName' in json_self else None)
        new_obj.phone_login = (
            json_self['phoneLogin']
            if 'phoneLogin' in json_self else None)
        new_obj.properties = (
            json_self['properties']
            if 'properties' in json_self else None)
        new_obj.roles = (
            RolePagination.from_json_obj(json_self['roles'])
            if 'roles' in json_self else RolePagination())
        new_obj.site = (
            ReferenceByIdAndSelfLink.from_json_obj(json_self['site'])
            if 'site' in json_self else ReferenceByIdAndSelfLink())
        new_obj.timezone = (
            json_self['timezone']
            if 'timezone' in json_self else None)
        new_obj.web_login = (
            json_self['webLogin']
            if 'webLogin' in json_self else None)
        return new_obj

    @classmethod
    def from_json_str(cls, json_self: str):
        """Build a Person instance from a JSON payload string

        Args:
            cls (:class:`Person`): Class to instantiate.
            json_self (:str:`JSON`): JSON string of a Person.

        Returns:
            Person: An instance populated with json_self.
        """
        obj = json.loads(json_self)
        return cls.from_json_obj(obj)

    def __init__(self):
        super().__init__()
        self.recipient_type = "PERSON"
        self.first_name: str = None
        self.language: str = None
        self.last_name: str = None
        self.phone_login: str = None
        self.properties = []
        self.roles = RolePagination()
        self.site: ReferenceByIdAndSelfLink = None
        self.timezone = None
        self.web_login = None

def main():
    """In case we ever need to run this stand-alone"""
    pass

if __name__ == '__main__':
    main()
