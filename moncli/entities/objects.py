import json

from schematics.models import Model
from schematics.types import StringType, BooleanType, IntType, DictType

from .. import config
from ..enums import ColumnType

class MondayClientCredentials():

    def __init__(self, api_key_v1: str, api_key_v2: str):
        self.api_key_v1 = api_key_v1
        self.api_key_v2 = api_key_v2


class Column(Model):

    id = StringType(required=True)
    title = StringType()
    archived = BooleanType()
    settings_str = StringType()
    type = StringType()
    width = IntType()

    
    def __repr__(self):
        return str(self.to_primitive())


    @property
    def settings(self):
        settings_str = json.loads(self.settings_str)
        if self.type == 'color':
            return StatusSettings(settings_str)

    
    @property
    def column_type(self):
        # TODO - Find something else other than auto-number to default to.
        return config.COLUMN_TYPE_MAPPINGS.get(self.type, ColumnType.auto_number)


class Update():

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        
        for key, value in kwargs.items():

            if key == 'body':
                self.body = value


class Notification():

    def __init__(self, **kwargs):
        self.id = kwargs['id']

        for key, value in kwargs.items():

            if key == 'text':
                self.text = value


class Tag():

    def __init__(self, **kwargs):

        self.id = kwargs['id']

        for key, value in kwargs.items():

            if key == 'name':
                self.name = value

            elif key == 'color':
                self.color = value


class Plan():

    def __init__(self, **kwargs):

        for key, value in kwargs.items():

            if key == 'max_users':
                self.max_users = value

            elif key == 'period':
                self.period = value

            elif key == 'tier':
                self.tier = value

            elif key == 'version':
                self.version = value


class StatusSettings(Model):

    labels = DictType(StringType())
    labels_positions_v2 = DictType(StringType())


    def __repr__(self):
        return str(self.to_primitive())


    def get_index(self, label: str):

        for key, value in self.labels.items():

            if value == label:
                return int(key)

        return None