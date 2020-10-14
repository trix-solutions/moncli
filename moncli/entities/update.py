from .. import api_v2 as client
from .. import entities as e

class Update():

    def __init__(self, **kwargs):
        self.__creds = kwargs['creds']
        self.id = kwargs['id']
        
        for key, value in kwargs.items():

            if key == 'body':
                self.body = value


    def add_file(self, file_path: str):

        asset_data = client.add_file_to_update(
            self.__creds.api_key_v2,
            self.id,
            file_path,
            'id', 'name', 'url')

        return e.objects.Asset(**asset_data)
