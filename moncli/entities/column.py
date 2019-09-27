from .. import api_v2 as client
from .item import Item

class Column():

    def __init__(self, **kwargs):
        self.__creds = kwargs['creds']
        self.id = kwargs['id']

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

            elif key == 'board_id':
                self.board_id = value

    
    def change_value(self, item_id, value: str, *argv):

        item_data = client.change_column_value(
            self.__creds.api_key_v2,
            item_id,
            self.id,
            self.board_id,
            value,
            *argv)
        
        return Item(creds=self.__creds, **item_data)


    def change_multiple_value(self, item_id: str, column_values: str, *argv):
        
        item_data = client.change_multiple_column_value(
            self.__creds.api_key_v2,
            item_id,
            self.board_id,
            column_values,
            *argv)

        return Item(creds=self.__creds, **item_data)