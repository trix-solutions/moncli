import json, warnings
from moncli.entities.base import BaseCollection

from schematics.models import Model
from schematics.types import StringType, BooleanType, IntType, DictType, ListType, ModelType


class MondayClientCredentials():
    """monday.com client credentials.
    
    Properties

        api_key_v1 : `str`
            The access key for monday.com API v1.
        api_key_v2 : `str`
            The access key for monday.com API v2.
    """

    def __init__(self, api_key_v1: str = None, api_key_v2: str = None):
        self.api_key_v1 = api_key_v1
        self.api_key_v2 = api_key_v2


class ActivityLog(Model):
    """monday.com client credentials.
    
    Properties

        account_id : `str`
            The user's payment account.
        created_at : `str`
            The activity log's created date.
        data : `str`
            The item's column values in string form.
        entity : `str`
            The monday.com object being updated.
        id : `str`
            The activity log's unique identifier.
        user_id : `str`
            The user who performed the change.
    """

    id = StringType(required=True)
    account_id = StringType()
    created_at = StringType()
    data = StringType()
    entity = StringType()
    event = StringType()
    user_id = StringType()

    def __repr__(self):
        return str(self.to_primitive())

class BoardView(Model):
    """A board's view.

    Properties

        id : `str`
            The view's unique identifier.
        name : `str`
            The view's name.
        settings_str : `str`
            The view's settings in a string from.
        type : `str`
            The view's type.
    """

    id = StringType(required=True)
    name = StringType()
    settings_str = StringType()
    type = StringType()

    def __repr__(self):
        return str(self.to_primitive())


class Notification(Model):
    """A notification.

    Properties

        id : `str`
            The notification`s unique identifier.
        text : `str`
            the notification text.
    """

    id = StringType(required=True)
    text = StringType()

    def __repr__(self):
        return str(self.to_primitive())


class Tag(Model):
    """A tag.

    Properties

        color : `str`
            The tag's color.
        id : `str`
            The tag's unique identifier.
        name : `str`
            The tag's name.
    """

    id = StringType(required=True)
    name = StringType()
    color = StringType()

    def __repr__(self):
        return str(self.to_primitive())


class Plan(Model):
    """ A payment plan.
    
    Properties

        max_users : `int`
            The maximum users allowed in the plan.
        period : `str`
            The plan's time period.
        tier : `str`
            The plan's tier.
        version : `int`
            The plan's version.
    """

    max_users = IntType()
    period = StringType()
    tier = StringType()
    version = IntType()

    def __repr__(self):
        return str(self.to_primitive())


class Webhook(Model):
    """ Monday webhooks

    Properties

        board_id : `str`
            The webhook's board id.
        id : `str`
            The webhook's unique identifier.
        is_active : `bool`
            If the webhook is still active.
    """

    id = StringType(required=True)
    board_id = StringType()
    is_active = BooleanType(default=False)

    def __repr__(self):
        return str(self.to_primitive())


class Workspace(Model):
    """ A monday.com workspace

    Properties

        description : `str`
            The workspace's description.
        id : `int`
            The workspace`s unique identifier.
        kind : `moncli.enums.WorkspaceKind`
            The workspace's kind (open / closed).
        name : `str`
            The workspace's name.
    """
    id = StringType(required=True)
    name = StringType()
    kind = StringType()
    description = StringType()

    def __repr__(self):
        return str(self.to_primitive())


class StatusSettings(Model):
    """The settings of a status column

    Properties

        labels : `str`
            The index / label parings of a status column option.
        labels_colors : `dict`
            The index / color property parings of a status column option.
        labels_positions_v2 : `dict`
            The position of each label by ID.

    Methods

        get_index : `str`
            Get the label ID from the label value.
    """

    def __init__(self, raw_data, **kwargs):
        warnings.warn('This functionality will be deprecated with the next minor release (v1.2)', DeprecationWarning)
        super(StatusSettings, self).__init__(raw_data=raw_data, **kwargs)

    labels = DictType(StringType())
    labels_colors = DictType(DictType(StringType()))
    labels_positions_v2 = DictType(StringType())
    done_colors = ListType(IntType())
    hide_footer = BooleanType(default=False)

    def __repr__(self):
        return str(self.to_primitive())

    def get_index(self, label: str):
        """Get the label ID from the label value.

        Parameters

            label : `str`
                The status column option label value.

        Returns

            index : `int`
                The id of the status column option.
        """

        for key, value in dict(self.labels).items():
            if value == label:
                return int(key)
        return None

    def __getitem__(self, index: int):
        return dict(self.labels)[str(index)]


class DropdownLabel(Model):
    """Label options for a dropdown column

    Properties

        id : `int`
            The label ID.
        name : `str`
            The label name.
    """

    def __init__(self, raw_data, **kwargs):
        warnings.warn('This functionality will be deprecated with the next minor release (v1.2)', DeprecationWarning)
        super(DropdownLabel, self).__init__(raw_data=raw_data, **kwargs)

    id = IntType(required=True)
    name = StringType(required=True)

    def __repr__(self):
        return str(self.to_primitive())


class DropdownSettings(Model):
    """Settings for a dropdown column
    
    Properties

        labels : `list[moncli.entities.DropdownLabel]`
            The dropdown column's list of labels. 
    """

    def __init__(self, raw_data, **kwargs):
        warnings.warn('This functionality will be deprecated with the next minor release (v1.2)', DeprecationWarning)
        super(DropdownSettings, self).__init__(raw_data=raw_data, **kwargs)
    
    labels = ListType(ModelType(DropdownLabel))
    hide_footer = BooleanType(default=False)

    def __repr__(self):
        o = self.to_primitive()

        if self.labels:
            o['labels'] = [label.to_primitive() for label in dict(self.labels)]

        return str(o)

    def __getitem__(self, id):
        for label in list(self.labels):
            if label.id == id or label.name == id:
                return label
        raise KeyError