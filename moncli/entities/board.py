from .. import api_v2 as client
from ..enums import ColumnType
from .objects import Update
from .column import Column
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


    def add_column(self, title:str, column_type: ColumnType, *argv):

        if len(argv) == 0:
            argv = ['id']

        column_data = client.create_column(
            self.__creds.api_key_v2, 
            self.id, 
            title, 
            column_type, 
            *argv)

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
                ids=int(self.id))[0]

            self.__columns = [Column(creds=self.__creds, **column_data) for column_data in board['columns']]

        return self.__columns

    
    def change_column_value(self, item_id: str, column_id: str, value: str, *argv):

        item_data = client.change_column_value(
            self.__creds.api_key_v2, 
            item_id, 
            column_id, 
            self.id,
            value, 
            *argv)

        return Item(creds=self.__creds, **item_data)

    
    def change_multiple_column_value(self, item_id: str, column_values: str, *argv):

        item_data = client.change_multiple_column_value(
            self.__creds.api_key_v2,
            item_id,
            self.id,
            column_values,
            *argv)

        return Item(creds=self.__creds, **item_data)


    def add_group(self, group_name: str, *argv):

        group_data = client.create_group(
            self.__creds.api_key_v2,
            self.id,
            group_name,
            *argv)

        return Group(
            creds=self.__creds,
            board_id=self.id,
            **group_data)


    def duplicate_group(self, group_id: str, add_to_top: bool = False, group_title: str = None, *argv):
        
        group_data = client.duplicate_group(
            self.__creds.api_key_v2, 
            self.id, 
            group_id, 
            *argv)

        return Group(
            self.__creds,
            board_id=self.id,
            **group_data)


    def get_groups(self):

        if self.__groups == None:
            
            board = client.get_boards(
                self.__creds.api_key_v2,
                'groups.id',
                'groups.title',
                'groups.archived',
                'groups.color',
                'groups.deleted',
                'groups.items.id',
                'groups.position',
                ids=int(self.id))[0]

            self.__groups = [
                Group(creds=self.__creds, board_id=self.id, **group_data)
                for group_data
                in board['groups']
            ]

        return self.__groups 


    def archive_group(self, group_id: str, *argv):
        
        group_data = client.archive_group(
            self.__creds.api_key_v2, 
            self.id,
            group_id,
            *argv)

        return Group(
            creds=self.__creds,
            board_id=self.id,
            **group_data)


    def delete_group(self, group_id: str, *argv):
        
        group_data = client.delete_group(
            self.__creds.api_key_v2,
            self.id,
            group_id,
            *argv)

        return Group(
            creds=self.__creds,
            board_id=self.id,
            **group_data)


    def add_item(self, item_name: str, **kwargs):

        item_data = client.create_item(self.__creds.api_key_v2, item_name, self.id, 'id', **kwargs)

        return Item(creds=self.__creds, **item_data)


    def get_items(self):
        
        items_resp = client.get_items(
            self.__creds.api_key_v2, 
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

        return [Item(creds=self.__creds, **item_data) for item_data in items_resp] 


    def get_items_by_column_values(self, column_id: str, column_value: str, *argv, **kwargs):
        
        items_data = client.get_items_by_column_values(
            self.__creds.api_key_v2, 
            self.id, 
            column_id, 
            column_value, 
            *argv, 
            **kwargs)

        return [Item(creds=self.__creds, **item_data) for item_data in items_data]


    def move_item_to_group(self, item_id: str, group_id: str, *argv):
        
        item_data = client.move_item_to_group(
            self.__creds.api_key_v2,
            item_id,
            group_id)

        return Item(creds=self.__creds, **item_data)


    def archive_item(self, item_id: str, *argv):

        item_data = client.archive_item(
            self.__creds.api_key_v2,
            item_id,
            *argv)
        
        return Item(creds=self.__creds, **item_data)

    
    def delete_item(self, item_id: str, *argv):
        
        item_data = client.delete_item(
            self.__creds.api_key_v2,
            item_id,
            *argv)

        return Item(creds=self.__creds, **item_data)


    def add_update(self, body: str, item_id: str, *argv):
        
        update_data = client.create_update(
            self.__creds.api_key_v2,
            body,
            item_id,
            *argv)

        return Update(**update_data)

