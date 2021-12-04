from typing import List, Dict, Any

from ..enums import BoardKind, ColumnType, NotificationTargetType, WebhookEventType, WorkspaceKind, WorkspaceSubscriberKind
from . import graphql as gql
from .constants import *
from .requests import execute_query, upload_file


def create_board(board_name: str, board_kind: BoardKind, *args, **kwargs):
    """Create a new board.

        Parameters

            board_name : `str`
                The board's name.
            board_kind : `moncli.enums.BoardKind`
                The board's kind (public / private / share)
            args : `tuple`
                The list of board return fields.
            kwargs : `dict`
                Optional keyword arguments for creating boards.

        Returns

            board_data : `dict`
                A monday.com board in dictionary form.

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

            api_key : `str`
                The monday.com v2 API user key.
            workspace_id : `int`
                Optional workspace id.
            template_id : `int`
                Optional board template id.
    """

    kwargs['board_name'] = gql.StringValue(board_name)
    kwargs['board_kind'] = gql.EnumValue(board_kind)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=CREATE_BOARD, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def get_boards(*args, **kwargs) -> List[Dict[str, Any]]:
    """Retrieves a list of boards.

        Parameters
        
            args : `tuple`
                The list of board return fields.
            kwargs : `dict`
                Optional keyword arguments for querying boards.

        Returns

            data : `dict`
                A monday.com board in dictionary form.

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
            
            api_key : `str`
                The monday.com v2 API user key.
            limit : `int`
                Number of boards to get; the default is 25.
            page : `int`
                Page number to get, starting at 1.
            ids : `list[str]`
                A list of boards unique identifiers.
            board_kind : `moncli.enumns.BoardKind`
                The board's kind (public / private /share).
            state : `moncli.enums.State`
                The state of the board (all / active / archived / deleted),; the default is active.
            order_by : `moncli.enums.BoardsOrderBy`
                The order in which to retrieve your boards (created_at / used_at).       
    """
    
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=BOARDS, operation_type=gql.OperationType.QUERY, fields=args, arguments=kwargs)  


def archive_board(board_id: str, *args, **kwargs):
    """Archives a board.

        Parameters
        

            board_id : `str`
                The board's unique identifier.
            args : `tuple`
                The list of board return fields.
            kwargs : `dict`
                Optional keyword arguments for archiving boards.

        Returns
            
            data : `dict`
                A monday.com board in dictionary form.

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

            api_key : `str`
                The monday.com v2 API user key.
    """

    kwargs['board_id'] = gql.IntValue(board_id)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=ARCHIVE_BOARD, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def add_subscribers_to_board(board_id: str, user_ids: list, *args, **kwargs):
    """Add subscribers to a board.

        Parameters

            board_id : `str`
                The board's unique identifier.
            user_ids : `list[str]`
                User ids to subscribe to a board.
            args : `tuple`
                The list of user return fields.
            kwargs : `dict`
                Optional keyword arguments for adding board subscribers.

        Returns

            data : `dict`
                A monday.com user in dictionary form.
        
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
            is_guest : `bool`
                Is the user a guest or not.
            is_pending : `bool`
                Is the user a pending user.
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

            api_key : `str`
                The monday.com v2 API user key.
            kind : `moncli.enums.SubscriberKind`
                Subscribers kind (subscriber / owner).
    """

    kwargs['board_id'] = gql.IntValue(board_id)
    kwargs['user_ids'] = gql.ListValue([int(id) for id in user_ids])
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=ADD_SUBSCRIBERS_TO_BOARD, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def delete_subscribers_from_board(board_id: str, user_ids: list, *args, **kwargs):
    """Remove subscribers from the board.

        Parameters

            board_id : `str`
                The board's unique identifier.
            user_ids : `list[str]`
                User ids to unsubscribe from board.
            args : `tuple`
                The list of user return fields.
            kwargs : `dict`
                Additional keyword arguments for deleting subscribers.

        Returns

            data : `dict`
                A monday.com user in dictionary form.
        
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
            is_guest : `bool`
                Is the user a guest or not.
            is_pending : `bool`
                Is the user a pending user.
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

            api_key : `str`
                The monday.com v2 API user key.
    """

    kwargs['board_id'] = gql.IntValue(board_id),
    kwargs['user_ids'] = gql.ListValue([int(id) for id in user_ids])
    
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=DELETE_SUBSCRIBERS_FROM_BOARD, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)

    
def create_column(board_id: str, title: str, column_type: ColumnType, *args, **kwargs):
    """Create a new column in board.

        Parameters
        
            board_id : `str`
                The board's unique identifier.
            title : `str`
                The new column's title.
            args : `tuple`
                The list of column return fields.
            kwargs : `dict`
                Optional keyword arguments for creating columns.

        Returns
            
            data : `dict`
                A monday.com column in dictionary form.

        Return Fields
            
            archived : `bool`
                Is the column archived or not.
            id : `str`
                The column's unique identifier.
            pos : `str`
                The column's position in the board.
            settings_str : `str`
                The column's settings in a string form.
            title : `str`
                The column's title.
            type : `str`
                The column's type.
            width : `int`
                The column's width.

        Optional Arguments
            
            api_key : `str`
                The monday.com v2 API user key.
            column_type : `moncli.enumns.ColumnType`
                The type of column to create.
            defaults : `json`
                The new column's defaults.
    """
    
    kwargs['board_id'] = gql.IntValue(board_id)
    kwargs['title'] = gql.StringValue(title)
    kwargs['column_type'] = gql.EnumValue(column_type)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=CREATE_COLUMN, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def change_column_title(title: str, column_id: str, board_id: str, *args, **kwargs):
    """Change an item's column title.

        Parameters
        
            title : `str`
                The new title of the column.
            column_id : `str`
                The column's unique identifier.
            board_id : `str`
                The board's unique identifier.
            args : `tuple`
                The list of item return fields.
            kwargs : `dict`
                Optional arguments for changing a column value.

        Returns
            
            data : `dict`
                A monday.com column in item form.

        Return Fields
        
            archived : `bool`
                Is the column archived or not.
            id : `str`
                The column's unique identifier.
            pos : `str`
                The column's position in the board. 
            settings_str : `str`
                The column's settings in a string form.
            settings : `moncli.entities.Settings`
                The settings in entity form (status / dropdown)
            title : `str`
                The column's title.
            type : `str`
                The column's type.
            width : `int`
                The column's width.
            
        Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    kwargs['column_id'] = gql.StringValue(column_id)
    kwargs['board_id'] = gql.IntValue(board_id)
    kwargs['title'] = gql.StringValue(title)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=CHANGE_COLUMN_TITLE, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def change_column_value(item_id: str, column_id: str, board_id: str, value: str, *args, **kwargs):
    """Change an item's column value.

        Parameters
        
            item_id : `str`
                The item's unique identifier.
            column_id : `str`
                The column's unique identifier.
            board_id : `str`
                The board's unique identifier.
            value : `json`
                The new value of the column.
            args : `tuple`
                The list of item return fields.
            kwargs : `dict`
                Optional arguments for changing a column value.

        Returns
            
            data : `dict`
                A monday.com column in item form.

        Return Fields
        
            assets : `list[moncli.entities.Asset]`
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

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    kwargs['item_id'] = gql.IntValue(item_id)
    kwargs['column_id'] = gql.StringValue(column_id)
    kwargs['board_id'] = gql.IntValue(board_id)
    kwargs['value'] = gql.JsonValue(value)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=CHANGE_COLUMN_VALUE, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)

def change_simple_column_value(item_id: str, board_id: str, column_id: str, value: str, *args, **kwargs):
    """Changes the column valuesvalues using simple values

        Parameters
        
            item_id : str
                The item's identifier.
            column_id : str
                The column identifier on your board.
            board_id : str
                The board identifier.
            value : str
                The new simple value of the column.
            *args : tuple
                The collection of item return fields.

        Returns
            
            data : `dict`
                A monday.com column in item form.

        Return Fields
        
            assets : `list[moncli.entities.Asset]`
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

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    kwargs['item_id'] = gql.IntValue(item_id)
    kwargs['board_id'] = gql.IntValue(board_id)
    kwargs['column_id'] = gql.StringValue(column_id)
    kwargs['value']=gql.StringValue(value)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=CHANGE_SIMPLE_COLUMN_VALUE, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def change_multiple_column_value(item_id: str, board_id: str, column_values: dict, *args, **kwargs):
    """Changes the column values of a specific item.

        Parameters
        
            item_id : `str`
                The item's unique identifier.
            board_id : `str`
                The board's unique identifier.
            column_values : `json`
                The column values updates.
            args : `tuple`
                The list of item return fields.
            kwargs : `dict`
                Optional arguments for changing a column value.

        Returns
            
            data : `dict`
                A monday.com column in item form.

        Return Fields
        
            assets : `list[moncli.entities.Asset]`
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

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    kwargs['item_id'] = gql.IntValue(item_id)
    kwargs['board_id'] = gql.IntValue(board_id)
    kwargs['column_values'] = gql.JsonValue(column_values)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=CHANGE_MULTIPLE_COLUMN_VALUES, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def get_assets(ids: list, *args, **kwargs):
    """Get a collection of assets by ids.

        Parameters

            ids : `list[str]`
                Ids of the assets/files you want to get.
            args : `tuple`
                The list of asset return fields.
            kwargs : `dict`
                Optional arguments for querying assets.

        Returns
            
            data : `dict`
                A monday.com asset in item form.

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
            uploaded_by : `moncli.entities.user.User`
                The user who uploaded the file
            url : `str`
                The user who uploaded the file
            url_thumbnail : `str`
                Url to view the asset in thumbnail mode. Only available for images.  

         Optional Arguments

            api_key : `str`
                The monday.com v2 API user key. 
    """
    
    ids = [gql.IntValue(id).value for id in ids]
    kwargs['ids'] = gql.ListValue(ids)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=ASSETS, operation_type=gql.OperationType.QUERY, *args, fields=args, arguments=kwargs)


def duplicate_group(board_id: str, group_id: str, *args, **kwargs):
    """Duplicate a group.

        Parameters
        
            board_ id : `str`
                The board's unique identifier.
            group_id : `str`
                The group's unique identifier.
            args : `tuple`
                The list of asset return fields.
            kwargs : `dict`
                Optional arguments for querying assets.

        Returns
            
            data : `dict`
                A monday.com group in item form.

        Return Fields
        
            archived : `bool`
                Is the group archived or not.
            color : `str`
                The group's color.
            deleted : `bool`
                Is the group deleted or not.
            id : `str`
                The group's unique identifier.
            items : `list[moncli.entities.Item]`
                The items in the group.
            position : `str`
                The group's position in the board.
            title : `str`
                The group's title.

        
        Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.
            add_to_top : `bool`
                Should the new group be added to the top.
            group_title : `str`
                The group's title.
    """
    
    kwargs['board_id'] = gql.IntValue(board_id)
    kwargs['group_id'] = gql.StringValue(group_id)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=DUPLICATE_GROUP, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def create_group(board_id: str, group_name: str, *args, **kwargs):
    """Creates a new group in a specific board.

        Parameters
        
            board_id : `str`
                The board's unique identifier.
            group_name : `str`
                The name of the new group.
            args : `tuple`
                The list of group return fields.
            kwargs : `dict`
                Optional arguments for querying assets.

        Returns
            
            data : `dict`
                A monday.com group in item form.

        Return Fields
        
            archived : `bool`
                Is the group archived or not.
            color : `str`
                The group's color.
            deleted : `bool`
                Is the group deleted or not.
            id : `str`
                The group's unique identifier.
            items : `list[moncli.entities.Item]`
                The items in the group.
            position : `str`
                The group's position in the board.
            title : `str`
                The group's title.


         Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    kwargs['board_id'] = gql.IntValue(board_id)
    kwargs['group_name'] = gql.StringValue(group_name)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=CREATE_GROUP, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def archive_group(board_id: str, group_id: str, *args, **kwargs):
    """Archives a group in a specific board.

        Parameters

            board_id : `str`
                The board's unique identifier.
            group_id : `str`
                The group's unique identifier.
            args : `tuple`
                The list of group return fields.
            kwargs : `dict`
                Optional arguments for archiving groups.

        Returns
            
            data : `dict`
                A monday.com group in item form.

        Return Fields
        
            archived : `bool`
                Is the group archived or not.
            color : `str`
                The group's color.
            deleted : `bool`
                Is the group deleted or not.
            id : `str`
                The group's unique identifier.
            items : `list[moncli.entities.Item]`
                The items in the group.
            position : `str`
                The group's position in the board.
            title : `str`
                The group's title.
        
         Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    kwargs['board_id'] = gql.IntValue(board_id)
    kwargs['group_id'] = gql.StringValue(group_id)    
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=ARCHIVE_GROUP, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def delete_group(board_id: str, group_id: str, *args, **kwargs):
    """Deletes a group in a specific board.

        Parameters

            board_id : `str`
                The board's unique identifier.
            group_id : `str`
                The group's unique identifier.
            args : `tuple`
                The list of group return fields.
            kwargs : `dict`
                Optional arguments for deleting groups.

        Returns
            
            data : `dict`
                A monday.com group in item form.

        Return Fields
        
            archived : `bool`
                Is the group archived or not.
            color : `str`
                The group's color.
            deleted : `bool`
                Is the group deleted or not.
            id : `str`
                The group's unique identifier.
            items : `list[moncli.entities.Item]`
                The items in the group.
            position : `str`
                The group's position in the board.
            title : `str`
                The group's title.
        
         Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    kwargs['board_id'] = gql.IntValue(board_id)
    kwargs['group_id'] = gql.StringValue(group_id)       
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=DELETE_GROUP, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def create_item(item_name: str, board_id: str, *args, **kwargs):
    """Create a new item.

        Parameters
        
            item_name : `str`
                The new item's name.
            board_id : `str`
                The board's unique identifier.
            args : `tuple`
                The list of item return fields.
            kwargs : `dict`
                Optional arguments for creating items.

        Returns
                    
            data : `dict`
                A monday.com column in item form.

        Return Fields
        
            assets : `list[moncli.entities.Asset]`
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

            api_key : `str`
                The monday.com v2 API user key.        
            group_id : `str`
                The group's unique identifier.
            column_values : `json`
                The column values of the new item.
    """
    
    kwargs['item_name'] = gql.StringValue(item_name)
    kwargs['board_id'] = gql.IntValue(board_id)    
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=CREATE_ITEM, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def create_subitem(parent_item_id: str, item_name: str, *args, **kwargs):
    """Create subitem.

        Parameters
        
            parent_item_id : `str`
                The parent item's unique identifier.
            item_name : `str`
                The new item's name.
            args : `tuple`
                The list of item return fields.
            kwargs : `dict`
                Optional arguments for creating subitems.

        Returns
                    
            data : `dict`
                A monday.com column in item form.

        Return Fields
        
            assets : `list[moncli.entities.Asset]`
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

            api_key : `str`
                The monday.com v2 API user key.
            column_values : `json`
                The column values of the new item.
    """

    kwargs['parent_item_id'] = gql.IntValue(parent_item_id)
    kwargs['item_name'] = gql.StringValue(item_name)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=CREATE_SUBITEM, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def get_items(*args, **kwargs):
    """Get a collection of items.

        Parameters
        
            args : `tuple`
                The list of item return fields.
            kwargs : `dict`
                Optional arguments for querying items.

        Returns
            
            data : `dict`
                A monday.com column in item form.

        Return Fields
        
            assets : `list[moncli.entities.Asset]`
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
        
            api_key : `str`
                The monday.com v2 API user key.
            limit : `int`
                Number of items to get; the default is 25.
            page : `int`
                Page number to get, starting at 1.
            ids : `list[str]`
                A list of items unique identifiers.
            mewest_first : `bool`
                Get the recently created items at the top of the list.
    """
    
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=ITEMS, operation_type=gql.OperationType.QUERY, fields=args, arguments=kwargs)


def get_items_by_column_values(board_id: str, column_id: str, column_value: str, *args, **kwargs):
    """Search items by a value for a single column.

        Parameters
        
            board_id : `str`
                The board's unique identifier.
            column_id : `str`
                The column's unique identifier.
            column_value `str`
                The column value to search items by.
            args : `tuple`
                The list of item return fields.
            kwargs : `dict`
                Optional arguments for querying items by column value.

        Returns
            
            data : `dict`
                A monday.com column in item form.

        Return Fields
        
            assets : `list[moncli.entities.Asset]`
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

            api_key : `str`
                The monday.com v2 API user key.
            limit : `int`
                Number of items to get.
            page : `int`
                Page number to get, starting at 1.
            column_type : `str`
                The column type.
            state : `moncli.enums.State`
                The state of the item (all / active / archived / deleted); the default is active.
    """
    
    kwargs['board_id'] = gql.IntValue(board_id)
    kwargs['column_id'] = gql.StringValue(column_id)
    kwargs['column_value'] = gql.StringValue(column_value)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=ITEMS_BY_COLUMN_VALUES, operation_type=gql.OperationType.QUERY, fields=args, arguments=kwargs)


def get_items_by_multiple_column_values(board_id: str, column_id: str, column_value: list, *args, **kwargs):
    """Search items by multiple values for a single column.

        Parameters
        
            board_id : `str`
                The board's unique identifier.
            column_id : `str`
                The column's unique identifier.
            column_values `list`
                The column value to search items by.
            args : `tuple`
                The list of item return fields.
            kwargs : `dict`
                Optional arguments for querying items by column value.

        Returns
            
            data : `dict`
                A monday.com column in item form.

        Return Fields
        
            assets : `list[moncli.entities.Asset]`
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

            api_key : `str`
                The monday.com v2 API user key.
            limit : `int`
                Number of items to get.
            page : `int`
                Page number to get, starting at 1.
            column_type : `str`
                The column type.
            state : `moncli.enums.State`
                The state of the item (all / active / archived / deleted); the default is active.
    """
    
    kwargs['board_id'] = gql.IntValue(board_id)
    kwargs['column_id'] = gql.StringValue(column_id)
    kwargs['column_values'] = gql.ListValue(column_value)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=ITEMS_BY_MULTIPLE_COLUMN_VALUES, operation_type=gql.OperationType.QUERY, fields=args, arguments=kwargs)


def clear_item_updates(item_id: str, *args, **kwargs):
    """Clear an item's updates.

        Parameters
        
            item_id : `str`
                The item's unique identifier.
            args : `tuple`
                The list of item return fields.
            kwargs : `dict`
                Optional arguments for clearing item updates.

        Returns
            
            data : `dict`
                A monday.com column in item form.

        Return Fields
        
            assets : `list[moncli.entities.Asset]`
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

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    kwargs['item_id'] = gql.IntValue(item_id)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=CLEAR_ITEM_UPDATES, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def move_item_to_group(item_id: str, group_id: str, *args, **kwargs):
    """Move an item to a different group.

        Parameters
        
            item_id : `str`
                The item's unique identifier.
            group_id : `str`
                The group's unique identifier.
            args : `tuple`
                The list of item return fields.
            kwargs : `dict`
                Optional arguments for moving item to group.

        Returns
            
            data : `dict`
                A monday.com column in item form.

        Return Fields
        
            assets : `list[moncli.entities.Asset]`
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

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    kwargs['item_id'] = gql.IntValue(item_id)
    kwargs['group_id'] = gql.StringValue(group_id)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=MOVE_ITEM_TO_GROUP, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def archive_item(item_id: str, *args, **kwargs):
    """Archive an item.

        Parameters
        
            item_id : `str`
                The item's unique identifier.
            args : `tuple`
                The list of item return fields.
            kwargs : `dict`
                Optional arguments for archiving items.

        Returns
            
            data : `dict`
                A monday.com column in item form.

        Return Fields
        
            assets : `list[moncli.entities.Asset]`
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

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    kwargs['item_id'] = gql.IntValue(item_id)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=ARCHIVE_ITEM, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def delete_item(item_id: str, *args, **kwargs):
    """Delete an item.

        Parameters
        
            item_id : `str`
                The item's unique identifier.
            args : `tuple`
                The list of item return fields.
            kwargs : `dict`
                Optional arguments for item.

        Returns
            
            data : `dict`
                A monday.com item in dictionary form.

        Return Fields
        
            assets : `list[moncli.entities.Asset]`
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

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    kwargs['item_id'] = gql.IntValue(item_id)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=DELETE_ITEM, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def duplicate_item(board_id: str, item_id: str, *args, **kwargs):
    """Duplicate an item.

        Parameters

            board_id : `str`
                The board's unique identifier.
            item_id : `str`
                The item's unique identifier.
            args : `tuple`
                The list of item return fields.
            kwargs : `dict`
                Optional arguments for item.

        Returns
            
            data : `dict`
                A monday.com item in dictionary form.

        Return Fields
        
            assets : `list[moncli.entities.Asset]`
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

            api_key : `str`
                The monday.com v2 API user key.
            with_updates : `bool`
                Duplicate with the item's updates.
    """
    
    kwargs['board_id'] = gql.IntValue(board_id)
    kwargs['item_id'] = gql.IntValue(item_id)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=DUPLICATE_ITEM, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def create_update(body: str, item_id: str, *args, **kwargs):
    """Create a new update.

        Parameters
        
            body : `str`
                The update text.
            item_id : `str`
                The item's unique identifier.
            args : `tuple`
                The list of update return fields.
            kwargs : `dict`
                Optional arguments for creating updates.

        Returns
            
            data : `dict`
                A monday.com column in dictionary form.

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
            replies : `list[moncli.entities.Reply]
                The update's replies.
            text_body : `str`
                The update's text body.
            updated_at : `str`
                The update's last edit date.

         Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.        
            parent_id : `str`
                The parent post identifier.
    """
    
    kwargs['body'] = gql.StringValue(body)
    kwargs['item_id'] = gql.IntValue(item_id)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=CREATE_UPDATE, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def get_updates(*args, **kwargs):
    """Get a collection of updates.

        Parameters
        
            args : `tuple`
                The list of update return fields.
            kwargs : `dict`
                Optional arguments for querying updates.

        Returns
            
            data : `dict`
                A monday.com column in dictionary form.

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
            replies : `list[moncli.entities.Reply]
                The update's replies.
            text_body : `str`
                The update's text body.
            updated_at : `str`
                The update's last edit date.

         Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.        
            limit : `int`
                Number of updates to get; the default is 25.
            page : `int`
                Page number to get, starting at 1.
    """
    
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=UPDATES, operation_type=gql.OperationType.QUERY, fields=args, arguments=kwargs)


def delete_update(id: str, *args, **kwargs):
    """Delete an update.

        Parameters
        
            id : `int`
                The update's unique identifier.
            args : `tuple`
                The list of update return fields.
            kwargs : `dict`
                Optional arguments for deleting updates.

        Returns
            
            data : `dict`
                A monday.com column in dictionary form.

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
            replies : `list[moncli.entities.Reply]
                The update's replies.
            text_body : `str`
                The update's text body.
            updated_at : `str`
                The update's last edit date.
        
         Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    kwargs['id'] = gql.IntValue(id)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=DELETE_UPDATE, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def create_notification(text: str, user_id: str, target_id: str, target_type: NotificationTargetType, *args, **kwargs):
    """Create a new notfication.

        Parameters
        
            text : `str`
                The notification text.
            user_id : `str`
                The user's unique identifier.
            target_id : `str`
                The target's unique identifier.
            target_type : `moncli.enums.NotificationTargetType`
                The target's type (Project / Post).
            args : `tuple`
                The list of notification return fields.
            kwargs : `dict`
                Optional arguments for creating notifications.

        Returns
            
            data : `dict`
                A monday.com notification in dictionary form.

        Return Fields
        
            id : `str`
                The notification's unique identifier.
            text : `str`
                The notification text.

         Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.        
            payload : `json`
                The notification payload.
    """
    
    kwargs['text'] = gql.StringValue(text)
    kwargs['user_id'] = gql.IntValue(user_id)
    kwargs['target_id'] = gql.IntValue(target_id)
    kwargs['target_type'] = gql.EnumValue(target_type)    
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=CREATE_NOTIFICATION, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def create_or_get_tag(tag_name: str, *args, **kwargs):
    """Create a new tag or get it if it already exists.

        Parameters
        
            tag_name : `str`
                The new tag's name.
            args : `tuple`
                The list of tag return fields.
            kwargs : `dict`
                Optional arguments for tag.

        Returns
            
            data : `dict`
                A monday.com tag in dictionary form.

        Return Fields
        
            color : `str`
                The tag's color.
            id : `str`
                The tag's unique identifier.
            name : `str`
                The tag's name.

        
         Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.        
            board_id : `str`
                The private board id to create the tag at (not needed for public boards).
    """
    
    kwargs['tag_name'] = gql.StringValue(tag_name)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=CREATE_OR_GET_TAG, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def get_tags(*args, **kwargs):
    """Get a collection of tags.

        Parameters
        
            args : `tuple`
                The list of tag return fields.
            kwargs : `dict`
                Optional arguments for tag.

        Returns
            
            data : `dict`
                A monday.com tag in dictionary form.

        Return Fields
        
            color : `str`
                The tag's color.
            id : `str`
                The tag's unique identifier.
            name : `str`
                The tag's name.
        
         Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.
            ids : `list[str]`
                A list of tags unique identifiers.
    """
    
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=TAGS, operation_type=gql.OperationType.QUERY, fields=args, arguments=kwargs)


def add_file_to_update(update_id: str, file_path: str, *args, **kwargs):
    """Add a file to an update.

        Parameters
        
            update_id : `str`
                The update to add the file to.
            file_path : `str`
                The path of the file to upload.
            args : `tuple`
                The list of asset return fields.
            kwargs : `dict`
                Optional arguments for adding file to update.

        Returns
            
            data : `dict`
                A monday.com asset in dictionary form.

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
            uploaded_by : `moncli.entities.user.User`
                The user who uploaded the file
            url : `str`
                The user who uploaded the file
            url_thumbnail : `str`
                Url to view the asset in thumbnail mode. Only available for images.  
        
         Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    kwargs['file'] = gql.FileValue('$file')
    kwargs['update_id'] = gql.IntValue(update_id)
    return upload_file(file_path, api_key=kwargs.pop('api_key', None), query_name=ADD_FILE_TO_UPDATE, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def add_file_to_column(item_id: str, column_id: str, file_path: str, *args, **kwargs):
    """Add a file to a column value.

        Parameters
        
            item_id : `str`
                The item to add the file to.
            column_id : `str`
                The column to add the file to.
            file_path : `str`
                The path of the file to add.
            args : `tuple`
                The list of asset return fields.
            kwargs : `dict`
                Optional arguments for adding file to column.

        Returns
            
            data : `dict`
                A monday.com asset in dictionary form.

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
            uploaded_by : `moncli.entities.user.User`
                The user who uploaded the file
            url : `str`
                The user who uploaded the file
            url_thumbnail : `str`
                Url to view the asset in thumbnail mode. Only available for images.

         Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    kwargs['file'] = gql.FileValue('$file')
    kwargs['item_id'] = gql.IntValue(item_id)
    kwargs['column_id'] = gql.StringValue(column_id)
    return upload_file(file_path, api_key=kwargs.pop('api_key', None), query_name=ADD_FILE_TO_COLUMN, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def get_users(*args, **kwargs):
    """Get a collection of users.

        Parameters
        
            args : `tuple`
                The list of user return fields.
            kwargs : `dict`
                Optional arguments for querying users.

        Returns
            
            data : `dict`
                A monday.com user in dictionary form.

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

            api_key : `str`
                The monday.com v2 API user key.
            ids : `list[str]`
                A list of users unique identifiers.
            kind : `moncli.enums.UserKind`
                The kind to search users by (all / non_guests / guests / non_pending).
            newest_first : `bool`
                Get the recently created users at the top of the list.
            limit : `int`
                Nimber of users to get.
    """
    
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=USERS, operation_type=gql.OperationType.QUERY, fields=args, arguments=kwargs)


def get_teams(*args, **kwargs):
    """Get a collection of teams.

        Parameters
        
            args : `tuple`
                The list of team return fields.
            kwargs : `dict`
                Optional arguments for querying teams.

        Returns
            
            data : `dict`
                A monday.com team in dictionary form.

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

            api_key : `str`
                The monday.com v2 API user key.
            ids : `list[str]`
                A list of teams unique identifiers.
    """
    
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=TEAMS, operation_type=gql.OperationType.QUERY, fields=args, arguments=kwargs)


def get_me(*args, **kwargs):
    """Get the connected user's information.

        Parameters
        
            args : `tuple`
                The list of user return fields.
            kwargs : `dict`
                Optional arguments for getting my user.

        Returns
            
            data : `dict`
                A monday.com user in dictionary form.

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

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=ME, operation_type=gql.OperationType.QUERY, fields=args, arguments=kwargs)


def get_account(*args, **kwargs):
    """Get the connected account's information.

        Parameters
        
            api_key : `str`
                The monday.com v2 API user key.
            args : `tuple`
                The list of account return fields.
            kwargs : `dict`
                Optional arguments for querying accounts.

        Returns
            
            data : `dict`
                A monday.com account in dictionary form.

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

         Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=ACCOUNT, operation_type=gql.OperationType.QUERY, fields=args, arguments=kwargs)


def create_webhook(board_id: str, url: str, event: WebhookEventType, *args, **kwargs):
    """Create a new webhook.

        Parameters
        
            api_key : `str`
                The monday.com v2 API user key.
            board_id : `str`
                The board's unique identifier.
            url : `str`
                The webhook URL.
            event : `moncli.enum.WebhookEventType`
                The event to listen to (incoming_notification / change_column_value / change_specific_column_value / create_item / create_update).
            args : `tuple`
                The list of webhook return fields.
            kwargs : `dict`
                Optional arguments for creating webhook.

        Returns
            
            data : `dict`
                A monday.com webhook in dictionary form.

        Return Fields
        
            board_id : `str`
                The webhook's board id.
            id : `str`
                The webhook's unique identifier.

         Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.        
            config : `json`
                The webhook config.
    """
    
    kwargs['board_id'] = gql.IntValue(board_id)
    kwargs['url'] = gql.StringValue(url)
    kwargs['event'] = gql.EnumValue(event)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=CREATE_WEBHOOK, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def delete_webhook(webhook_id: str, *args, **kwargs):
    """Delete a new webhook.

        Parameters
        
            webhook_id : `str`
                The webhook's unique identifier.
            args : `tuple`
                The list of webhook return fields.
            kwargs : `dict`
                Optional arguments for deleting webhook.

        Returns
            
            data : `dict`
                A monday.com webhook in dictionary form.

        Return Fields
        
            board_id : `str`
                The webhook's board id.
            id : `str`
                The webhook's unique identifier.

         Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.
    """
    
    kwargs['id'] = gql.IntValue(webhook_id)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=DELETE_WEBHOOK, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def create_workspace(name: str, kind: WorkspaceKind, *args, **kwargs):
    """Create a new workspace.

        Parameters
        
            name : `str`
                The Workspace's name
            kind : `moncli.enums.WorkspaceKind`
                The workspace's kind (open / closed)
            args : `tuple`
                The list of workspace return fields.
            kwargs : `dict`
                Optional arguments for creating workspace.

        Returns
            
            data : `dict`
                A monday.com workspace in dictionary form.

        Return Fields
        
            id : `str`
                The workspace's unique identifier.
            name : `str`
                The workspace's name.
            kind : `str`
                The workspace's kind (open / closed)
            description : `str`
                The workspace's description

         Optional Arguments

            api_key : `str`
                The monday.com v2 API user key.        
            description : `str`
                The Workspace's description.
    """
    
    kwargs['name'] = gql.StringValue(name)
    kwargs['kind'] = gql.EnumValue(kind)
    return execute_query(api_key=kwargs.pop('api_key', None), query_name=CREATE_WORKSPACE, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def add_users_to_workspace(workspace_id: str,user_ids: list(), kind: WorkspaceSubscriberKind, *args, **kwargs):
        """Allows you to add users to a workspace. You can define if users will be added as regular subscribers or as owners of the workspace.

            Parameters 

                workspace_id: int
                     The workspace's unique identifier
                user_ids: `list[str]`
                    User IDs to subscribe to the workspace
                kind: WorkspaceSUbscriberKind
                    Kind of subscribers added (subscriber/owner)
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

                api_key: `str`
                    The monday.com v2 API user key.
                kwargs: dict
                    Additional Arguments
        """

        kwargs["workspace_id"]= gql.IntValue(workspace_id)      
        kwargs['user_ids'] = gql.ListValue([int(id) for id in user_ids])
        kwargs["kind"]= gql.EnumValue(kind)
        
        return execute_query(api_key=kwargs.pop('api_key', None), query_name=ADD_USERS_TO_WORKSPACE, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)

      
def delete_users_from_workspace(workspace_id: str, user_ids: list(), *args: tuple, **kwargs: dict ):
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

                api_key: `str`
                    The monday.com v2 API user key.
                kwargs: dict
                    Additional Arguments
                
    """
    
    kwargs["workspace_id"]= gql.IntValue(workspace_id)
    kwargs['user_ids'] = gql.ListValue([int(id) for id in user_ids])

    return execute_query(api_key=kwargs.pop('api_key', None), query_name=DELETE_USERS_FROM_WORKSPACE, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)

  
def add_teams_to_workspace(workspace_id: str, team_ids: list(), *args, **kwargs ):
    """
        Allows you to add teams to a workspace.

        Parameters

            workspace_id: str
                The workspace's unique identifier.
            team_ids: list()
                Team ids to subscribe to the workspace.
        
        Returns
            
            data : `dict`
                A monday.com team in dictionary form.

        Return Fields
        
            id : `int`
                The team's unique identifier.
            name : `str`
                The team's name.
            picture_url : `str`
                The team's picture url.
            users : `moncli.entities.user.User`
                The users in the team.

    """
    kwargs['workspace_id'] = gql.IntValue(workspace_id)
    kwargs['team_ids'] = gql.ListValue(int(id) for id in team_ids)

    return execute_query(api_key=kwargs.pop('api_key', None), query_name=ADD_TEAMS_TO_WORKSPACE, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)


def delete_teams_from_workspace(workspace_id: str, team_ids: list(), *args, **kwargs ):
    """
        Allows you to remove teams to a workspace.

        Parameters

            workspace_id: str
                The workspace's unique identifier.
            team_ids: list()
                Team ids to subscribe to the workspace.
                
        Returns
            
            data : `dict`
                A monday.com team in dictionary form.

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

            api_key : `str`
                The monday.com v2 API user key.


    """
    kwargs['workspace_id'] = gql.IntValue(workspace_id)
    kwargs['team_ids'] = gql.ListValue(int(id) for id in team_ids)

    return execute_query(api_key=kwargs.pop('api_key', None), query_name=DELETE_TEAMS_FROM_WORKSPACE, operation_type=gql.OperationType.MUTATION, fields=args, arguments=kwargs)