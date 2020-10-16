from schematics.models import Model
from schematics import types

from .. import api_v2 as client, config, enums, entities as en
from ..api_v2 import constants
from ..decorators import default_field_list, optional_arguments
from ..entities import column_value as cv


class _Board(Model):

    id = types.StringType(required=True)
    name = types.StringType()
    board_folder_id = types.IntType()
    board_kind = types.StringType()
    description = types.StringType()
    permissions = types.StringType()
    pos = types.StringType()
    state = types.StringType()


class Board(_Board):

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds', None)
        self.__columns = None
        columns = kwargs.pop('columns', None)
        if columns:
            self.__columns = [en.Column() for column in columns]
        self.__groups = None
        groups = kwargs.pop('groups', None)
        if groups:
            self.__groups = [en.Group(creds=self.__creds, **groups) for group in groups]
        self.__items = None
        items = kwargs.pop('items', None)
        if items:
            self.__items = [en.Item(creds=self.__creds, **item) for item in items]
        super(Board, self).__init__(kwargs)

    def __repr__(self):
        o = self.to_primitive()
        if self.__columns:
            o['columns'] = [column.to_primitive() for column in self.__columns]
        if self.__groups:
            o['groups'] = [group.to_primitive() for group in self.__groups]
        if self.__items:
            o['items'] = [item.to_primitive() for item in self.__items]       
        return str(o)
 
    @property
    def columns(self):
        if not self.__columns:
            self.__columns = self.get_columns()
        return self.__columns

    @property
    def groups(self):
        if not self.__groups:
            self.__groups = self.get_groups()
        return self.__groups

    @property
    def items(self):
        if not self.__items:
            self.__items = self.get_items()
        return self.__items

    @optional_arguments(constants.CREATE_COLUMN_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_COLUMN_QUERY_FIELDS)
    def add_column(self, title:str, column_type: enums.ColumnType, *args): 
        column_data = client.create_column(
            self.__creds.api_key_v2, 
            self.id, 
            title, 
            column_type, 
            *args)
        return en.Column(column_data)
   
    @default_field_list(config.DEFAULT_COLUMN_QUERY_FIELDS)
    def get_columns(self, *args):
        args = ['columns.' + arg for arg in args]
        column_data = client.get_boards(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.id)],
            limit=1)[0]['columns']
        return [en.Column(data) for data in column_data]

    @optional_arguments(constants.CREATE_GROUP_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_GROUP_QUERY_FIELDS)
    def add_group(self, group_name: str, *args):
        group_data = client.create_group(
            self.__creds.api_key_v2,
            self.id,
            group_name,
            *args)
        return en.Group(
            creds=self.__creds,
            board_id=self.id,
            **group_data)

    @default_field_list(config.DEFAULT_GROUP_QUERY_FIELDS)
    def get_groups(self, *args):
        args = ['groups.' + arg for arg in args]
        groups_data = client.get_boards(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.id)])[0]['groups']
        return [en.Group(creds=self.__creds, board_id=self.id, **data) for data in groups_data]
  
    def get_group(self, id: str = None, title: str = None):     
        if id is None and title is None:
            raise NotEnoughGetGroupParameters()
        if id is not None and title is not None:
            raise TooManyGetGroupParameters()
        if id is not None:
            return [group for group in self.groups if group.id == id][0]
        else:
            return [group for group in self.groups if group.title == title][0]

    @optional_arguments(constants.CREATE_ITEM_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_ITEM_QUERY_FIELDS)
    def add_item(self, item_name: str, *args, **kwargs):
        column_values = kwargs.pop('column_values', None)
        if column_values:
            if type(column_values) == dict:
                kwargs['column_values'] = column_values
            elif type(column_values) == list:
                kwargs['column_values'] = { value.id: value.format() for value in column_values }
            else:
                raise InvalidColumnValue(type(column_values).__name__)

        item_data = client.create_item(
            self.__creds.api_key_v2, 
            item_name, 
            self.id, 
            *args, 
            **kwargs)
        return en.Item(creds=self.__creds, **item_data)

    @default_field_list(config.DEFAULT_ITEM_QUERY_FIELDS)
    def get_items(self, *args):
        args = ['items.' + arg for arg in args]
        items_data = client.get_boards(
            self.__creds.api_key_v2,
            *args, 
            ids=[int(self.id)])[0]['items']
        return [en.Item(creds=self.__creds, **item_data) for item_data in items_data] 

    @optional_arguments(constants.ITEMS_BY_COLUMN_VALUES_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_ITEM_QUERY_FIELDS)
    def get_items_by_column_values(self, column_value: en.ColumnValue, *args, **kwargs):      
        if type(column_value) == cv.DateValue:
            value = column_value.date
        elif type(column_value) == cv.StatusValue:
            value = column_value.label
        else:
            value = column_value.format()

        items_data = client.get_items_by_column_values(
            self.__creds.api_key_v2, 
            self.id, 
            column_value.id, 
            value, 
            *args,
            **kwargs)
        return [en.Item(creds=self.__creds, **item_data) for item_data in items_data]

    def get_column_values(self):
        pass

    def get_column_value(self, id: str = None, title: str = None, **kwargs):
        if id is None and title is None:
            raise NotEnoughGetColumnValueParameters()
        if id is not None and title is not None:
            raise TooManyGetColumnValueParameters()

        columns = { column.id: column for column in self.columns }
        if id is not None:
            column = columns[id]
            column_type = config.COLUMN_TYPE_MAPPINGS[column.type]           
        elif title is not None:
            column = [column for column in columns.values() if column.title == title][0]
            column_type = config.COLUMN_TYPE_MAPPINGS[column.type]

        if column_type == enums.ColumnType.status:
            kwargs['settings'] = column.settings     
        return cv.create_column_value(column_type, id=column.id, title=column.title)

    @default_field_list(config.DEFAULT_WEBHOOK_QUERY_FIELDS)
    def create_webhook(self, url: str, event: enums.WebhookEventType, *args, **kwargs):
        # Modify kwargs to config if supplied.
        if kwargs:
            if event != enums.WebhookEventType.change_specific_column_value:
                raise WebhookConfigurationError(event)
            kwargs = {'config': kwargs}
        webhook_data = client.create_webhook(
            self.__creds.api_key_v2, 
            self.id, 
            url, 
            event,
            *args,
            **kwargs)
        webhook_data['is_active'] = True
        return en.objects.Webhook(webhook_data)

    @default_field_list(config.DEFAULT_WEBHOOK_QUERY_FIELDS)
    def delete_webhook(self, webhook_id: str, *args, **kwargs):
        webhook_data = client.delete_webhook(
            self.__creds.api_key_v2, 
            webhook_id,
            *args,
            **kwargs)
        webhook_data['is_active'] = False
        return en.objects.Webhook(webhook_data)

        
class TooManyGetGroupParameters(Exception):
    def __init__(self):
        self.message = "Unable to use both 'id' and 'title' when querying for a group."
        

class NotEnoughGetGroupParameters(Exception):
    def __init__(self):
        self.message = "Either the 'id' or 'title' is required when querying a group."


class InvalidColumnValue(Exception):
    def __init__(self, column_value_type: str):
        self.message = "Unable to use column value of type '{}' with the given set of input parameters".format(column_value_type)


class TooManyGetColumnValueParameters(Exception):
    def __init__(self):
        self.message = "Unable to use both 'id' and 'title' when querying for a column value."
        

class NotEnoughGetColumnValueParameters(Exception):
    def __init__(self):
        self.message = "Either the 'id' or 'title' is required when querying a column value."

class WebhookConfigurationError(Exception):
    def __init__(self, event: enums.WebhookEventType):
        self.message = "Webhook event type '{}' does not support configuraitons".format(event.name)