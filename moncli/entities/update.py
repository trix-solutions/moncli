from .. import api_v2 as client
from .. import entities as e

class Update():

    def __init__(self, **kwargs):
        self.__creds = kwargs['creds']
        self.id = kwargs['id']
        
        for key, value in kwargs.items():

            if key == 'assets':
                self.assets = [e.objects.Asset(**asset_data) for asset_data in value]

            if key == 'body':
                self.body = value

            if key == 'item_id':
                self.item_id = value

            if key == 'created_at':
                self.created_at = value

            if key == 'creator':
                self.creator = e.user.User(**value)
            
            if key == 'creator_id':
                self.creator_id = value

            if key == 'text_body':
                self.text_body = value

            if key == 'update_at':
                self.update_at = value


    def add_file(self, file_path: str):

        asset_data = client.add_file_to_update(
            self.__creds.api_key_v2,
            self.id,
            file_path,
            'id', 'name', 'url')

        return e.objects.Asset(**asset_data)
