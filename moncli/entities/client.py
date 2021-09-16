from .. import api, entities as en
from ..enums import *


class MondayClient():
    """monday.com client for login and board/item management

        Properties

            me : `moncli.entities.User`
                The client login user.

        Methods

            create_board : `moncli.entities.Board`
                Create a new board.
            get_boards : `list[moncli.entities.Board]`
                Get a collection of boards.
            get_board : `moncli.entities.Board`
                Get a board by unique identifier or name.
            get_board_by_id : `moncli.entities.Board`
                Get a board by unique identifier.
            get_board_by_name : `moncli.entities.Board`
                Get a board by name.
            archive_board : `moncli.entities.Board`
                Archive a board.
            get_assets : `list[monlci.entities.Asset]`
                Get a collection of assets by IDs.
            get_items : `list[moncli.entities.Item]`
                Get a collection of items.
            get_updates : `list[moncli.entities.Update]`
                Get a collection of updates.
            delete_update : `moncli.entities.Update`
                Delete an update.
            clear_item_updates: `moncli.entities.Item`
                Clear an item's updates.
            create_notification : `moncli.entities.Notification`
                Create a new notification.
            create_or_get_tag : `moncli.entities.Tag`
                Create a new tag or get it if it already exists.
            get_tags : `list[moncli.entities.Tag]`
                Get a collection of tags.
            get_users : `list[moncli.entities.User]`
                Get a collection of users.
            get_teams : `list[moncli.entities.Team]`
                Get a collection of teams.
            get_me : `moncli.entities.User`
                Get the connected user's information.
            get_account : `moncli.entities.Account`
                Get the connected user's account.
            create_workspace : `moncli.entities.Workspace`
                Create a new workspace.
            add_users_to_workspace: `moncli.entities.Workspace`
                Adds new users to a new workspace.
            delete_users_from_workspace: `moncli.entities.Workspace`
                Deletes  users from an existing workspace.
            add_teams_to_workspace: `moncli.entities.Workspace`
                Allows you to add teams to a workspace.
            delete_teams_from_workspace: `moncli.entities.Workspace`
                Allows you to remove teams to a workspace.
    """

    def __init__(self, **kwargs):    
        self.__me = None
        self.__creds = en.MondayClientCredentials()

        try:
            username = kwargs['user_name']
        except KeyError:
            username = None

        try:
            api_key_v1 = kwargs['api_key_v1']
        except KeyError:
            api_key_v1 = None

        try:
            api_key_v2 = kwargs['api_key_v2']
        except KeyError:
            api_key_v2 = None

        if api_key_v1:
            self.__creds.api_key_v1 = api_key_v1

        if api_key_v2:
            self.api_key_v2 = api_key_v2
        
        # Only "login" when user_name and API Key v2 are provided.
        if username and api_key_v2 and self.me.email.lower() != username.lower():
            raise AuthorizationError(username)

    @property
    def me(self):
        """Retrieve login user"""
        if not self.__me:
            self.__me = self.get_me()
        return self.__me

    @property
    def api_key_v2(self):
        """Get API Key V2"""
        return self.__creds.api_key_v2

    @api_key_v2.setter
    def api_key_v2(self, value):
        """Set API Key V2"""
        self.__creds.api_key_v2 = value
        api.api_key = value


    def create_board(self, board_name: str, board_kind: BoardKind, *args, **kwargs):
        """Create a new board.

            Parameters

                board_name : `str`
                    The board's name.
                board_kind : `moncli.enums.BoardKind`
                    The board's kind (public / private / share)
                args : `tuple`
                    The list of board return fields.
                kwargs : `dict`
                    Optional keyword arguments for creating a board.

            Returns

                board : `moncli.entities.Board`
                    The newly created board.

            Return Fields

                activity_logs : `list[moncli.entities.ActivityLog]`
                    The board log events.
                board_folder_id : `int`
                    The board's folder unique identifier.
                board_kind : `str`
                    The board's kind (public / private / share).
                columns : `list[moncli.entities.Column]`
                    The board's visible columns.
                communication : `str`
                    Get the board communication value - typically meeting ID.
                description : `str`
                    The board's description.
                groups : `list[moncli.entities.Group]`
                    The board's visible groups.
                id : `str`
                    The unique identifier of the board.
                items : `list[moncli.entities.Item]`
                    The board's items (rows).
                name : `str`
                    The board's name.
                owner : `moncli.entities.user.User`
                    The owner of the board.
                permissions : `str`
                    The board's permissions.
                pos : `str`
                    The board's position.
                state : `str`
                    The board's state (all / active / archived / deleted).
                subscribers : `list[moncli.entities.User]`
                    The board's subscribers.
                tags : `list[moncli.entities.Tag]`
                    The board's specific tags.
                top_group : `moncli.entities.Group`
                    The top group at this board.
                updated_at : `str`
                    The last time the board was updated at (ISO8601 DateTime).
                updates : `list[moncli.entities.Update]`
                    The board's updates.
                views : `list[moncli.entities.BoardView]`
                    The board's views.
                workspace : `moncli.entities.Workspace`
                    The workspace that contains this board (null for main workspace).
                workspace_id : `str`
                    The board's workspace unique identifier (null for main workspace).

            Optional Arguments

                workspace_id : `str`
                    Optional workspace id.
                template_id : `str`
                    Optional board template id.
        """
        
        board_data = api.create_board(
            board_name, 
            board_kind, 
            *args,
            api_key=self.__creds.api_key_v2, 
            **kwargs)
        return en.Board(creds=self.__creds, **board_data)


    def get_boards(self, *args, **kwargs):
        """Get a collection of boards.

            Parameters

                args : `tuple`
                    The list of board return fields.
                kwargs : `dict`
                    Optional keyword arguments for getting boards.

            Returns

                boards : `list[moncli.entities.Board]`
                    The collection of boards.

            Return Fields

                activity_logs : `list[moncli.entities.ActivityLog]`
                    The board log events.
                board_folder_id : `int`
                    The board's folder unique identifier.
                board_kind : `str`
                    The board's kind (public / private / share).
                columns : `list[moncli.entities.Column]`
                    The board's visible columns.
                communication : `str`
                    Get the board communication value - typically meeting ID.
                description : `str`
                    The board's description.
                groups : `list[moncli.entities.Group]`
                    The board's visible groups.
                id : `str`
                    The unique identifier of the board.
                items : `list[moncli.entities.Item]`
                    The board's items (rows).
                name : `str`
                    The board's name.
                owner : `moncli.entities.user.User`
                    The owner of the board.
                permissions : `str`
                    The board's permissions.
                pos : `str`
                    The board's position.
                state : `str`
                    The board's state (all / active / archived / deleted).
                subscribers : `list[moncli.entities.User]`
                    The board's subscribers.
                tags : `list[moncli.entities.Tag]`
                    The board's specific tags.
                top_group : `moncli.entities.Group`
                    The top group at this board.
                updated_at : `str`
                    The last time the board was updated at (ISO8601 DateTime).
                updates : `list[moncli.entities.Update]`
                    The board's updates.
                views : `list[moncli.entities.BoardView]`
                    The board's views.
                workspace : `moncli.entities.Workspace`
                    The workspace that contains this board (null for main workspace).
                workspace_id : `str`
                    The board's workspace unique identifier (null for main workspace).

            Optional Arguments

                limit : `int`
                    Number of boards to get; the default is 25.
                page : `int`
                    Page number to get, starting at 1.
                ids : `list[str]`
                    A list of boards unique identifiers.
                board_kind : `moncli.enums.BoardKind`
                    The board's kind (public / private / share)
                state : `moncli.enums.State`
                    The state of the board (all / active / archived / deleted), the default is active.
                order_by : `moncli.enums.BoardsOrderBy`
                    The order in which to retrieve your boards (created_at / used_at). 
        """

        # Add columns to board if column_values are asked for.
        args = list(args)
        for arg in args:
            if 'column_values' in arg:
                args.append('columns.id')
                args.append('columns.type')
                args.append('columns.settings_str')
                break
        
        boards_data = api.get_boards(
            *args, 
            api_key=self.__creds.api_key_v2, 
            **kwargs)

        for data in boards_data:
            try:
                for item_data in data['items']:
                    item_data['board'] = {'id': data['id']}
                    if item_data.__contains__('column_values'):
                        item_data['board']['columns'] = data['columns']
            except:
                break


        return [en.Board(creds=self.__creds, **data) for data in boards_data]


    def get_board(self, id: str = None, name: str = None, *args):
        """Get a board by unique identifier or name.

            Parameters

                id : `str`
                    The unique identifier of the board to retrieve.
                    NOTE: This parameter is mutually exclusive and cannot be used with 'name'.
                name : `str`
                    The name of the board to retrieve.
                    NOTE: This parameter is mutially exclusive and cannot be used with 'id'.
                args : `tuple`
                    The list of board return fields.

            Returns

                board : `moncli.entities.Board`
                    The board requested by ID or name

            Return Fields

                activity_logs : `list[moncli.entities.ActivityLog]`
                    The board log events.
                board_folder_id : `int`
                    The board's folder unique identifier.
                board_kind : `str`
                    The board's kind (public / private / share).
                columns : `list[moncli.entities.Column]`
                    The board's visible columns.
                communication : `str`
                    Get the board communication value - typically meeting ID.
                description : `str`
                    The board's description.
                groups : `list[moncli.entities.Group]`
                    The board's visible groups.
                id : `str`
                    The unique identifier of the board.
                items : `list[moncli.entities.Item]`
                    The board's items (rows).
                name : `str`
                    The board's name.
                owner : `moncli.entities.user.User`
                    The owner of the board.
                permissions : `str`
                    The board's permissions.
                pos : `str`
                    The board's position.
                state : `str`
                    The board's state (all / active / archived / deleted).
                subscribers : `list[moncli.entities.User]`
                    The board's subscribers.
                tags : `list[moncli.entities.Tag]`
                    The board's specific tags.
                top_group : `moncli.entities.Group`
                    The top group at this board.
                updated_at : `str`
                    The last time the board was updated at (ISO8601 DateTime).
                updates : `list[moncli.entities.Update]`
                    The board's updates.
                views : `list[moncli.entities.BoardView]`
                    The board's views.
                workspace : `moncli.entities.Workspace`
                    The workspace that contains this board (null for main workspace).
                workspace_id : `str`
                    The board's workspace unique identifier (null for main workspace).
        """
        
        if id != None and name != None:
            raise TooManyGetBoardParameters()
        if id == None and name == None:
            raise NotEnoughGetBoardParameters()
        if id != None:         
            return self.get_board_by_id(id)
        else:
            return self.get_board_by_name(name)


    def get_board_by_id(self, id: str, *args):
        """Get a board by unique identifier.

            Parameters

                id : `str`
                    The unique identifier of the board.
                args : `tuple`
                    The list of board return fields.

            Returns

                board : `moncli.entities.Board`
                    The board retrieved by ID.

            Return Fields

                activity_logs : `list[moncli.entities.ActivityLog]`
                    The board log events.
                board_folder_id : `int`
                    The board's folder unique identifier.
                board_kind : `str`
                    The board's kind (public / private / share).
                columns : `list[moncli.entities.Column]`
                    The board's visible columns.
                communication : `str`
                    Get the board communication value - typically meeting ID.
                description : `str`
                    The board's description.
                groups : `list[moncli.entities.Group]`
                    The board's visible groups.
                id : `str`
                    The unique identifier of the board.
                items : `list[moncli.entities.Item]`
                    The board's items (rows).
                name : `str`
                    The board's name.
                owner : `moncli.entities.user.User`
                    The owner of the board.
                permissions : `str`
                    The board's permissions.
                pos : `str`
                    The board's position.
                state : `str`
                    The board's state (all / active / archived / deleted).
                subscribers : `list[moncli.entities.User]`
                    The board's subscribers.
                tags : `list[moncli.entities.Tag]`
                    The board's specific tags.
                top_group : `moncli.entities.Group`
                    The top group at this board.
                updated_at : `str`
                    The last time the board was updated at (ISO8601 DateTime).
                updates : `list[moncli.entities.Update]`
                    The board's updates.
                views : `list[moncli.entities.BoardView]`
                    The board's views.
                workspace : `moncli.entities.Workspace`
                    The workspace that contains this board (null for main workspace).
                workspace_id : `str`
                    The board's workspace unique identifier (null for main workspace).
        """
        
        try:
            board_data = api.get_boards(
                *args,
                api_key=self.__creds.api_key_v2, 
                ids=[int(id)],
                limit=1)[0]
        except IndexError:
            raise BoardNotFound('id', id)
        return en.Board(creds=self.__creds, **board_data)


    def get_board_by_name(self, name: str, *args):
        """Get a board by name.

            Parameters

                name : `str`
                    The name of the board to retrieve.
                args : `tuple`
                    The list of board return fields.

            Returns

                board : `moncli.entities.Board`
                    The board retrieved by name.

            Return Fields

                activity_logs : `list[moncli.entities.ActivityLog]`
                    The board log events.
                board_folder_id : `int`
                    The board's folder unique identifier.
                board_kind : `str`
                    The board's kind (public / private / share).
                columns : `list[moncli.entities.Column]`
                    The board's visible columns.
                communication : `str`
                    Get the board communication value - typically meeting ID.
                description : `str`
                    The board's description.
                groups : `list[moncli.entities.Group]`
                    The board's visible groups.
                id : `str`
                    The unique identifier of the board.
                items : `list[moncli.entities.Item]`
                    The board's items (rows).
                name : `str`
                    The board's name.
                owner : `moncli.entities.user.User`
                    The owner of the board.
                permissions : `str`
                    The board's permissions.
                pos : `str`
                    The board's position.
                state : `str`
                    The board's state (all / active / archived / deleted).
                subscribers : `list[moncli.entities.User]`
                    The board's subscribers.
                tags : `list[moncli.entities.Tag]`
                    The board's specific tags.
                top_group : `moncli.entities.Group`
                    The top group at this board.
                updated_at : `str`
                    The last time the board was updated at (ISO8601 DateTime).
                updates : `list[moncli.entities.Update]`
                    The board's updates.
                views : `list[moncli.entities.BoardView]`
                    The board's views.
                workspace : `moncli.entities.Workspace`
                    The workspace that contains this board (null for main workspace).
                workspace_id : `str`
                    The board's workspace unique identifier (null for main workspace).
        """
        
        # Hard configure the pagination rate.
        page = 1
        page_limit = 500
        record_count = 500

        while record_count >= page_limit:
            boards_data = api.get_boards(
                'id', 'name',
                api_key=self.__creds.api_key_v2, 
                limit=page_limit,
                page=page)
            
            try:
                target_board = [board for board in boards_data if board['name'].lower() == name.lower()][0]
                return self.get_board_by_id(target_board['id'], *args)
            except IndexError:
                page += 1
                record_count = len(boards_data)
                continue
        raise BoardNotFound('name', name)   


    def archive_board(self, board_id: str, *args):
        """Archive a board.

            Parameters

                board_id : `str`
                    The board's unique identifier.
                args : `tuple`
                    The list of board return fields.
            
            Returns

                board : `moncli.entities.Board`
                    The archived board.

            Return Fields

                activity_logs : `list[moncli.entities.ActivityLog]`
                    The board log events.
                board_folder_id : `int`
                    The board's folder unique identifier.
                board_kind : `str`
                    The board's kind (public / private / share).
                columns : `list[moncli.entities.Column]`
                    The board's visible columns.
                communication : `str`
                    Get the board communication value - typically meeting ID.
                description : `str`
                    The board's description.
                groups : `list[moncli.entities.Group]`
                    The board's visible groups.
                id : `str`
                    The unique identifier of the board.
                items : `list[moncli.entities.Item]`
                    The board's items (rows).
                name : `str`
                    The board's name.
                owner : `moncli.entities.user.User`
                    The owner of the board.
                permissions : `str`
                    The board's permissions.
                pos : `str`
                    The board's position.
                state : `str`
                    The board's state (all / active / archived / deleted).
                subscribers : `list[moncli.entities.User]`
                    The board's subscribers.
                tags : `list[moncli.entities.Tag]`
                    The board's specific tags.
                top_group : `moncli.entities.Group`
                    The top group at this board.
                updated_at : `str`
                    The last time the board was updated at (ISO8601 DateTime).
                updates : `list[moncli.entities.Update]`
                    The board's updates.
                views : `list[moncli.entities.BoardView]`
                    The board's views.
                workspace : `moncli.entities.Workspace`
                    The workspace that contains this board (null for main workspace).
                workspace_id : `str`
                    The board's workspace unique identifier (null for main workspace).
        """

        board_data = api.archive_board(
            board_id,
            *args, 
            api_key=self.__creds.api_key_v2)
        return en.Board(creds=self.__creds, **board_data)


    def get_assets(self, ids: list, *args):
        """Get a collection of assets by IDs.

            Parameters

                ids : `list[int/str]`
                    Ids of the assets/files you want to get.
                    Example:
                    >>> api.get_assets(ids=['12345678'])
                args : `tuple`
                    The list asset return fields.

            Returns

                assets : `list[moncli.entities.asset.Asset]`
                    A list of file assets uploaded to the account.

            Return Fields

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
                uploaded_by : `moncli.entities.User`
                    The user who uploaded the file
                url : `str`
                    The user who uploaded the file
                url_thumbnail : `str`
                    Url to view the asset in thumbnail mode. Only available for images.
        """
        
        if not ids:
            raise AssetIdsRequired()

        assets_data = api.get_assets(
            ids,
            *args,
            api_key=self.__creds.api_key_v2)
        return [en.asset.Asset(**data) for data in assets_data]


    def get_items(self, get_column_values = None, *args, **kwargs):
        """Get a collection of items.

            Parameters

                args : `tuple`
                    The list of item return fields.
                get_column_values: `bool`
                    Flag used to include column values with the returned items.
                kwargs : `dict`
                    Optional keyword arguments for querying items.

            Returns

                items : `list[moncli.entities.Item]`
                    The collection of items.

            Return Fields

                assets : `list[moncli.entities.set.Asset]`
                    The item's assets/files.
                board : `moncli.entities.Board`
                    The board that contains this item.
                column_values : `list[moncli.entities.ColumnValue]`
                    The item's column values.
                created_at : `str`
                    The item's create date.
                creator : `moncli.entities.User`
                    The item's creator.
                creator_id : `str`
                    The item's unique identifier.
                group : `moncli.entities.Group`
                    The group that contains this item.
                id : `str`
                    The item's unique identifier.
                name : `str`
                    The item's name.
                state : `str`
                    The board's state (all / active / archived / deleted)
                subscriber : `moncli.entities.User`
                    The pulse's subscribers.
                updated_at : `str`
                    The item's last update date.
                updates : `moncli.entities.Update`
                    The item's updates.

            Optional Arguments

                limit : `int`
                    Number of items to get; the default is 25.
                page : `int`
                    Page number to get, starting at 1.
                ids : `list[str]`
                    A list of items unique identifiers.
                newest_first : `bool`
                    Get the recently created items at the top of the list.
        """

        if get_column_values:
            args = list(args)
            for arg in ['id', 'name', 'column_values.[*]', 'board.id', 'board.columns.[*]']:
                if arg not in args:
                    args.append(arg)

        if kwargs.__contains__('ids'):
            kwargs['ids'] = [int(id) for id in kwargs['ids']]

        items_data = api.get_items(
            *args,
            api_key=self.__creds.api_key_v2, 
            **kwargs)
        return [en.Item(creds=self.__creds, **item_data) for item_data in items_data] 
        

    def get_updates(self, *args, **kwargs):
        """Get a collection of updates.

            Parameters

                args : `tuple`
                    The list of update return fields.
                kwargs : `dict`
                    The optional keyword arguments for querying updates.

            Returns

                updates : `list[moncli.entities.Update]`
                    A collection of updates.

            Return Fields

                assets : `list[moncli.entities.asset.Asset]`
                    The update's assets/files.
                body: `str`
                    The update's html formatted body.
                created_at: `str`
                    The update's creation date.
                creator : `moncli.entities.user.User`
                    The update's creator
                creator_id : `str`
                    The unique identifier of the update creator.
                id : `str`
                    The update's unique identifier.
                item_id : `str`
                    The update's item ID.
                replies : `list[moncli.entities.reply.Reply]
                    The update's replies.
                text_body : `str`
                    The update's text body.
                updated_at : `str`
                    The update's last edit date.

            Optional Arguments

                limit : `int`
                    Number of updates to get; the default is 25.
                page : `int`
                    Page number to get, starting at 1.
        """

        updates_data = api.get_updates(
            *args,
            api_key=self.__creds.api_key_v2, 
            **kwargs)
        return [en.Update(creds=self.__creds, **update_data) for update_data in updates_data]


    def delete_update(self, id: str, *args):
        """Delete an update.

            Parameters

                id : `str`
                    The update's unique identifier.
                args : `tuple`
                    The list of update fields to return.

            Returns

                update : `moncli.entities.Update`
                    The deleted update.

            Return Fields

                assets : `list[moncli.entities.Asset]`
                    The update's assets/files.
                body: `str`
                    The update's html formatted body.
                created_at: `str`
                    The update's creation date.
                creator : `moncli.entities.User`
                    The update's creator
                creator_id : `str`
                    The unique identifier of the update creator.
                id : `str`
                    The update's unique identifier.
                item_id : `str`
                    The update's item ID.
                replies : `list[moncli.entities.Reply]`
                    The update's replies.
                text_body : `str`
                    The update's text body.
                updated_at : `str`
                    The update's last edit date.
        """
        
        update_data = api.delete_update(
            id, 
            *args, 
            api_key=self.__creds.api_key_v2)
        return en.Update(creds=self.__creds, **update_data)


    def clear_item_updates(self, item_id: str, *args):
        """Clear an item's updates.

            Parameters

                item_id : `str`
                    The item's unique identifier.
                args : `tuple`
                    The list of optional fields to return.

            Returns

                update : `moncli.entities.Item`
                    The updated item.

            Return Fields

                assets : `list[moncli.entities.asset.Asset]`
                    The item's assets/files.
                board : `moncli.entities.board.Board`
                    The board that contains this item.
                column_values : `list[moncli.entities.column_value.ColumnValue]`
                    The item's column values.
                created_at : `str`
                    The item's create date.
                creator : `moncli.entities.user.User`
                    The item's creator.
                creator_id : `str`
                    The item's unique identifier.
                group : `moncli.entities.group.Group`
                    The group that contains this item.
                id : `str`
                    The item's unique identifier.
                name : `str`
                    The item's name.
                state : `str`
                    The board's state (all / active / archived / deleted)
                subscriber : `moncli.entities.user.User`
                    The pulse's subscribers.
                updated_at : `str`
                    The item's last update date.
                updates : `moncli.entities.update.Update`
                    The item's updates.
        """
        
        item_data = api.clear_item_updates(
            item_id,
            *args,
            api_key=self.__creds.api_key_v2)
        return en.Item(creds=self.__creds, **item_data)


    def create_notification(self, text: str, user_id: str, target_id: str, target_type: NotificationTargetType, *args, **kwargs):
        """Create a new notification.

            Parameters

                text : `str`
                    The notification text.
                user_id : `str`
                    The user's unique identifier.
                target_id : `str`
                    The target's unique identifier.
                target_type : `moncli.enums.NotificationTargetType`
                    The target's type (Project / Post)
                args : `tuple`
                    The list of notification return fields.
                kwargs : `dict`
                    The optional keyword arguments for creating notifications.

            Returns

                notification : `moncli.entities.Notification`
                    A new notification.

            Return Fields

                id : `str`
                    The notification's unique identifier.
                text : `str`
                    The notification text.

            Optional Arguments

                payload : `json`
                    The notification payload.
        """

        notification_data = api.create_notification(
            text, 
            user_id, 
            target_id,
            target_type,
            *args,
            api_key=self.__creds.api_key_v2, 
            **kwargs)
        return en.Notification(notification_data)
    

    def create_or_get_tag(self, tag_name: str, *args, **kwargs):
        """Create a new tag or get it if it already exists.

            Parameters

                tag_name : `str`
                    The new tag's name.
                args : `tuple`
                    The list of tag return fields.
                kwargs : `dict`
                    Optional keyword arguments for creating/getting a tag.

            Returns

                tag : `moncli.entities.Tag`
                    The created or retrieved tag.

            Return Fields

                color : `str`
                    The tag's color.
                id : `str`
                    The tag's unique identifier.
                name : `str`
                    The tag's name.

            Optional Arguments

                board_id : `str`
                    The private board id to create the tag at (not needed for public boards).
        """

        tag_data = api.create_or_get_tag(
            tag_name,
            *args,
            api_key=self.__creds.api_key_v2, 
            **kwargs)
        return en.Tag(tag_data)


    def get_tags(self, *args, **kwargs):
        """Get a collection of tags.

            Parameters

                args : `tuple`
                    The list of tag return fields.
                kwargs : `dict`
                    Optional keyword arguments for querying tags.

            Returns

                tags : `list[moncli.entities.Tag]`
                    A collection of tags.

            Return Fields

                color : `str`
                    The tag's color.
                id : `str`
                    The tag's unique identifier.
                name : `str`
                    The tag's name.

            Optional Arguments

                ids : `list[str]`
                    The list of tags unique identifiers.
        """
        
        tags_data = api.get_tags(
            *args,
            api_key=self.__creds.api_key_v2,
            **kwargs)
        return [en.Tag(tag_data) for tag_data in tags_data]
    

    def get_users(self, *args, **kwargs):
        """Get a collection of users.

            Parameters

                args : `tuple`
                    The list of user return fields.
                kwargs : `dict`
                    Optional keyword arguments for querying users.

            Returns

                users : `list[moncli.entities.User]`
                    A collection of users.

            Return Fields

                account : `moncli.entities.Account`
                    The user's account.
                birthday : `str`
                    The user's birthday.
                country_code : `str`
                    The user's country code.
                created_at : `str`
                    The user's creation date.
                email : `str`
                    The user's email.
                enabled : `bool`
                    Is the user enabled or not.
                id : `str`
                    The user's unique identifier.
                is_admin: `bool`
                    Is the user a admin or not.
                is_guest : `bool`
                    Is the user a guest or not.
                is_pending : `bool`
                    Is the user a pending user.
                is_verified: `bool`
                    Is the user is verified
                is_view_only : `bool`
                    Is the user a view only user or not.
                join_date : `str`
                    The date the user joined the account.
                location : `str`
                    The user' location.
                mobile_phone : `str`
                    The user's mobile phone number.
                name : `str`
                    The user's name.
                phone : `str`
                    The user's phone number.
                photo_original : `str`
                    The user's photo in the original size.
                photo_small : `str`
                    The user's photo in small size (150x150).
                photo_thumb : `str`
                    The user's photo in thumbnail size (100x100).
                photo_thumb_small : `str`
                    The user's photo in small thumbnail size (50x50).
                photo_tiny : `str`
                    The user's photo in tiny size (30x30).
                teams : `list[moncli.entities.Team]`
                    The teams the user is a member in.
                time_zone_identifier : `str`
                    The user's time zone identifier.
                title : `str`
                    The user's title.
                url : `str`
                    The user's profile url.
                utc_hours_diff : `int`
                    The user's UTC hours difference.

            Optional Arguments

                ids : `list[str]`
                    A list of users unique identifiers.
                kind : `moncli.entities.UserKind`
                    The kind to search users by (all / non_guests / guests / non_pending).
                newest_first : `bool`
                    Get the recently created users at the top of the list.
                limit : `int`
                    Number of users to get.
        """

        users_data = api.get_users(
            *args,
            api_key=self.__creds.api_key_v2, 
            **kwargs)
        return [en.User(creds=self.__creds, **user_data) for user_data in users_data]
    

    def get_teams(self, *args, **kwargs):
        """Get a collection of teams.

            Parameters

                args : `tuple`
                    The list of team return fields.
                kwargs : `dict`
                    Optional keyword arguments for querying teams.
            
            Returns

                teams : `list[moncli.entities.Team]`
                    A collection of teams.

            Return Fields

                id : `int`
                    The team's unique identifier.
                name : `str`
                    The team's name.
                picture_url : `str`
                    The team's picture url.
                users : `moncli.entities.user.User`
                    The users in the team.

            
            Optional Arguments

                ids : `list[str]`
                    A list of teams unique identifiers.
        """

        teams_data = api.get_teams(
            *args,
            api_key=self.__creds.api_key_v2,
            **kwargs)
        return [en.Team(creds=self.__creds, **team_data) for team_data in teams_data]
    

    def get_me(self, *args):
        """Get the connected user's information.

            Parameters

                args : `tuple`
                    The list of user return fields.
            
            Returns

                user : `moncli.entities.User`
                    The connected user.

            Return Fields

                account : `moncli.entities.Account`
                    The user's account.
                birthday : `str`
                    The user's birthday.
                country_code : `str`
                    The user's country code.
                created_at : `str`
                    The user's creation date.
                email : `str`
                    The user's email.
                enabled : `bool`
                    Is the user enabled or not.
                id : `str`
                    The user's unique identifier.
                is_admin: `bool`
                    Is the user a admin or not.
                is_guest : `bool`
                    Is the user a guest or not.
                is_pending : `bool`
                    Is the user a pending user.
                is_verified: `bool`
                    Is the user is verified
                is_view_only : `bool`
                    Is the user a view only user or not.
                join_date : `str`
                    The date the user joined the account.
                location : `str`
                    The user' location.
                mobile_phone : `str`
                    The user's mobile phone number.
                name : `str`
                    The user's name.
                phone : `str`
                    The user's phone number.
                photo_original : `str`
                    The user's photo in the original size.
                photo_small : `str`
                    The user's photo in small size (150x150).
                photo_thumb : `str`
                    The user's photo in thumbnail size (100x100).
                photo_thumb_small : `str`
                    The user's photo in small thumbnail size (50x50).
                photo_tiny : `str`
                    The user's photo in tiny size (30x30).
                teams : `list[moncli.entities.Team]`
                    The teams the user is a member in.
                time_zone_identifier : `str`
                    The user's time zone identifier.
                title : `str`
                    The user's title.
                url : `str`
                    The user's profile url.
                utc_hours_diff : `int`
                    The user's UTC hours difference.
        """

        user_data = api.get_me(
            *args, 
            api_key=self.__creds.api_key_v2)

        return en.User(creds=self.__creds, **user_data)


    def get_account(self, *args):
        """Get the connected user's account.

            Parameters

                args : `tuple`
                    The list of account return fields.
            
            Returns

                account : `moncli.entities.Account`
                    The connected user's account.

            Return Fields

                first_day_of_the_week : `str`
                    The first day of the week for the account (sunday / monday).
                id : `int`
                    The account's unique identifier.
                logo : `str`
                    The account's logo.
                name : `str`
                    The account's name.
                plan : `moncli.entities.Plan`
                    The account's payment plan.
                show_timeline_weekends : `bool`
                    Show weekends in timeline.
                slug : `str`
                    The account's slug.
        """

        account_data = api.get_account(
            *args,
            api_key=self.__creds.api_key_v2)

        return en.Account(creds=self.__creds, **account_data)


    def create_workspace(self, name: str, kind: WorkspaceKind, *args, **kwargs):
        """Creates a new workspace

            Parameters

                name : `str`
                    The workspace's name.
                kind : `moncli.enums.WorkspaceKind`
                    The workspace's kind (open / closed)
                args : `tuple`
                    The list of workspace return fields.
                kwargs : `dict`
                    Optional keyword arguments listed below.
            
            Returns

                workspace : `moncli.entities.Workspace`
                    The newly created workspace

            Return Fields

                id : `str`
                    The workspace's unique identifier
                name : `str`
                    The workspace's name
                kind : `str`
                    The workspace's kind (open / closed)
                description : `str`
                    The workspace's description

            Optional Arguments

                description : `str`
                    The workspace's description.
        """
        
        workspace_data = api.create_workspace(
            name, 
            kind,
            *args,
            api_key=self.__creds.api_key_v2,
            **kwargs)

        return en.Workspace(workspace_data)
    
    def add_users_to_workspace(self, workspace_id: str, user_ids: list, kind: WorkspaceSubscriberKind, *args, **kwargs):
        """Allows you to add users to a workspace. You can define if users will be added as regular subscribers or as owners of the workspace.

            Parameters 

                workspace_id: int
                     The workspace's unique identifier
                user_ids: `list[str]`
                        User IDs to subscribe to the workspace
                kind: WorkspaceSUbscriberKind
                    Kind of subscribers added (subscriber/owner)
                args: tuple
                    The collection of workspace return fields.
                kwargs : `dict`
                    Optional keyword arguments listed below.
            
            Return Fields
            
                account : `moncli.entities.Account`
                    The user's account.
                birthday : `str`
                    The user's birthday.
                country_code : `str`
                    The user's country code.
                created_at : `str`
                    The user's creation date.
                email : `str`
                    The user's email.
                enabled : `bool`
                    Is the user enabled or not.
                id : `str`
                    The user's unique identifier.
                is_admin: `bool`
                    Is the user a admin or not.
                is_guest : `bool`
                    Is the user a guest or not.
                is_pending : `bool`
                    Is the user a pending user.
                is_verified: `bool`
                    Is the user is verified
                is_view_only : `bool`
                    Is the user a view only user or not.
                join_date : `str`
                    The date the user joined the account.
                location : `str`
                    The user' location.
                mobile_phone : `str`
                    The user's mobile phone number.
                name : `str`
                    The user's name.
                phone : `str`
                    The user's phone number.
                photo_original : `str`
                    The user's photo in the original size.
                photo_small : `str`
                    The user's photo in small size (150x150).
                photo_thumb : `str`
                    The user's photo in thumbnail size (100x100).
                photo_thumb_small : `str`
                    The user's photo in small thumbnail size (50x50).
                photo_tiny : `str`
                    The user's photo in tiny size (30x30).
                teams : `list[moncli.entities.Team]`
                    The teams the user is a member in.
                time_zone_identifier : `str`
                    The user's time zone identifier.
                title : `str`
                    The user's title.
                url : `str`
                    The user's profile url.
                utc_hours_diff : `int`
                    The user's UTC hours difference.
         """
         
        users_data = api.add_users_to_workspace(
            workspace_id,
            user_ids, 
            kind,
            *args,
            api_key=self.__creds.api_key_v2,
            **kwargs)

        return [en.User(creds=self.__creds, **data) for data in users_data]


    def delete_users_from_workspace(self, workspace_id: str, user_ids: list(), *args: tuple, **kwargs: dict ):
        """Allows you to delete users to a workspace.

            Parameters 

                workspace_id: int
                    The workspace's unique identifier
                user_ids: `list[str]`
                        User IDs to subscribe to the workspace
                *args: tuple
                    The collection of workspace return fields.
            
            Return Fields
        
                account : `moncli.entities.Account`
                    The user's account.
                birthday : `str`
                    The user's birthday.
                country_code : `str`
                    The user's country code.
                created_at : `str`
                    The user's creation date.
                email : `str`
                    The user's email.
                enabled : `bool`
                    Is the user enabled or not.
                id : `str`
                    The user's unique identifier.
                is_admin: `bool`
                    Is the user a admin or not.
                is_guest : `bool`
                    Is the user a guest or not.
                is_pending : `bool`
                    Is the user a pending user.
                is_verified: `bool`
                    Is the user is verified
                is_view_only : `bool`
                    Is the user a view only user or not.
                join_date : `str`
                    The date the user joined the account.
                location : `str`
                    The user' location.
                mobile_phone : `str`
                    The user's mobile phone number.
                name : `str`
                    The user's name.
                phone : `str`
                    The user's phone number.
                photo_original : `str`
                    The user's photo in the original size.
                photo_small : `str`
                    The user's photo in small size (150x150).
                photo_thumb : `str`
                    The user's photo in thumbnail size (100x100).
                photo_thumb_small : `str`
                    The user's photo in small thumbnail size (50x50).
                photo_tiny : `str`
                    The user's photo in tiny size (30x30).
                teams : `list[moncli.entities.Team]`
                    The teams the user is a member in.
                time_zone_identifier : `str`
                    The user's time zone identifier.
                title : `str`
                    The user's title.
                url : `str`
                    The user's profile url.
                utc_hours_diff : `int`
                    The user's UTC hours difference.
        """
        
        users_data = api.delete_users_from_workspace(
            workspace_id,
            user_ids,
            *args,
            api_key=self.__creds.api_key_v2,
            **kwargs)

        return [en.User(creds=self.__creds, **data) for data in users_data]


    def add_teams_to_workspace(self, workspace_id: str, team_ids: list(), *args, **kwargs ):
        """Allows you to add teams to a workspace.

            Parameters

                workspace_id: str
                    The workspace's unique identifier.
                team_ids: list()
                    Team ids to subscribe to the workspace.
            
            Returns

                teams: `list[moncli.entities.user.Team]`
                    List of teams deleted from the workspace
            
            Return Fields

                id : `int`
                    The team's unique identifier.
                name : `str`
                    The team's name.
                picture_url : `str`
                    The team's picture url.
                users : `moncli.entities.user.User`
                    The users in the team.
                name : `str`
                    The team's name.
                picture_url : `str`
                    The team's picture url.
                users : `moncli.entities.user.User`
                    The users in the team.

            Optional Arguments

                api_key : `str`
                    The monday.com v2 API user key.
        """
        
        teams_data = api.add_teams_to_workspace(
            workspace_id,
            team_ids,
            *args,
            api_key=self.__creds.api_key_v2,
            **kwargs)

        return [en.Team(creds=self.__creds, **data) for data in teams_data]


    def delete_teams_from_workspace(self, workspace_id: str, team_ids: list(), *args, **kwargs ):
        """Allows you to delete teams from a workspace.

            Parameters

                workspace_id: str
                    The workspace's unique identifier.
                team_ids: list()
                    Team ids to subscribe to the workspace.
            
            Returns

                teams: `list[moncli.entities.user.Team]`
                    List of teams deleted from the workspace
            
            Return Fields

                id : `int`
                    The team's unique identifier.
                name : `str`
                    The team's name.
                picture_url : `str`
                    The team's picture url.
                users : `moncli.entities.user.User`
                    The users in the team.
                name : `str`
                    The team's name.
                picture_url : `str`
                    The team's picture url.
                users : `moncli.entities.user.User`
                    The users in the team.

            Optional Arguments

                api_key : `str`
                    The monday.com v2 API user key.
        """
        
        teams_data = api.delete_teams_from_workspace(
            workspace_id,
            team_ids,
            *args,
            api_key=self.__creds.api_key_v2,
            **kwargs)

        return [en.Team(creds=self.__creds, **data) for data in teams_data]


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

