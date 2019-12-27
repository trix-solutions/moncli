import json
from typing import List

from schematics.models import Model
from schematics.types import StringType, DateType

import moncli.entities.exceptions as ex
from .. import entities as e
from .. import api_v2 as client
from .. import config
from ..enums import ColumnType
from ..config import COLUMN_TYPE_MAPPINGS
from ..columnvalue import create_column_value
from ..entities import column_value as cv


class _Item(Model):
    id = StringType(required=True)
    name = StringType()
    created_at = StringType()
    creator_id = StringType()
    state = StringType()
    updated_at = StringType()


class Item(_Item):

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        self.__board = None
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
        if self.__board:
            return self.__board

        field_list = ['board.' + field for field in config.DEFAULT_BOARD_QUERY_FIELDS]
        board_data = client.get_items(
            self.__creds.api_key_v2,
            *field_list,
            ids=[int(self.id)])[0]['board']

        self.__board = e.Board(creds=self.__creds, **board_data)

        return self.__board


    @property
    def column_values(self):
        self.__column_values = self.get_column_values()
        return self.__column_values

        
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
            value = data['value']
            if value:
                value = json.loads(value)
                if type(value) is dict:
                    """
                    try:
                        del value['id']
                    except:
                        pass
                    """
                    if column_type is ColumnType.status or column_type :
                        data['settings'] = columns_map[id].settings

            values.append(cv.create_column_value(column_type, **data))

        return values


    def get_column_value(self, id = None, title = None):

        self.get_column_values()

        if id is not None:

            if title is not None:
                raise ex.TooManyGetColumnValueParameters()

            return self.__column_values[id]

        if title is not None:

            for column_value in self.__column_values:
                if column_value.title == title:
                    return column_value

        raise ex.NotEnoughGetColumnValueParameters()

    
    def change_column_value(self, column_id: str = None, column_value = None):
        if column_id is None:

            if column_value is None:
                raise ex.ColumnValueRequired()
            if not isinstance(column_value, e.column_value.ColumnValue):
                raise ex.InvalidColumnValue(type(column_value).__name__)
            else:
                column_id = column_value.id
                value = column_value.format()

        else:
            
            if type(column_value) == str or type(column_value) == dict:
                value = column_value
            else:
                raise ex.InvalidColumnValue(type(column_value).__name__)

        item_data = client.change_column_value(
            self.__creds.api_key_v2,
            self.id,
            column_id,
            self.board.id,
            value,
            'id', 'name', 'board.id')

        return Item(creds=self.__creds, **item_data)

    
    def change_multiple_column_values(self, column_values):

        if type(column_values) == dict:
            values = column_values
        elif type(column_values) == list:
            values = { value.id: value.format() for value in column_values }
        else:
            raise ex.InvalidColumnValue(type(column_values).__name__)

        item_data = client.change_multiple_column_value(
            self.__creds.api_key_v2,
            self.id,
            self.board.id,
            values,
            'id', 'name', 'board.id')

        return Item(creds=self.__creds, **item_data)

    
    def move_to_group(self, group_id: str):
        
        item_data = client.move_item_to_group(
            self.__creds.api_key_v2,
            self.id,
            group_id,
            'id', 'name', 'board.id')

        return Item(creds=self.__creds, **item_data)


    def archive(self):
        
        item_data = client.archive_item(
            self.__creds.api_key_v2,
            self.id,
            'id', 'name', 'board.id')

        return Item(creds=self.__creds, **item_data)


    def delete(self):
        
        item_data = client.delete_item(
            self.__creds.api_key_v2,
            self.id,
            'id', 'name', 'board.id')

        return Item(creds=self.__creds, **item_data)


    def add_update(self, body: str):
        
        update_data = client.create_update(
            self.__creds.api_key_v2, 
            body, 
            self.id,
            'id', 'body')

        return e.objects.Update(**update_data)