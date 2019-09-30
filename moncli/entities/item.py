import json
from typing import List

from .. import api_v2 as client
from ..enums import ColumnType
from ..constants import COLUMN_TYPE_MAPPINGS
from ..columnvalue import create_column_value, ColumnValue
from .objects import Update

class Item():

    def __init__(self, **kwargs):
        self.__creds = kwargs['creds']
        self.__board_id = kwargs['board']['id']
        self.__column_values = None

        self.id = kwargs['id']
        self.name = kwargs['name']

        for key, value in kwargs.items():

            if key == 'creator_id':
                self.creator_id = value

            elif key == 'group':
                self.__group_id = value['id']

            elif key == 'state':
                self.state = value
            
            elif key == 'subscribers':
                self.__subscriber_ids = [int(item['id']) for item in value]

        
    def get_column_values(self):

        if self.__column_values == None: 

            # Pulls the columns from the board containing the item and maps 
            # column ID to type.
            column_types_map = {
                column['id']: ColumnType[COLUMN_TYPE_MAPPINGS[column['type']]]
                for column
                in client.get_items(
                    self.__creds.api_key_v2,
                    'board.columns.id', 'board.columns.type',
                    ids=[int(self.id)])[0]['board']['columns']
            }

            item_data = client.get_items(
                self.__creds.api_key_v2,
                'column_values.id', 'column_values.title', 'column_values.value',
                ids=[int(self.id)])[0]

            column_values_data = item_data['column_values']

            self.__column_values = {}

            for data in column_values_data:

                id = data['id']
                title = data['title']
                column_type = column_types_map[id]

                value = data['value']
                if value is None:
                    column_value = create_column_value(id, column_type, title)
                else:
                    value = json.loads(value)
                    column_value = create_column_value(id, column_type, title, value)

                self.__column_values[id] = column_value          

        return self.__column_values.values()


    def get_column_value(self, id = None, title = None):

        self.get_column_values()

        if id is not None:

            if title is not None:
                raise TooManyGetColumnValueParameters()

            return self.__column_values[id]

        if title is not None:

            return [column_value for column_value in self.__column_values.values() if column_value.title == title][0]

        raise NotEnoughGetColumnValueParameters()

    
    def change_column_value(self, column_value: ColumnValue):
        
        item_data = client.change_column_value(
            self.__creds.api_key_v2,
            self.id,
            column_value.id,
            self.__board_id,
            column_value.format(),
            'id', 'name', 'board.id')

        return Item(creds=self.__creds, **item_data)

    
    def change_multiple_column_values(self, column_values: List[ColumnValue]):
        
        values = { value.id: value.format() for value in column_values }

        item_data = client.change_multiple_column_value(
            self.__creds.api_key_v2,
            self.id,
            self.__board_id,
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

        return Update(**update_data)


class TooManyGetColumnValueParameters(Exception):

    def __init__(self):
        self.message = "Unable to use both 'id' and 'title' when querying for a column value."
        

class NotEnoughGetColumnValueParameters(Exception):

    def __init__(self):
        self.message = "Either the 'id' or 'title' is required when querying a column value."