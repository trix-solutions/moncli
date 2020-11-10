import json

from schematics.models import Model
from schematics import types

from .. import config
from ..enums import ColumnType

class MondayClientCredentials():
    """monday.com client credentials.
    
    __________
    Properties

        api_key_v1 : `str`
            The access key for monday.com API v1.
        api_key_v2 : `str`
            The access key for monday.com API v2.
    """

    def __init__(self, api_key_v1: str, api_key_v2: str):
        self.api_key_v1 = api_key_v1
        self.api_key_v2 = api_key_v2


class ActivityLog(Model):
    """monday.com client credentials.
    
    __________
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

    id = types.StringType(required=True)
    account_id = types.StringType()
    created_at = types.StringType()
    data = types.StringType()
    entity = types.StringType()
    event = types.StringType()
    user_id = types.StringType()

    def __repr__(self):
        return str(self.to_primitive())

class BoardView(Model):
    """A board's view.

    __________
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

    id = types.StringType(required=True)
    name = types.StringType()
    settings_str = types.StringType()
    type = types.StringType()

    def __repr__(self):
        return str(self.to_primitive())
    

class Column(Model):
    """A board's column.
    
    __________
    Properties

        archived : `bool`
            Is the column archived or not.
        id : `str`
            The column's unique identifier.
        pos : `str`
            The column's position in the board. 
        settings_str : `str`
            The column's settings in a string form.
        settings : `moncli.entities.Settings`
            The settings in entity form (status / dropdown)
        title : `str`
            The column's title.
        type : `str`
            The column's type.
        column_type : `moncli.entities.ColumnType`
            The column's type as an enum.
        width : `int`
            The column's width.
    """

    id = types.StringType(required=True)
    title = types.StringType()
    archived = types.BooleanType()
    settings_str = types.StringType()
    type = types.StringType()
    width = types.IntType()
    
    def __repr__(self):
        return str(self.to_primitive())

    @property
    def settings(self):
        if not self.settings_str:
            return None
        settings_obj = json.loads(self.settings_str)
        if self.column_type is ColumnType.status:
            return StatusSettings(settings_obj, strict=False)
        elif self.column_type is ColumnType.dropdown:
            return DropdownSettings(settings_obj, strict=False)
    
    @property
    def column_type(self):
        # TODO - Find something else other than auto-number to default to.
        return config.COLUMN_TYPE_MAPPINGS.get(self.type, ColumnType.auto_number)


class Notification(Model):
    """A notification.

    __________
    Properties

        id : `str`
            The notification`s unique identifier.
        text : `str`
            the notification text.
    """

    id = types.StringType(required=True)
    text = types.StringType()

    def __repr__(self):
        return str(self.to_primitive())


class Tag(Model):
    """A tag.

    __________
    Properties

        color : `str`
            The tag's color.
        id : `str`
            The tag's unique identifier.
        name : `str`
            The tag's name.
    """

    id = types.StringType(required=True)
    name = types.StringType()
    color = types.StringType()

    def __repr__(self):
        return str(self.to_primitive())


class Plan(Model):
    """ A payment plan.
    
    __________
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

    max_users = types.IntType()
    period = types.StringType()
    tier = types.StringType()
    version = types.IntType()

    def __repr__(self):
        return str(self.to_primitive())


class Webhook(Model):
    """ Monday webhooks

    __________
    Properties

        board_id : `str`
            The webhook's board id.
        id : `str`
            The webhook's unique identifier.
        is_active : `bool`
            If the webhook is still active.
    """

    id = types.StringType(required=True)
    board_id = types.StringType()
    is_active = types.BooleanType(default=False)

    def __repr__(self):
        return str(self.to_primitive())


class Workspace(Model):
    """ A monday.com workspace

    __________
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
    id = types.StringType(required=True)
    name = types.StringType()
    kind = types.StringType()
    description = types.StringType()

    def __repr__(self):
        return str(self.to_primitive())


class StatusSettings(Model):
    """The settings of a status column

    __________
    Properties

        labels : `str`
            The index / label parings of a status column option.
        labels_colors : `dict`
            The index / color property parings of a status column option.
        labels_positions_v2 : `dict`
            The position of each label by ID.

    _______
    Methods

        get_index : `str`
            Get the label ID from the label value.
    """

    labels = types.DictType(types.StringType())
    labels_colors = types.DictType(types.DictType(types.StringType()))
    labels_positions_v2 = types.DictType(types.StringType())
    done_colors = types.ListType(types.IntType())
    hide_footer = types.BooleanType(default=False)

    def __repr__(self):
        return str(self.to_primitive())

    def get_index(self, label: str):
        """Get the label ID from the label value.

        __________
        Parameters

            label : `str`
                The status column option label value.

        _______
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

    __________
    Properties

        id : `int`
            The label ID.
        name : `str`
            The label name.
    """

    id = types.IntType(required=True)
    name = types.StringType(required=True)

    def __repr__(self):
        return str(self.to_primitive())


class DropdownSettings(Model):
    """Settings for a dropdown column
    
    __________
    Properties

        labels : `list[moncli.entities.DropdownLabel]`
            The dropdown column's list of labels. 
    """
    
    labels = types.ListType(types.ModelType(DropdownLabel))
    hide_footer = types.BooleanType(default=False)

    def __repr__(self):
        o = self.to_primitive()

        if self.labels:
            o['labels'] = [label.to_primitive() for label in dict(self.labels)]

        return str(o)

    def __getitem__(self, id):
        for label in list(self.labels):
            if label.id is id:
                return label
        raise KeyError