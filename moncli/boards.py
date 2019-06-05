from datetime import datetime

from moncli.routes import boards 
from .constants import DATE_FORMAT, COLUMN_COLOR

class Board():

    def __init__(self, data, api_key, user):

        self.__data = data
        self.__api_key = api_key
        self.__user = user

        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.board_kind = data['board_kind']
        self.created_at = datetime.strptime(data['created_at'], DATE_FORMAT)
        self.updated_at = datetime.strptime(data['updated_at'], DATE_FORMAT)
        self.columns = [Column(column_data) for column_data in data['columns']]
        self.groups = [Group(group_data) for group_data in data['groups']]

        group_iter = ((group.title, group) for group in self.groups)
        self.__group_map = {title:group for (title, group) in group_iter}


    def get_pulses(self, group_name = None):

        record_count = 25
        results = []
        page = 1

        while record_count == 25:

            this_page = boards.get_board_pulses(self.__api_key, self.id, page, record_count)

            if len(this_page) == 0:
                return results

            if group_name == None:
                results += this_page
            else:
                group_id = self.__group_map[group_name].id
                results += [pulse for pulse in this_page if pulse['board_meta']['group_id'] == group_id]

            record_count = len(this_page)
            page += 1

        return results


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


    