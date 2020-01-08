import json
from typing import List

from schematics.models import Model
from schematics import types

from .. import api_v2 as client, config, entities as en, enums
from ..columnvalue import create_column_value


class _Item(Model):
    id = types.StringType(required=True)
    name = types.StringType()
    created_at = types.StringType()
    creator_id = types.StringType()
    state = types.StringType()
    updated_at = types.StringType()


class Item(_Item):

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        self.__board = None
        self.__creator = None
        self.__column_values = None
        super(Item, self).__init__(kwargs)

    def __repr__(self):
        o = self.to_primitive()

        if self.__board:
            o['board'] = self.__board.to_primitive()
        if self.__column_values:
            o['column_values'] = [value.to_primitive() for value in self.__column_values]

        return str(o)

    @property
    def board(self):
        if not self.__board:
            self.__board = self.get_board()
        return self.__board

    @property
    def creator(self):
        if not self.__creator:
            self.__creator = self.get_creator()
        return self.__creator

    @property
    def column_values(self):
        self.__column_values = self.get_column_values()
        return self.__column_values

    def get_board(self):
        field_list = ['board.' + field for field in config.DEFAULT_BOARD_QUERY_FIELDS]
        board_data = client.get_items(
            self.__creds.api_key_v2,
            *field_list,
            ids=[int(self.id)])[0]['board']

        return en.Board(creds=self.__creds, **board_data)

    def get_creator(self):
        field_list = ['creator.' + field for field in config.DEFAULT_USER_QUERY_FIELDS]
        user_data = client.get_items(
            self.__creds.api_key_v2,
            *field_list,
            ids=[int(self.id)])[0]['creator']

        return en.User(creds=self.__creds, **user_data)
   
    def get_column_values(self):
        # Pulls the columns from the board containing the item and maps 
        # column ID to type.
        columns_map = { column.id: column for column in self.board.columns }
        field_list = ['column_values.' + field for field in config.DEFAULT_COLUMN_VALUE_QUERY_FIELDS]
        column_values_data = client.get_items(
            self.__creds.api_key_v2,
            *field_list,
            ids=[int(self.id)])[0]['column_values']

        values = []
        for data in column_values_data:
            id = data['id']
            column_type = columns_map[id].column_type
            if columns_map[id].settings:
                data['settings'] = columns_map[id].settings
            values.append(en.create_column_value(column_type, **data))

        return values

    def get_column_value(self, id = None, title = None):
        if id and title:
            raise en.board.TooManyGetColumnValueParameters()
        if id is None and title is None:
            raise en.board.NotEnoughGetColumnValueParameters()

        for column_value in self.column_values:
            if title and column_value.title == title:
                return column_value
            elif id and column_value.id == id:
                return column_value
    
    def change_column_value(self, column_id: str = None, column_value = None):
        if column_id is None:
            if column_value is None:
                raise ColumnValueRequired()
            if not isinstance(column_value, en.ColumnValue):
                raise en.board.InvalidColumnValue(type(column_value).__name__)
            else:
                column_id = column_value.id
                value = column_value.format()
        else:    
            if type(column_value) == str or type(column_value) == dict:
                value = column_value
            else:
                raise en.InvalidColumnValue(type(column_value).__name__)

        field_list = config.DEFAULT_ITEM_QUERY_FIELDS
        item_data = client.change_column_value(
            self.__creds.api_key_v2,
            self.id,
            column_id,
            self.board.id,
            value,
            *field_list)

        return Item(creds=self.__creds, **item_data)
    
    def change_multiple_column_values(self, column_values):
        if type(column_values) == dict:
            values = column_values
        elif type(column_values) == list:
            values = { value.id: value.format() for value in column_values }
        else:
            raise en.InvalidColumnValue(type(column_values).__name__)

        field_list = config.DEFAULT_ITEM_QUERY_FIELDS
        item_data = client.change_multiple_column_value(
            self.__creds.api_key_v2,
            self.id,
            self.board.id,
            values,
            *field_list)

        return Item(creds=self.__creds, **item_data)

    def move_to_group(self, group_id: str):
        field_list = config.DEFAULT_ITEM_QUERY_FIELDS
        item_data = client.move_item_to_group(
            self.__creds.api_key_v2,
            self.id,
            group_id,
            *field_list)

        return Item(creds=self.__creds, **item_data)

    def archive(self):
        field_list = config.DEFAULT_ITEM_QUERY_FIELDS
        item_data = client.archive_item(
            self.__creds.api_key_v2,
            self.id,
            *field_list)

        return Item(creds=self.__creds, **item_data)

    def delete(self):
        field_list = config.DEFAULT_ITEM_QUERY_FIELDS
        item_data = client.delete_item(
            self.__creds.api_key_v2,
            self.id,
            *field_list)

        return Item(creds=self.__creds, **item_data)

    def add_update(self, body: str):
        field_list = config.DEFAULT_UPDATE_QUERY_FIELDS
        update_data = client.create_update(
            self.__creds.api_key_v2, 
            body, 
            self.id,
            *field_list)

        return en.Update(update_data)


class ColumnValueRequired(Exception):
    def __init__(self):
        self.message = "A column value is required if no 'column_id' value is present."