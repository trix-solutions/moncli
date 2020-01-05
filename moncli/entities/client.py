from .. import api_v2 as client, config, enums, entities as en


class MondayClient():

    def __init__(self, user_name: str, api_key_v1: str, api_key_v2: str):    
        self.__creds: en.MondayClientCredentials = en.MondayClientCredentials(api_key_v1, api_key_v2)
        self.__me = None

        if self.me.email.lower() != user_name.lower():
            raise AuthorizationError(user_name)

    @property
    def me(self):
        if not self.__me:
            self.__me = self.get_me()
        return self.__me
        
    def create_board(self, board_name: str, board_kind: enums.BoardKind):
        field_list = config.DEFAULT_BOARD_QUERY_FIELDS
        board_data = client.create_board(
            self.__creds.api_key_v2, 
            board_name, 
            board_kind, 
            *field_list)

        return en.Board(creds=self.__creds, **board_data)
    
    def get_boards(self, **kwargs):
        field_list = ['id', 'name']
        boards_data = client.get_boards(
            self.__creds.api_key_v2, 
            *field_list, 
            **kwargs)

        return [en.Board(creds=self.__creds, **data) for data in boards_data]

    def get_board(self, id: str = None, name: str = None):
        if id != None and name != None:
            raise TooManyGetBoardParameters()
        if id == None and name == None:
            raise NotEnoughGetBoardParameters()
        if id != None:         
            return self.get_board_by_id(id)
        else:
            return self.get_board_by_name(name)

    def get_board_by_id(self, id: str):
        field_list = config.DEFAULT_BOARD_QUERY_FIELDS
        try:
            board_data = client.get_boards(
                self.__creds.api_key_v2, 
                *field_list,
                ids=[int(id)],
                limit=1)[0]
        except IndexError:
            raise BoardNotFound('id', id)

        return en.Board(creds=self.__creds, **board_data)

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
            
            try:
                target_board = [board for board in boards_data if board['name'].lower() == name.lower()][0]
                return self.get_board_by_id(target_board['id'])
            except KeyError:
                if len(target_board) == 0:
                    page += 1
                    record_count = len(boards_data)
                    continue

        raise BoardNotFound('name', name)   

    def archive_board(self, board_id: str):
        field_list = config.DEFAULT_BOARD_QUERY_FIELDS
        board_data = client.archive_board(
            self.__creds.api_key_v2, 
            board_id,
            *field_list)

        return en.Board(creds=self.__creds, **board_data)
    
    def get_items(self, **kwargs):
        field_list = config.DEFAULT_ITEM_QUERY_FIELDS
        items_data = client.get_items(
            self.__creds.api_key_v2, 
            *field_list,
            **kwargs)

        return [en.Item(creds=self.__creds, **item_data) for item_data in items_data] 
    
    def get_updates(self, **kwargs):
        field_list = config.DEFAULT_UPDATE_QUERY_FIELDS
        updates_data = client.get_updates(
            self.__creds.api_key_v2, 
            *field_list,
            **kwargs)

        return [en.Update(update_data) for update_data in updates_data]

    def create_notification(self, text: str, user_id: str, target_id: str, target_type: enums.NotificationTargetType, **kwargs):
        field_list = config.DEFAULT_NOTIFICATION_QUERY_FIELDS
        notification_data = client.create_notification(
            self.__creds.api_key_v2, 
            text, 
            user_id, 
            target_id,
            target_type,
            *field_list,
            **kwargs)

        return en.Notification(notification_data)

    def create_or_get_tag(self, tag_name: str, **kwargs):
        field_list = config.DEFAULT_TAG_QUERY_FIELDS
        tag_data = client.create_or_get_tag(
            self.__creds.api_key_v2, 
            tag_name,
            *field_list)

        return en.Tag(tag_data)
    
    def get_tags(self, **kwargs):
        
        tags_data = client.get_tags(
            self.__creds.api_key_v2,
            *config.DEFAULT_TAG_QUERY_FIELDS,
            **kwargs)

        return [en.Tag(tag_data) for tag_data in tags_data]

    def get_users(self, **kwargs):
        
        users_data = client.get_users(
            self.__creds.api_key_v2, 
            *config.DEFAULT_USER_QUERY_FIELDS,
            **kwargs)

        return [en.User(creds=self.__creds, **user_data) for user_data in users_data]

    def get_teams(self, **kwargs):
        field_list = config.DEFAULT_TEAM_QUERY_FIELDS
        teams_data = client.get_teams(
            self.__creds.api_key_v2,
            *field_list,
            **kwargs)

        return [en.Team(creds=self.__creds, **team_data) for team_data in teams_data]
    
    def get_me(self):
        field_list = config.DEFAULT_USER_QUERY_FIELDS
        user_data = client.get_me(
            self.__creds.api_key_v2, 
            *field_list)

        return en.User(creds=self.__creds, **user_data)

    def get_account(self):
        field_list = config.DEFAULT_ACCOUNT_QUERY_FIELDS
        account_data = client.get_account(
            self.__creds.api_key_v2,
            *field_list)

        return en.Account(creds=self.__creds, **account_data)


class AuthorizationError(Exception):
    def __init__(self, user_name: str):
        self.message = 'User {} was not recognized by the applied token'.format(user_name)


class TooManyGetBoardParameters(Exception):
    def __init__(self):
        self.message = "Unable to use both 'id' and 'name' when querying for a board."
        

class NotEnoughGetBoardParameters(Exception):
    def __init__(self):
        self.message = "Either the 'id' or 'name' is required when querying a board."


class BoardNotFound(Exception):
    def __init__(self, search_type, value):        
        if search_type == 'id':
            self.message = 'Unable to find board with name: "{}".'.format(value)       
        elif search_type == 'name':
            self.message = 'Unable to find board with the ID: "{}".'.format(value)
        else:
            self.message = 'Unable to find the requested board.'

