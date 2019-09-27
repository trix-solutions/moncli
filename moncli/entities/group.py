from .. import api_v2 as client
from .item import Item

class Group():

    def __init__(self, **kwargs):
        self.__creds = kwargs['creds']
        self.id = kwargs['id']
        self.board_id = kwargs['board_id']
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
    

    def duplicate(self, group_title: str, add_to_top: bool = False, *argv):
        
        group_data = client.duplicate_group(
            self.__creds.api_key_v2, 
            self.board_id, 
            self.id, 
            *argv)

        return Group(
            creds=self.__creds,
            board_id=self.board_id,
            **group_data)


    def archive(self, *argv):
        
        group_data = client.archive_group(
            self.__creds.api_key_v2,
            self.board_id,
            self.id,
            *argv)

        return Group(
            creds=self.__creds,
            board_id=self.board_id,
            **group_data)


    def delete(self, *argv):
        
        group_data = client.delete_group(
            self.__creds.api_key_v2,
            self.board_id,
            self.id,
            *argv)

        return Group(
            creds=self.__creds,
            board_id=self.board_id
            **group_data)


    def add_item(self, item_name: str, column_values: str = None, *argv):
        
        item_data = client.create_item(
            self.__creds.api_key_v2,
            item_name,
            self.board_id,
            *argv,
            column_values=column_values)

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
            self.board_id,
            self.id,
            column_value,
            *argv,
            **kwargs)

        return [
            Item(creds=self.__creds, **item_data)
            for item_data
            in items_data
        ]

    
    def move_item(self, item_id: str, group_id: str, *argv):
        
        item_data = client.move_item_to_group(
            self.__creds, 
            item_id, 
            group_id,
            *argv)

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