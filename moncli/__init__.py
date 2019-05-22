from moncli.routes import get_boards, get_board_by_id

class MondayClient():

    def __init__(self, api_key):
     
        self.__api_key = api_key

    
    def get_boards(self, per_page = 25, only_globals = False, order_by_latest = False):

        return get_boards(self.__api_key, per_page, only_globals, order_by_latest)


    def get_board(self, name):

        for board in get_boards(self.__api_key):

            if board['name'].lower() == name.lower():           
                return board
        
        raise BoardNotFound('name', name)


    def get_board_by_id(self, board_id):

        return get_board_by_id(self.__api_key, board_id)


class BoardNotFound(Exception):

    def __init__(self, search_type, value):
        
        if search_type == 'id':
            self.message = 'Unable to find board with name: "{}".'.format(value)
        
        elif search_type == 'name':
            self.message = 'Unable to find board with the ID: "{}".'.format(value)

        else:
            self.message = 'Unable to find the requested board.'