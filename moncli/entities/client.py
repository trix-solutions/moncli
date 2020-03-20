from .. import api_v2 as client
from ..enums import BoardKind, NotificationTargetType
from .objects import MondayClientCredentials, Tag, Update, Notification
from . import exceptions as ex
from .board import Board
from .item import Item
from .user import User, Team


GET_BOARD_FIELD_LIST = [
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

class MondayClient():

    def __init__(self, user_name: str, api_key_v1: str, api_key_v2: str):
     
        self.__creds: MondayClientCredentials = MondayClientCredentials(api_key_v1, api_key_v2)

        me: User = self.get_me()
        if me.email.lower() != user_name.lower():
            raise ex.AuthorizationError(user_name)
        

    def create_board(self, board_name: str, board_kind: BoardKind):

        field_list = [
            'id', 
            'name', 
            'board_folder_id', 
            'board_kind', 
            'description', 
            'owner.id', 
            'permissions',
            'pos',
            'state']

        board_data = client.create_board(
            self.__creds.api_key_v2, 
            board_name, 
            board_kind, 
            *field_list)

        return Board(creds=self.__creds, **board_data)
    

    def get_boards(self, **kwargs):

        boards_data = client.get_boards(
            self.__creds.api_key_v2, 
            'id', 
            'name', 
            **kwargs)

        return [
            Board(creds=self.__creds, **board_data)
            for board_data
            in boards_data
        ]


    def get_board(self, id: str = None, name: str = None):

        if id != None and name != None:
            raise ex.TooManyGetBoardParameters()

        if id == None and name == None:
            raise ex.NotEnoughGetBoardParameters()

        if id != None:         
            return self.get_board_by_id(id)
        else:
            return self.get_board_by_name(name)


    def get_board_by_id(self, id: str):

        boards_data = client.get_boards(
            self.__creds.api_key_v2, 
            *GET_BOARD_FIELD_LIST,
            ids=[int(id)],
            limit=1)

        if len(boards_data) == 0:
            raise ex.BoardNotFound('id', id)

        return Board(creds=self.__creds, **boards_data[0])


    def get_board_by_name(self, name: str):

        # Hard configure the pagination rate.
        page = 1
        page_limit = 500
        record_count = 500

        while record_count >= page_limit:

            boards_data = client.get_boards(
                self.__creds.api_key_v2, 
                'id', 'name',
                limit=page_limit,
                page=page)

            target_boards = [board for board in boards_data if board['name'].lower() == name.lower()]

            if len(target_boards) == 0:
                page += 1
                record_count = len(boards_data)
                continue

            return self.get_board_by_id(target_boards[0]['id'])
    
        if len(target_boards) == 0:
            raise ex.BoardNotFound('name', name)   


    def archive_board(self, board_id: str):

        board_data = client.archive_board(
            self.__creds.api_key_v2, 
            board_id,
            'id')

        return Board(creds=self.__creds, **board_data)

    
    def get_items(self, **kwargs):

        items_data = client.get_items(
            self.__creds.api_key_v2, 
            'id',
            'name',
            'board.id',
            'creator_id',
            'column_values.id',
            'column_values.text',
            'column_values.title',
            'column_values.value',
            'column_values.additional_info',
            'group.id',
            'state',
            'subscribers.id',
            **kwargs)

        return [Item(creds=self.__creds, **item_data) for item_data in items_data] 

    
    def get_updates(self, **kwargs):
        
        updates_data = client.get_updates(
            self.__creds.api_key_v2, 
            'id',
            'body',
            **kwargs)

        return [Update(**update_data) for update_data in updates_data]


    def create_notification(self, text: str, user_id: str, target_id: str, target_type: NotificationTargetType, **kwargs):

        notification_data = client.create_notification(
            self.__creds.api_key_v2, 
            text, 
            user_id, 
            target_id,
            target_type,
            'id',
            'text',
            **kwargs)

        return Notification(**notification_data)


    def create_or_get_tag(self, tag_name: str, **kwargs):
        
        tag_data = client.create_or_get_tag(
            self.__creds.api_key_v2, 
            tag_name,
            'id',
            'name',
            'color')

        return Tag(**tag_data)

    
    def get_tags(self, **kwargs):
        
        tags_data = client.get_tags(
            self.__creds.api_key_v2,
            'id',
            'name',
            'color',
            **kwargs)

        return [Tag(**tag_data) for tag_data in tags_data]


    def get_users(self, **kwargs):
        
        users_data = client.get_users(
            self.__creds.api_key_v2, 
            'id',
            'name',
            'url',
            'email',
            'enabled',
            'account.id',
            'teams.id',
            'birthday',
            'country_code',
            'created_at',
            'is_guest',
            'is_pending',
            'join_date',
            **kwargs)

        return [User(creds=self.__creds, **user_data) for user_data in users_data]


    def get_teams(self, **kwargs):
        
        teams_data = client.get_teams(
            self.__creds.api_key_v2,
            'id',
            'name',
            'picture_url',
            'users.id',
            **kwargs)

        return [Team(creds=self.__creds, **team_data) for team_data in teams_data]

    
    def get_me(self):

        user_data = client.get_me(
            self.__creds.api_key_v2, 
            'id',
            'name',
            'url',
            'email',
            'enabled',
            'account.id',
            'teams.id',
            'birthday',
            'country_code',
            'created_at',
            'is_guest',
            'is_pending',
            'join_date')

        return User(creds=self.__creds, **user_data)