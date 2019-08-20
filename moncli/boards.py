from datetime import datetime
from typing import List

from .graphql import boards, items 
from .constants import DATETIME_FORMAT, COLUMN_COLOR

class Board():

    def __init__(self, api_key_v1: str, api_key_v2: str, **kwargs):

        self.__api_key_v1 = api_key_v1
        self.__api_key_v2 = api_key_v2

        self.id = kwargs['id']
        self.name = kwargs['name']

        for key, value in kwargs.items():

            if key == 'board_folder_id':
                self.board_folder_id = value
            
            elif key == 'board_kind':
                self.board_kind = value

            elif key == 'description':
                self.description = value

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


    def get_items(self, group_name = None):
        pass


    def add_pulse(self, name, group_name, update_text = None, add_to_bottom = False):
        pass


class Column():

    def __init__(self, data):

        self.__data = data

        self.id = data['id']
        self.title = data['title']
        self.type = data['type']
        
        if self.type == COLUMN_COLOR:
            self.labels = data['labels']


class Group():

    def __init__(self, data):

        self.__data = data

        self.id = data['id']
        self.title = data['title']
        self.board_id = data['board_id']

class GroupNotFound(Exception):

    def __init__(self, board, group_name):

        self.board_id = board.id
        self.board_name = board.name
        self.group_name = group_name
        self.message = 'Unable to find group {} in board {}.'.format(self.group_name, self.board_name)

    