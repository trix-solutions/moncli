import json
from typing import List

from schematics.models import Model
from schematics import types

from .. import api_v2 as client, config, entities as en, enums
from ..api_v2 import constants
from ..decorators import default_field_list, optional_arguments
from .column_value import FileValue


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
        self.__updates = None
        board = kwargs.pop('board', None)
        if board:
            self.__board = en.Board(creds=self.__creds, **board)
        creator = kwargs.pop('creator', None)
        if creator:
            self.__creator = en.User(creds=self.__creds, **creator)
        kwargs.pop('column_values', None)
        updates = kwargs.pop('updates', None)
        if updates:
            self.__updates = [en.Update(creds=self.__creds)]
        super(Item, self).__init__(kwargs)

    def __repr__(self):
        o = self.to_primitive()
        if self.__board:
            o['board'] = self.__board.to_primitive()
        if self.__column_values:
            o['column_values'] = [value.to_primitive() for value in self.__column_values]
        if self.__updates:
            o['column_values'] = [value.to_primitive() for value in self.__updates]
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

    @property
    def updates(self):
        if not self.__updates: 
            self.__updates = self.get_updates()
        return self.__updates

    @default_field_list(config.DEFAULT_BOARD_QUERY_FIELDS)
    def get_board(self, *args):
        args = ['board.' + arg for arg in args]
        board_data = client.get_items(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.id)])[0]['board']

        return en.Board(creds=self.__creds, **board_data)

    @default_field_list(config.DEFAULT_USER_QUERY_FIELDS)
    def get_creator(self, *args):
        args = ['creator.' + arg for arg in args]
        user_data = client.get_items(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.id)])[0]['creator']
        return en.User(creds=self.__creds, **user_data)
   
    @default_field_list(config.DEFAULT_COLUMN_VALUE_QUERY_FIELDS)
    def get_column_values(self, *args):
        # Pulls the columns from the board containing the item and maps 
        # column ID to type.
        columns_map = { column.id: column for column in self.board.columns }
        args = ['column_values.' + arg for arg in args]
        column_values_data = client.get_items(
            self.__creds.api_key_v2,
            *args,
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
    
    @optional_arguments(constants.CHANGE_COLUMN_VALUE_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_ITEM_QUERY_FIELDS)
    def change_column_value(self, column_value = None, *args):
        if column_value is None:
            raise ColumnValueRequired()
        if not isinstance(column_value, en.ColumnValue):
            raise en.board.InvalidColumnValue(type(column_value).__name__)
        else:
            column_id = column_value.id
            value = column_value.format()

        item_data = client.change_column_value(
            self.__creds.api_key_v2,
            self.id,
            column_id,
            self.board.id,
            value,
            *args)
        return Item(creds=self.__creds, **item_data)
    
    @optional_arguments(constants.CHANGE_MULTIPLE_COLUMN_VALUES_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_ITEM_QUERY_FIELDS)
    def change_multiple_column_values(self, column_values, *args):
        if type(column_values) == dict:
            values = column_values
        elif type(column_values) == list:
            values = { value.id: value.format() for value in column_values }
        else:
            raise en.InvalidColumnValue(type(column_values).__name__)
        item_data = client.change_multiple_column_value(
            self.__creds.api_key_v2,
            self.id,
            self.board.id,
            values,
            *args)
        return Item(creds=self.__creds, **item_data)

    @optional_arguments(constants.MOVE_ITEM_TO_GROUP_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_ITEM_QUERY_FIELDS)
    def move_to_group(self, group_id: str, *args):
        item_data = client.move_item_to_group(
            self.__creds.api_key_v2,
            self.id,
            group_id,
            *args)

        return Item(creds=self.__creds, **item_data)

    @default_field_list(config.DEFAULT_ITEM_QUERY_FIELDS)
    def archive(self, *args):
        item_data = client.archive_item(
            self.__creds.api_key_v2,
            self.id,
            *args)

        return Item(creds=self.__creds, **item_data)

    @default_field_list(config.DEFAULT_ITEM_QUERY_FIELDS)
    def delete(self, *args):
        item_data = client.delete_item(
            self.__creds.api_key_v2,
            self.id,
            *args)
        return Item(creds=self.__creds, **item_data)

    @optional_arguments(constants.CREATE_UPDATE_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_UPDATE_QUERY_FIELDS)
    def add_update(self, body: str, *args):
        update_data = client.create_update(
            self.__creds.api_key_v2, 
            body, 
            self.id,
            *args)
        return en.Update(creds=self.__creds, **update_data)

    @default_field_list(config.DEFAULT_UPDATE_QUERY_FIELDS)
    def get_updates(self, *args, **kwargs):
        args = ['updates.' + arg for arg in args]
        limit = kwargs.pop('limit', 25)
        page = kwargs.pop('page', 1)
        updates_data = client.get_items(
            self.__creds.api_key_v2,
            *args,
            ids=[int(self.id)],
            limit=1,
            updates={'limit': limit, 'page': page})[0]['updates']
        return [en.Update(creds=self.__creds, **update_data) for update_data in updates_data]

    @default_field_list(config.DEFAULT_FILE_QUERY_FIELDS)
    def add_file(self, file_column: FileValue, file_path: str, *argv):
        asset_data = client.add_file_to_column(
            self.__creds.api_key_v2,
            self.id,
            file_column.id,
            file_path,
            *argv)
        return en.objects.Asset(asset_data)

    @default_field_list(config.DEFAULT_ITEM_QUERY_FIELDS)
    def remove_files(self, file_column: FileValue, *argv):
        item_data = client.change_column_value(
            self.__creds.api_key_v2,
            self.id,
            file_column.id,
            self.__board.id,
            file_column.format(),
            *argv)
        return Item(creds=self.__creds, **item_data)


class ColumnValueRequired(Exception):
    def __init__(self):
        self.message = "A column value is required if no 'column_id' value is present."