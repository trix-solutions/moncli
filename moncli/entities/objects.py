import json

from schematics.models import Model
from schematics import types

from .. import config
from ..enums import ColumnType

class MondayClientCredentials():

    def __init__(self, api_key_v1: str, api_key_v2: str):
        self.api_key_v1 = api_key_v1
        self.api_key_v2 = api_key_v2


class Column(Model):
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
            return StatusSettings(settings_obj)
        elif self.column_type is ColumnType.dropdown:
            return DropdownSettings(settings_obj)
    
    @property
    def column_type(self):
        # TODO - Find something else other than auto-number to default to.
        return config.COLUMN_TYPE_MAPPINGS.get(self.type, ColumnType.auto_number)


class Update(Model):
    id = types.StringType(required=True)
    body = types.StringType()
    create_at = types.StringType()
    creator_id = types.StringType()
    item_id = types.StringType()
    text_body = types.StringType()
    updated_at = types.StringType()

    def __repr__(self):
        return str(self.to_primitive())


class Notification(Model):
    id = types.StringType(required=True)
    text = types.StringType()

    def __repr__(self):
        return str(self.to_primitive())


class Tag(Model):
    id = types.StringType(required=True)
    name = types.StringType()
    color = types.StringType()

    def __repr__(self):
        return str(self.to_primitive())


class Plan(Model):
    max_users = types.IntType()
    period = types.StringType()
    tier = types.StringType()
    version = types.IntType()

    def __repr__(self):
        return str(self.to_primitive())


class StatusSettings(Model):

    labels = types.DictType(types.StringType())
    labels_positions_v2 = types.DictType(types.StringType())

    def __repr__(self):
        return str(self.to_primitive())

    def get_index(self, label: str):
        for key, value in self.labels.items():
            if value == label:
                return int(key)
        return None

    def __getitem__(self, index: int):
        return self.labels[str(index)]


class DropdownLabel(Model):

    id = types.IntType(required=True)
    name = types.StringType(required=True)

    def __repr__(self):
        return str(self.to_primitive())


class DropdownSettings(Model):
    
    labels = types.ListType(types.ModelType(DropdownLabel))

    def __repr__(self):
        o = self.to_primitive()

        if self.labels:
            o['labels'] = [label.to_primitive() for label in self.labels]

        return str(o)

    def __getitem__(self, id):
        for label in self.labels:
            if label.id is id:
                return label
        raise KeyError