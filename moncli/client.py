from typing import List

from .graphql import boards, items
from .boards import Board, Item
from .users import User

class MondayClient():

    def __init__(self, api_key_v1: str, api_key_v2: str):
     
        self.__api_key_v1 = api_key_v1
        self.__api_key_v2 = api_key_v2


    def get_boards(self, **kwargs):

        result = []

        resp_boards = boards.get_boards(self.__api_key_v2, 'id', 'name', **kwargs)

        for board_data in resp_boards:
            result.append(Board(self.__api_key_v1, self.__api_key_v2, **board_data))

        return result


    def get_board(self, id: str = None, name: str = None):

        field_list = [
            'id', 
            'name', 
            'board_folder_id', 
            'board_kind', 
            'description', 
            'items.id', 
            'owner.id', 
            'permissions',
            'pos',
            'state']

        if id != None and name != None:
            raise TooManyGetBoardParameters()

        elif id == None and name == None:
            raise NotEnoughGetBoardParameters()

        # Search for single board by ID
        elif id != None:
            resp_boards = boards.get_boards(
                self.__api_key_v2, 
                *field_list,
                ids=int(id),
                limit=1)

            if len(resp_boards) == 0:
                raise BoardNotFound('id', id)

            return Board(self.__api_key_v1, self.__api_key_v2, **resp_boards[0])

        # Page through boards until name match appears.
        else:

            # Hard configure the pagination rate.
            page = 1
            page_limit = 1000
            record_count = 1000
            while record_count >= page_limit:
                resp_boards = boards.get_boards(
                    self.__api_key_v2, 
                    *field_list,
                    limit=page_limit,
                    page=page)

                target_boards = [board for board in resp_boards if board['name'].lower() == name.lower()]

                if len(target_boards) == 0:
                    page += 1
                    record_count = len(resp_boards)
                    continue

                return Board(self.__api_key_v1, self.__api_key_v2, **resp_boards[0])
        
            if len(target_boards) == 0:
                raise BoardNotFound('name', name)        

    
    def get_items(self, ids, **kwargs) -> List[Item]:

        items_resp = items.get_items(
            self.__api_key_v2, 
            'id',
            'name',
            'board.id',
            'board.name',
            'creator_id',
            'column_values.id',
            'column_values.text',
            'column_values.title',
            'column_values.value',
            'column_values.additional_info',
            'group.id',
            'state',
            'subscribers.id',
            ids=ids, 
            limit=1000)

        return [Item(self.__api_key_v1, self.__api_key_v2, **item_data) for item_data in items_resp] 
        

class BoardNotFound(Exception):

    def __init__(self, search_type, value):
        
        if search_type == 'id':
            self.message = 'Unable to find board with name: "{}".'.format(value)
        
        elif search_type == 'name':
            self.message = 'Unable to find board with the ID: "{}".'.format(value)

        else:
            self.message = 'Unable to find the requested board.'

class TooManyGetBoardParameters(Exception):

    def __init__(self):
        self.message = "Unable to use both 'id' and 'name' when querying for a board."

class NotEnoughGetBoardParameters(Exception):

    def __init__(self):
        self.message = "Either the 'id' or 'name' is required when querying a board."