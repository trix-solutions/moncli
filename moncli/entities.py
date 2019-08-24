from datetime import datetime

from moncli.constants import DATETIME_FORMAT
from moncli.enums import BoardKind, ColumnType, NotificationTargetType
from moncli.graphql.operations import *

class MondayClient():

    def __init__(self, api_key_v1: str, api_key_v2: str):
     
        self.__api_key_v1 = api_key_v1
        self.__api_key_v2 = api_key_v2
        

    def create_board(self, board_name: str, board_kind: BoardKind):

        resp_board = create_board(self.__api_key_v2, board_name, board_kind, 'id')

        return resp_board['id']
    

    def get_boards(self, **kwargs):

        result = []

        resp_boards = get_boards(self.__api_key_v2, 'id', 'name', **kwargs)

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
            resp_boards = get_boards(
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
                resp_boards = get_boards(
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

        items_resp = get_items(
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

    
    def get_updates(self, **kwargs):
        pass


class Board():

    def __init__(self, api_key_v1: str, api_key_v2: str, **kwargs):
        self.__columns = None
        self.__groups = None
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

    
    def get_columns(self):

        if self.__columns == None:

            board = get_boards(
                self.__api_key_v2,
                'columns.id',
                'columns.archived',
                'columns.settings_str',
                'columns.title',
                'columns.type',
                'columns.width',
                ids=int(self.id))[0]

            self.__columns = [Column(**column_data) for column_data in board['columns']]

        return self.__columns

    def get_groups(self):

        if self.__groups == None:
            
            board = get_boards(
                self.__api_key_v2,
                'groups.id',
                'groups.title',
                'groups.archived',
                'groups.color',
                'groups.deleted',
                'groups.items.id',
                'groups.position',
                ids=int(self.id))[0]

            self.__groups = [Group(**group_data) for group_data in board['groups']]

        return self.__groups


    def get_items(self):
        
        items_resp = get_items(
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
            ids=self.__item_ids, 
            limit=1000)

        return [Item(self.__api_key_v1, self.__api_key_v2, **item_data) for item_data in items_resp] 


    def add_item(self, item_name: str, **kwargs):

        item = create_item(self.__api_key_v2, item_name, self.id, 'id', **kwargs)

        return item['id']


class Column():

    def __init__(self, **kwargs):
        self.id= kwargs['id']

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


class Group():

    def __init__(self, api_key_v1: str, api_key_v2: str, **kwargs):
        self.__api_key_v1 = api_key_v1
        self.__api_key_v2 = api_key_v2
        self.id = kwargs['id']
        self.__item_ids = None

        for key, value in kwargs.items():

            if key == 'title':
                self.title = value

            elif key == 'archived':
                self.archived = value
            
            elif key == 'color':
                self.color = value

            elif key == 'deleted':
                self.deleted = value

            elif key == 'items':
                self.__item_ids = [int(item['id'] for item in value)]

            elif key == 'position':
                self.position = value
    

    def get_items(self):

        items_resp = get_items(
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
            ids=self.__item_ids, 
            limit=1000)

        return [Item(self.__api_key_v1, self.__api_key_v2, **item_data) for item_data in items_resp] 


class Item():

    def __init__(self, api_key_v1: str, api_key_v2: str, **kwargs):
        self.__api_key_v2 = api_key_v2
        self.__column_values = None
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

            elif key == 'column_values':
                self.__column_values = [ColumnValue(**column_values) for column_values in value]

            elif key == 'creator_id':
                self.creator_id = value

            elif key == 'group':
                self.__group_id = value['id']

            elif key == 'state':
                self.state = value
            
            elif key == 'subscribers':
                self.__subscriber_ids = [int(item['id']) for item in value]

        
    def get_column_values(self):

        if self.__column_values == None:           
            item = get_items(
                self.__api_key_v2,
                'column_values.id',
                'column_values.text',
                'column_values.title',
                'column_values.value',
                'column_values.additional_info',
                ids=int(self.id))
                
            self.__column_values = [ColumnValue(**column_values) for column_values in item['column_values']]

        return self.__column_values


class ColumnValue():

    def __init__(self, **kwargs):
        self.id = kwargs['id']

        for key, value in kwargs.items():

            if key == 'text':
                self.text = value

            if key == 'title':
                self.title = value

            if key == 'value':
                self.value = value

            if key == 'additional_info':
                self.additional_info = value


class User():

    def __init__(self, resp):

        self.id = resp['id']
        self.name = resp['name']
        self.username = resp['email']
        self.title = resp['title']
        self.position = resp['position']
        self.phone = resp['phone']
        self.location = resp['location']
        self.status = resp['status']
        self.birthday = resp['birthday']
        self.is_guest = resp['is_guest']
        self.created_at = datetime.strptime(resp['created_at'], DATETIME_FORMAT)
        self.updated_at = datetime.strptime(resp['updated_at'], DATETIME_FORMAT)


class GroupNotFound(Exception):

    def __init__(self, board, group_name):

        self.board_id = board.id
        self.board_name = board.name
        self.group_name = group_name
        self.message = 'Unable to find group {} in board {}.'.format(self.group_name, self.board_name)
    
        

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