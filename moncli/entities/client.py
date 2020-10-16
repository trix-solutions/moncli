from .. import api_v2 as client, config, enums, entities as en
from ..api_v2 import constants
from ..decorators import default_field_list, optional_arguments


class MondayClient():
    def __init__(self, user_name: str, api_key_v1: str, api_key_v2: str):    
        self.__creds: en.MondayClientCredentials = en.MondayClientCredentials(api_key_v1, api_key_v2)
        self.__me = None

        if self.me.email.lower() != user_name.lower():
            raise AuthorizationError(user_name)

    @property
    def me(self):
        """Retrieve login user"""
        if not self.__me:
            self.__me = self.get_me()
        return self.__me

    @optional_arguments(constants.CREATE_BOARD_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_BOARD_QUERY_FIELDS)
    def create_board(self, board_name: str, board_kind: enums.BoardKind, *args):
        board_data = client.create_board(
            self.__creds.api_key_v2, 
            board_name, 
            board_kind, 
            *args)
        return en.Board(creds=self.__creds, **board_data)

    @optional_arguments(constants.BOARDS_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_BOARD_QUERY_FIELDS)
    def get_boards(self, *args, **kwargs):
        boards_data = client.get_boards(
            self.__creds.api_key_v2, 
            *args, 
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

    @optional_arguments(constants.BOARDS_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_BOARD_QUERY_FIELDS)
    def get_board_by_id(self, id: str, *args):
        try:
            board_data = client.get_boards(
                self.__creds.api_key_v2, 
                *args,
                ids=[int(id)],
                limit=1)[0]
        except IndexError:
            raise BoardNotFound('id', id)
        return en.Board(creds=self.__creds, **board_data)

    def get_board_by_name(self, name: str, *args):
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
                return self.get_board_by_id(target_board['id'], *args)
            except KeyError:
                if len(target_board) == 0:
                    page += 1
                    record_count = len(boards_data)
                    continue
        raise BoardNotFound('name', name)   

    @optional_arguments(constants.ARCHIVE_BOARD_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_BOARD_QUERY_FIELDS)
    def archive_board(self, board_id: str, *args):
        board_data = client.archive_board(
            self.__creds.api_key_v2, 
            board_id,
            *args)
        return en.Board(creds=self.__creds, **board_data)

    @optional_arguments(constants.ASSETS_OPTIONAL_PARAMS)
    def get_assets(self, ids: list, *args):
        """Retrieves the file assets for the login user's account.
        __________
        Parameters
        __________
        ids : `list[int/str]`
            Ids of the assets/files you want to get.
            Example:
            >>> client.get_assets(ids=['12345678'])
        *args : `str`
            The list asset return fields.

        _______
        Returns
        _______
        assets : `list[moncli.entities.asset.Asset]`
            A list of file assets uploaded to the account.

        _____________
        Return Fields
        _____________
        created_at : `str`
            The file's creation date.
        file_extension : `str`
            The file's extension.
        file_size : `int`
            The file's size in bytes.
        id : `str`
            The file's unique identifier.
        name : `str`
            The file's name.
        public_url : `str`
            Public url to the asset, valid for 1 hour.
        uploaded_by : `moncli.entities.user.User`
            The user who uploaded the file
        url : `str`
            The user who uploaded the file
        url_thumbnail : `str`
            Url to view the asset in thumbnail mode. Only available for images.
        """
        
        if not ids:
            raise AssetIdsRequired()

        assets_data = client.get_assets(
            self.__creds.api_key_v2,
            ids,
            *args)
        return [en.asset.Asset(**data) for data in assets_data]
    
    def get_items(self, *args,  **kwargs):
        items_data = client.get_items(
            self.__creds.api_key_v2, 
            *args,
            **kwargs)
        return [en.Item(creds=self.__creds, **item_data) for item_data in items_data] 
        
    @optional_arguments(constants.UPDATES_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_UPDATE_QUERY_FIELDS)
    def get_updates(self, *args, **kwargs):
        updates_data = client.get_updates(
            self.__creds.api_key_v2, 
            *args,
            **kwargs)
        return [en.Update(creds=self.__creds, **update_data) for update_data in updates_data]
    
    @optional_arguments(constants.CREATE_NOTIFICATION_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_NOTIFICATION_QUERY_FIELDS)
    def create_notification(self, text: str, user_id: str, target_id: str, target_type: enums.NotificationTargetType, *args, **kwargs):
        notification_data = client.create_notification(
            self.__creds.api_key_v2, 
            text, 
            user_id, 
            target_id,
            target_type,
            *args,
            **kwargs)
        return en.Notification(notification_data)
    
    @optional_arguments(constants.CREATE_OR_GET_TAG_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_TAG_QUERY_FIELDS)
    def create_or_get_tag(self, tag_name: str, *args, **kwargs):
        tag_data = client.create_or_get_tag(
            self.__creds.api_key_v2, 
            tag_name,
            *args)
        return en.Tag(tag_data)
        
    @optional_arguments(constants.TAGS_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_TAG_QUERY_FIELDS)
    def get_tags(self, *args, **kwargs):
        
        tags_data = client.get_tags(
            self.__creds.api_key_v2,
            *args,
            **kwargs)
        return [en.Tag(tag_data) for tag_data in tags_data]
    
    @optional_arguments(constants.USERS_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_USER_QUERY_FIELDS)
    def get_users(self, *args, **kwargs):
        
        users_data = client.get_users(
            self.__creds.api_key_v2, 
            *args,
            **kwargs)
        return [en.User(creds=self.__creds, **user_data) for user_data in users_data]
    
    @optional_arguments(constants.TEAMS_OPTIONAL_PARAMS)
    @default_field_list(config.DEFAULT_TEAM_QUERY_FIELDS)
    def get_teams(self, *args, **kwargs):
        teams_data = client.get_teams(
            self.__creds.api_key_v2,
            *args,
            **kwargs)
        return [en.Team(creds=self.__creds, **team_data) for team_data in teams_data]
    
    @default_field_list(config.DEFAULT_USER_QUERY_FIELDS)
    def get_me(self, *args):
        user_data = client.get_me(
            self.__creds.api_key_v2, 
            *args)
        return en.User(creds=self.__creds, **user_data)

    @default_field_list(config.DEFAULT_ACCOUNT_QUERY_FIELDS)
    def get_account(self, *args):
        account_data = client.get_account(
            self.__creds.api_key_v2,
            *args)
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

class AssetIdsRequired(Exception):
    def __init__(self):
        self.message = "Ids parameter is required."

