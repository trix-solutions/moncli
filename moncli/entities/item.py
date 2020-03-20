import json
from typing import List

from .. import entities as e
from .. import api_v2 as client
from ..enums import ColumnType
from ..constants import COLUMN_TYPE_MAPPINGS
from ..columnvalue import create_column_value, ColumnValue
from . import exceptions as ex


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

        # Pulls the columns from the board containing the item and maps 
        # column ID to type.
        column_data = client.get_boards(
            self.__creds.api_key_v2,
            'columns.id', 'columns.type', 'columns.settings_str',
            ids=[int(self.__board_id)]
        )[0]['columns']
        columns_map = { data['id']: e.objects.Column(**data) for data in column_data }

        column_types_map = {}
        for column in column_data:
            try:
                column_types_map[column['id']] = ColumnType[COLUMN_TYPE_MAPPINGS[column['type']]]
            except:
                # Using auto-number to trigger read-only value
                column_types_map[column['id']] = ColumnType.auto_number

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

                def _strip_id():
                    try:
                        del value['id']
                    except:
                        pass
                
                # There may be more type switches to come
                def _handle_before():
                    if column_type == ColumnType.status:
                        value['settings'] = columns_map[id].settings

                if type(value) is dict:
                    _strip_id()
                    _handle_before()
                    column_value = create_column_value(id, column_type, title, **value)
                # This case pertains to number and text fields
                else:
                    column_value = create_column_value(id, column_type, title, value=value)

            self.__column_values[id] = column_value   

        return list(self.__column_values.values())


    def get_column_value(self, id = None, title = None):

        self.get_column_values()

        if id is not None:

            if title is not None:
                raise ex.TooManyGetColumnValueParameters()

            return self.__column_values[id]

        if title is not None:

            column_values_list = list(self.__column_values.values())
            for column_value in column_values_list:
                if column_value.title == title:
                    return column_value

        raise ex.NotEnoughGetColumnValueParameters()

    
    def change_column_value(self, column_id: str = None, column_value = None):
        
        if column_id is None:

            if column_value is None:
                raise ex.ColumnValueRequired()
            if not isinstance(column_value, ColumnValue):
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
            self.__board_id,
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

        return e.objects.Update(**update_data)