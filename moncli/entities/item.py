from .. import api_v2 as client
from .objects import ColumnValue, Update

class Item():

    def __init__(self, **kwargs):
        self.__creds = kwargs['creds']
        self.__board_id = kwargs['board']['id']
        self.__column_values = None

        self.id = kwargs['id']
        self.name = kwargs['name']

        for key, value in kwargs.items():

            if key == 'column_values':
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
            item = client.get_items(
                self.__creds.api_key_v2,
                'column_values.id',
                'column_values.text',
                'column_values.title',
                'column_values.value',
                'column_values.additional_info',
                ids=int(self.id))
                
            self.__column_values = [ColumnValue(**column_values) for column_values in item['column_values']]

        return self.__column_values

    
    def change_column_value(self, column_id: str, value: str, *argv):
        
        item_data = client.change_column_value(
            self.__creds.api_key_v2,
            self.id,
            column_id,
            self.__board_id,
            value,
            *argv)


        return Item(creds=self.__creds, **item_data)

    
    def change_multiple_column_values(self, column_values: str, *argv):
        
        item_data = client.change_multiple_column_value(
            self.__creds.api_key_v2,
            self.id,
            self.__board_id,
            column_values,
            *argv)

        return Item(creds=self.__creds, **item_data)

    
    def move_to_group(self, group_id: str, *argv):
        
        item_data = client.move_item_to_group(
            self.__creds.api_key_v2,
            self.id,
            group_id)

        return Item(creds=self.__creds, **item_data)


    def archive(self, *argv):
        
        item_data = client.archive_item(
            self.__creds.api_key_v2,
            self.id,
            *argv)

        return Item(creds=self.__creds, **item_data)


    def delete(self, *argv):
        
        item_data = client.delete_item(
            self.__creds.api_key_v2,
            self.id,
            *argv)

        return Item(creds=self.__creds, **item_data)


    def add_update(self, body: str, *argv):
        
        update_data = client.create_update(
            self.__creds.api_key_v2, 
            body, 
            self.id,
            *argv)

        return Update(**update_data)

    
    def get_updates(self, *argv, **kwargs):
        
        updates_data = client.get_updates(
            self.__creds.api_key_v2,
            *argv, 
            **kwargs)

        return [Update(**update_data) for update_data in updates_data]