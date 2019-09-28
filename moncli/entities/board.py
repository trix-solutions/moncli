from .. import api_v2 as client
from ..enums import ColumnType
from .objects import Update, Column
from .group import Group
from .item import Item

class Board():

    def __init__(self, **kwargs):
        self.__columns = None
        self.__groups = None
        self.__creds = kwargs['creds']

        self.id = kwargs['id']

        for key, value in kwargs.items():

            if key == 'name':
                self.name = value

            if key == 'board_folder_id':
                self.board_folder_id = value
            
            elif key == 'board_kind':
                self.board_kind = value

            elif key == 'description':
                self.description = value

            elif key == 'items':
                self.__item_ids = [int(item['id']) for item in value]

            elif key == 'owner':
                self.__owner_id: str = value['id']

            elif key == 'permissions':
                self.permissions = value

            elif key == 'pos':
                self.position = value

            elif key == 'state':
                self.state = value


    def add_column(self, title:str, column_type: ColumnType):
        
        column_data = client.create_column(
            self.__creds.api_key_v2, 
            self.id, 
            title, 
            column_type, 
            'id', 'title', 'type')

        return Column(creds=self.__creds, **column_data)

    
    def get_columns(self):

        if self.__columns == None:

            board = client.get_boards(
                self.__creds.api_key_v2,
                'columns.id',
                'columns.archived',
                'columns.settings_str',
                'columns.title',
                'columns.type',
                'columns.width',
                ids=[int(self.id)])

            self.__columns = [Column(creds=self.__creds, **column_data) for column_data in board[0]['columns']]

        return self.__columns


    def add_group(self, group_name: str):

        group_data = client.create_group(
            self.__creds.api_key_v2,
            self.id,
            group_name,
            'id', 'title')

        return Group(
            creds=self.__creds,
            board_id=self.id,
            **group_data)


    def get_groups(self):

        field_list = ['groups.id', 'groups.title', 'groups.archived', 'groups.color', 'groups.deleted', 'groups.items.id', 'groups.position']

        if self.__groups == None:
            
            board = client.get_boards(
                self.__creds.api_key_v2,
                *field_list,
                ids=[int(self.id)])[0]

            self.__groups = [
                Group(creds=self.__creds, board_id=self.id, **group_data)
                for group_data
                in board['groups']
            ]

        return self.__groups 


    def add_item(self, item_name: str, **kwargs):

        item_data = client.create_item(
            self.__creds.api_key_v2, 
            item_name, 
            self.id, 
            'id', 'name', 'board.id', 
            **kwargs)

        return Item(creds=self.__creds, **item_data)


    def get_items(self):
        
        field_list = [
            'id',
            'name',
            'board.id',
            'board.name',
            'creator_id',
            'group.id',
            'state',
            'subscribers.id'
        ]

        if not hasattr(self, '__item_ids'):

            items = client.get_boards(
                self.__creds.api_key_v2,
                'items.id', 
                ids=[int(self.id)])[0]['items']

            self.__item_ids = [int(item['id']) for item in items]

        items_data = client.get_items(
            self.__creds.api_key_v2, 
            *field_list,
            ids=self.__item_ids, 
            limit=1000)

        return [Item(creds=self.__creds, **item_data) for item_data in items_data] 


    def get_items_by_column_values(self, column_id: str, column_value: str, **kwargs):
        
        field_list = [
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
            'subscribers.id'
        ]

        items_data = client.get_items_by_column_values(
            self.__creds.api_key_v2, 
            self.id, 
            column_id, 
            column_value, 
            *field_list,
            **kwargs)

        return [Item(creds=self.__creds, **item_data) for item_data in items_data]