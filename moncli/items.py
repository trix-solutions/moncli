from .boards import Board, Group

class Item():

    def __init__(self, api_key_v1: str, api_key_v2: str, **kwargs):
        self.__api_key_v2 = api_key_v2
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

            if key == 'creator_id':
                self.creator_id = value

            if key == 'group':
                self.__group_id = value['id']

            if key == 'state':
                self.state = value
            
            if key == 'subscribers':
                self.__subscriber_ids = [int(item['id']) for item in value]


class ColumnValue():

    def __init__(self, api_key_v2: str, **kwargs):
        pass