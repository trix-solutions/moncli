from datetime import datetime
from typing import List

from .graphql import boards, items

class Board():

    def __init__(self, api_key_v1: str, api_key_v2: str, **kwargs):
        self.__api_key_v1 = api_key_v1
        self.__api_key_v2 = api_key_v2
        self.__columns = None
        self.id = kwargs['id']
        self.name = kwargs['name']

        for key, value in kwargs.items():

            if key == 'board_folder_id':
                self.board_folder_id = value
            
            elif key == 'board_kind':
                self.board_kind = value

            elif key == 'columns':
                self.__columns = [Column(**column_data) for column_data in value]

            elif key == 'description':
                self.description = value

            elif key == 'groups':
                self.__group_ids: List[int] = [int(item['id']) for item in value]

            elif key == 'items':
                self.__item_ids: List[int] = [int(item['id']) for item in value]

            elif key == 'owner':
                self.__owner_id: str = value['id']

            elif key == 'permissions':
                self.permissions = value

            elif key == 'pos':
                self.position = value

            elif key == 'state':
                self.state = value


    def get_items(self):
        
        items_resp = items.get_items(
            self.__api_key_v2, 
            'id',
            'name',
            'board.id',
            'board.name',
            'creator_id',
            'column_values.id',
            'column_values.text',
            'column_values.title',
            'column_values.value',
            'column_values.additional_info',
            'group.id',
            'state',
            'subscribers.id',
            ids=self.__item_ids, 
            limit=1000)

        return [Item(self.__api_key_v1, self.__api_key_v2, **item_data) for item_data in items_resp] 

    
    def get_columns(self):

        if self.__columns == None:

            board = boards.get_boards(
                self.__api_key_v2,
                'columns.id',
                'columns.archived',
                'columns.settings_str',
                'columns.title',
                'columns.type',
                'columns.width',
                ids=int(self.id))[0]

            self.__columns = [Column(**column_data) for column_data in board['columns']]

        return self.__columns


    def add_item(self, item_name: str, **kwargs):

        item = items.create_item(self.__api_key_v2, item_name, self.id, 'id', **kwargs)

        return item['id']


class Column():

    def __init__(self, **kwargs):
        self.id= kwargs['id']

        for key, value in kwargs.items():

            if key == 'archived':
                self.archived = value

            elif key == 'settings_str':
                self.settings_str = value

            elif key == 'title':
                self.title = value
            
            elif key == 'type':
                self.type = value

            elif key == 'width':
                self.width = value


class Group():

    def __init__(self, api_key_v1: str, api_key_v2: str, **kwargs):
        self.__api_key_v1 = api_key_v1
        self.__api_key_v2 = api_key_v2
        self.id = kwargs['id']
        self.__item_ids = None

        for key, value in kwargs.items():

            if key == 'title':
                self.title = value

            elif key == 'archived':
                self.archived = value
            
            elif key == 'color':
                self.color = value

            elif key == 'deleted':
                self.deleted = value

            elif key == 'items':
                self.__item_ids = [int(item['id'] for item in value)]

            elif key == 'position':
                self.position = value
    

    def get_items(self):

        items_resp = items.get_items(
            self.__api_key_v2, 
            'id',
            'name',
            'board.id',
            'board.name',
            'creator_id',
            'column_values.id',
            'column_values.text',
            'column_values.title',
            'column_values.value',
            'column_values.additional_info',
            'group.id',
            'state',
            'subscribers.id',
            ids=self.__item_ids, 
            limit=1000)

        return [Item(self.__api_key_v1, self.__api_key_v2, **item_data) for item_data in items_resp] 


class Item():

    def __init__(self, api_key_v1: str, api_key_v2: str, **kwargs):
        self.__api_key_v2 = api_key_v2
        self.__column_values = None
        self.id = kwargs['id']
        self.name = kwargs['name']

        for key, value in kwargs.items():

            if key == 'board':
                
                if type(value) == type(Board):
                    self.board = value
                
                elif type(value) is dict:
                    
                    if value.__contains__('name'):
                        self.board = Board(api_key_v1, api_key_v2, **value)

                    else:
                        self.__board_id = value['id']

            elif key == 'column_values':
                self.__column_values = [ColumnValue(**column_values) for column_values in value]

            elif key == 'creator_id':
                self.creator_id = value

            elif key == 'group':
                self.__group_id = value['id']

            elif key == 'state':
                self.state = value
            
            elif key == 'subscribers':
                self.__subscriber_ids = [int(item['id']) for item in value]

        
    def get_column_values(self):

        if self.__column_values == None:           
            item = items.get_items(
                self.__api_key_v2,
                'column_values.id',
                'column_values.text',
                'column_values.title',
                'column_values.value',
                'column_values.additional_info')
                
            self.__column_values = [ColumnValue(**column_values) for column_values in item['column_values']]

        return self.__column_values


class ColumnValue():

    def __init__(self, **kwargs):
        self.id = kwargs['id']

        for key, value in kwargs.items():

            if key == 'text':
                self.text = value

            if key == 'title':
                self.title = value

            if key == 'value':
                self.value = value

            if key == 'additional_info':
                self.additional_info = value


class GroupNotFound(Exception):

    def __init__(self, board, group_name):

        self.board_id = board.id
        self.board_name = board.name
        self.group_name = group_name
        self.message = 'Unable to find group {} in board {}.'.format(self.group_name, self.board_name)

    