"""xmatters Event

This class represents a view of the xmatters Event that is created as part of a
request for a notification to occur.  The Event class contains both controlling
methods (typically static) for retrieving a list of Event instances, as well as
methods for manipulating instances of events.

Ref:
    https://help.xmatters.com/xmAPI/index.html#event-objects

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from enum import Enum
import logging

from xmatters import Pagination
from xmatters import PaginationLinks
from xmatters import PersonReference
from xmatters import Recipient
from xmatters import ReferenceById
from xmatters import XmattersBase
from xmatters import XmattersList

LOGGER = logging.getLogger('xlogger')

class EventStatus(Enum):
    """The status of an Event object

    The current status of this event. Use one of the following values.
    """
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    TERMINATED = "TERMINATED"
    TERMINATED_EXTERNAL = "TERMINATED_EXTERNAL"

class EventPriority(Enum):
    """The priority of an Event object

    The priority of the event. Use one of the following values.
    """
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class ConferenceHostType(Enum):
    """The hosting type for an xMatters Conference object.

    Whether the conference bridge is an xMatters-hosted conference bridge or
    hosted by a third-party provider.
        BRIDGE : for xMatters-hosted bridges
        EXTERNAL: for externally-hosted bridges

    Reference:
        https://help.xmatters.com/xmAPI/index.html#conference-object
    """
    BRIDGE = "BRIDGE"
    EXTERNAL = "EXTERNAL"

class ResponseAction(Enum):
    """The Response Option Action choices.

    The action to take when this response option is chosen.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#response-option-object
    """
    RECORD_RESPONSE = "RECORD_RESPONSE"
    STOP_NOTIFYING_USER = "STOP_NOTIFYING_USER"
    STOP_NOTIFYING_TARGET = "STOP_NOTIFYING_TARGET"
    ESCALATE = "ESCALATE"
    ASSIGN_TO_USER = "ASSIGN_TO_USER"
    END = "END"

class ResponseContribution(Enum):
    """The Response Option Contribution choices.

    How to classify this response.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#response-option-object
    """
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"
    NONE = "NONE"

class RecipientList(XmattersList):
    """xMatters Recipient list representation

    Defines a Python list that also adds a member_type element to hold the
    XmattersBase subclass that represents the type of member

    Attributes:
        base_class (:obj:`class`): Type of XmatterBase subclass held in list
    """
    base_class = Recipient

class RecipientPagination(Pagination):
    """xMatters Pagination of Recipient object

    Reference:
        https://help.xmatters.com/xmAPI/index.html#recipient-object
        https://help.xmatters.com/xmAPI/index.html#pagination-object

    Args:
        count (int): The number of items in this page of results.
        total (int): The total number of items in the result set.
        data (:obj:`RecipientList`): A list of Recipient objects.
        links (:obj:`PaginationLinks`, optional): Links to the current,
            previous, and next pages of results.

    Attributes:
        count (int): The number of items in this page of results.
        total (int): The total number of items in the result set.
        data (:obj:`RecipientList`): A list of Recipient objects.
        links (:obj:`PaginationLinks`): Links to the current, previous, and
            next pages of results.

    """
    _arg_names = ['count', 'total', 'data', '*links']
    _attr_names = _json_names = ['count', 'total', 'data', 'links']
    _attr_types = [int, int, RecipientList, PaginationLinks]

class FormReference(ReferenceById):
    """xMatters FormReference representation

    Provides the unique identifier of a form.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#form-reference-object

    Args:
        id (str): The unique identifier of the form.

    Attributes:
        id (str): The unique identifier of the form.
    """
    pass

class Conference(XmattersBase):
    """xMatters Conference object

    The Conference object describes xMatters-hosted and externally-hosted
    conference bridges associated with an event.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#conference-object

    Args:
        bridge_id (str): For xMatters-hosted bridges, this field contains the
            xMatters bridge number. For externally-hosted conference bridges,
            this field contains the name of the external conference bridge.
        type (:Enum:`ConferenceHostType`): Whether the conference bridge is an
            xMatters-hosted conference bridge or hosted by a third-party
            provider. Use one of the following values:
                ConferenceHostType.BRIDGE: for xMatters-hosted bridges
                ConferenceHostType.EXTERNAL: for externally-hosted bridges

    Attributes:
        bridge_id (str): For xMatters-hosted bridges, this field contains the
            xMatters bridge number. For externally-hosted conference bridges,
            this field contains the name of the external conference bridge.
        type (:Enum:`ConferenceHostType`): Whether the conference bridge is an
            xMatters-hosted conference bridge or hosted by a third-party
            provider. Use one of the following values:
                ConferenceHostType.BRIDGE: for xMatters-hosted bridges
                ConferenceHostType.EXTERNAL: for externally-hosted bridges
    """
    _arg_names = _attr_names = ['bridge_id', 'type']
    _json_names = ['bridgeId', 'type']
    _attr_types = [str, ConferenceHostType]

class ResponseOption(XmattersBase):
    """xMatters ResponseOption object

    The ResponseOption object describes the response options that are included
    in the event.

    Reference:
        https://help.xmatters.com/xmAPI/index.html#response-option-object

    Args:
        text (str): The response option displayed on text devices and as a
            link in email messages.
        description (str): A description of the response to be included in
            email messages.
        prompt (str): A phrase that is read aloud using text-to-speech
            translation for voice messages.
        number (int): The keypad digit associated with this response, used when
            responding to to voice notifications on a touch-tone phone.
        join_conference (bool): True if selecting this response from a touch-
            tone phone automatically connects you to the conference bridge.
        action (:Enum:`ResponseAction`): The action to take when this response
            option is chosen. Use one of the following values:
                ResponseAction.RECORD_RESPONSE
                ResponseAction.STOP_NOTIFYING_USER
                ResponseAction.STOP_NOTIFYING_TARGET
                ResponseAction.ESCALATE
                ResponseAction.ASSIGN_TO_USER
                ResponseAction.END
        contribution (:Enum:`ResponseContribution`): How to classify this
            response. Use one of the following values:
                ResponseContribution.POSITIVE
                ResponseContribution.NEGATIVE
                ResponseContribution.NEUTRAL
                ResponseContribution.NONE

    Attributes:
        text (str): The response option displayed on text devices and as a
            link in email messages.
        description (str): A description of the response to be included in
            email messages.
        prompt (str): A phrase that is read aloud using text-to-speech
            translation for voice messages.
        number (int): The keypad digit associated with this response, used when
            responding to to voice notifications on a touch-tone phone.
        join_conference (bool): True if selecting this response from a touch-
            tone phone automatically connects you to the conference bridge.
        action (:Enum:`ResponseAction`): The action to take when this response
            option is chosen. Use one of the following values:
                ResponseAction.RECORD_RESPONSE
                ResponseAction.STOP_NOTIFYING_USER
                ResponseAction.STOP_NOTIFYING_TARGET
                ResponseAction.ESCALATE
                ResponseAction.ASSIGN_TO_USER
                ResponseAction.END
        contribution (:Enum:`ResponseContribution`): How to classify this
            response. Use one of the following values:
                ResponseContribution.POSITIVE
                ResponseContribution.NEGATIVE
                ResponseContribution.NEUTRAL
                ResponseContribution.NONE
    """
    _arg_names = _attr_names = [
        'text', 'description', 'prompt', 'number', 'join_conference', 'action',
        'contribution']
    _json_names = [
        'text', 'description', 'prompt', 'number', 'joinConference', 'action',
        'contribution']
    _attr_types = [
        str, str, str, int, bool, ResponseAction, ResponseContribution]

class ResponseOptionList(XmattersList):
    """xMatters ResponseOption list representation

    Defines a Python list that also adds a member_type element to hold the
    XmattersBase subclass that represents the type of member

    Attributes:
        base_class (:obj:`class`): Type of XmatterBase subclass held in list
    """
    base_class = ResponseOption

class ResponseOptionPagination(Pagination):
    """xMatters Pagination of ResponseOption objects

    Reference:
        https://help.xmatters.com/xmAPI/index.html#response-option-object
        https://help.xmatters.com/xmAPI/index.html#pagination-object

    Args:
        count (int): The number of items in this page of results.
        total (int): The total number of items in the result set.
        data (:obj:`ResponseOptionList`): A list of ResponseOption objects.
        links (:obj:`PaginationLinks`, optional): Links to the current,
            previous, and next pages of results.

    Attributes:
        count (int): The number of items in this page of results.
        total (int): The total number of items in the result set.
        data (:obj:`ResponseOptionList`): A list of ResponseOption objects.
        links (:obj:`PaginationLinks`): Links to the current, previous, and
            next pages of results.

    """
    _arg_names = ['count', 'total', 'data', '*links']
    _attr_names = _json_names = ['count', 'total', 'data', 'links']
    _attr_types = [int, int, ResponseOptionList, PaginationLinks]

class Event(XmattersBase):
    """xMatters Event representation

    This class represents a view of the xMatters Event that is created as part
    of a request for a notification to occur.  The Event class contains both
    controlling methods (typically static) for retrieving a list of Event
    instances, as well as methods for manipulating instances of events.

    Reference:
        See https://help.xmatters.com/xmAPI/index.html#event-object
    Args:
        id (str): The unique identifier of this event (UUID).
        event_id (str): The integer identifier used to identify this event in
            the xMatters user interface.
        created (str): The date and time the event was initiated
            (in UTC format)
            Standard used: https://www.w3.org/TR/xmlschema11-2/#dateTime.
        status (:Enum:`EventStatus`): The current status of this event.
            Use one of the following values:
            EventStatus.ACTIVE
            EventStatus.SUSPENDED
            EventStatus.TERMINATED
            EventStatus.“TERMINATED_EXTERNAL”
        priority (:Enum:`EventPriority`): The priority of the event.
            Use one of the following values:
            EventPriority.LOW
            EventPriority.MEDIUM
            EventPriority.HIGH
        incident (str): The incident ID of the event.
        expiration_in_minutes (int): The number of minutes the event is active
            before it terminates.
        submitter (:obj:`PersonReference`): The user who initiated the event.
        recipients (:obj:`RolePagination`): The recipients of the event. This
            attribute contains only the first page of results
            (up to 100 recipients).
        form (:obj:`FormReference`): The identifier of the form.
        terminated (str, optional): The date and time the event was terminated
            (in UTC format). This field is only present for terminated events.
            Standard used: https://www.w3.org/TR/xmlschema11-2/#dateTime.
        conference (:obj:`Conference`, optional): Describes the conference
            bridge used with this event.
        response_options (:obj:`ResponseOptionPagination`, optional):
            The response options included with this event.

    Attributes:
        id (str): The unique identifier of this event (UUID).
        event_id (str): The integer identifier used to identify this event in
            the xMatters user interface.
        created (str): The date and time the event was initiated
            (in UTC format)
            Standard used: https://www.w3.org/TR/xmlschema11-2/#dateTime.
        status (:Enum:`EventStatus`): The current status of this event.
            Use one of the following values:
            EventStatus.ACTIVE
            EventStatus.SUSPENDED
            EventStatus.TERMINATED
            EventStatus.“TERMINATED_EXTERNAL”
        priority (:Enum:`EventPriority`): The priority of the event.
            Use one of the following values:
            EventPriority.LOW
            EventPriority.MEDIUM
            EventPriority.HIGH
        incident (str): The incident ID of the event.
        expiration_in_minutes (int): The number of minutes the event is active
            before it terminates.
        submitter (:obj:`PersonReference`): The user who initiated the event.
        recipients (:obj:`RolePagination`): The recipients of the event. This
            attribute contains only the first page of results
            (up to 100 recipients).
        form (:obj:`FormReference`): The identifier of the form.
        terminated (str, optional): The date and time the event was terminated
            (in UTC format). This field is only present for terminated events.
            Standard used: https://www.w3.org/TR/xmlschema11-2/#dateTime.
        conference (:obj:`Conference`, optional): Describes the conference
            bridge used with this event.
        response_options (:obj:`ResponseOptionPagination`, optional):
            The response options included with this event.
    """
    _arg_names = [
        'id', 'event_id', 'created', 'status', 'priority', 'incident',
        'expiration_in_minutes', 'submitter', 'recipients', 'form',
        '*terminated', '*conference', '*response_options']
    _attr_names = [
        'id', 'event_id', 'created', 'status', 'priority', 'incident',
        'expiration_in_minutes', 'submitter', 'recipients', 'form',
        'terminated', 'conference', 'response_options']
    _json_names = [
        'id', 'eventId', 'created', 'status', 'priority', 'incident',
        'expirationInMinutes', 'submitter', 'recipients', 'form',
        'terminated', 'conference', 'responseOptions']
    _attr_types = [
        str, str, str, EventStatus, EventPriority, str, int, PersonReference,
        RecipientPagination, FormReference, str, Conference,
        ResponseOptionPagination]

def main():
    """In case we ever need to run as a standalone module"""
    pass

if __name__ == '__main__':
    main()
