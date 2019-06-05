from datetime import datetime

from moncli.routes import boards 
from .constants import DATE_FORMAT, COLUMN_COLOR

class Board():

    def __init__(self, data, user):

        self.__data = data
        self.__user = user

        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.board_kind = data['board_kind']
        self.created_at = datetime.strptime(data['created_at'], DATE_FORMAT)
        self.updated_at = datetime.strptime(data['updated_at'], DATE_FORMAT)
        self.columns = [Column(column_data) for column_data in data['columns']]
        self.groups = [Group(group_data) for group_data in data['groups']]

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


    