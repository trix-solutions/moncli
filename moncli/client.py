from moncli.routes import users, boards
from .boards import Board
from .users import User

class MondayClient():

    def __init__(self, username, api_key):
     
        self.__api_key = api_key
        self.__user = self.get_user(username)


    def get_user(self, username):

        record_count = 100
        page = 1

        while record_count == 100:

            this_page = users.get_users(self.__api_key, page, record_count)

            target_user = [user for user in this_page if user['email'] == username]

            if (len(target_user) == 0):
                record_count = len(this_page)
                continue

            return User(target_user[0])
        
        raise UserNotFound(username)


    def get_boards(self, per_page = 25, only_globals = False, order_by_latest = False):

        result = []

        resp_list = boards.get_boards(self.__api_key, per_page, only_globals, order_by_latest)

        for resp in resp_list:
            result.append(Board(resp))

        return result


    def get_board(self, name):

        for resp in boards.get_boards(self.__api_key):

            if resp['name'].lower() == name.lower():           
                return Board(resp)
        
        raise BoardNotFound('name', name)


    def get_board_by_id(self, board_id):

        resp = boards.get_board_by_id(self.__api_key, board_id)

        return Board(resp)


class BoardNotFound(Exception):

    def __init__(self, search_type, value):
        
        if search_type == 'id':
            self.message = 'Unable to find board with name: "{}".'.format(value)
        
        elif search_type == 'name':
            self.message = 'Unable to find board with the ID: "{}".'.format(value)

        else:
            self.message = 'Unable to find the requested board.'

class UserNotFound(Exception):

    def __init__(self, username):

        self.message = 'Unable to find user with username: "{}".'.format(username)