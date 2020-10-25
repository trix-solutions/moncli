from typing import List, Dict, Any

from ..enums import BoardKind, ColumnType, NotificationTargetType, WebhookEventType, WorkspaceKind
from . import graphql as util, requests, constants
from .exceptions import MondayApiError


def create_board(api_key: str, board_name: str, board_kind: BoardKind, *args, **kwargs):
    """Create a new board.

    __________
    Parameters

        api_key : `str`
            The monday.com v2 API user key.
        board_name : `str`
            The board's name.
        board_kind : `moncli.enums.BoardKind`
            The board's kind (public / private / share)
        args : `tuple`
            The list of board return fields.
        kwargs : `dict`
            Optional keyword arguments for creating boards.

    _______
    Returns

        board_data : `dict`
            A monday.com board in dictionary form.

    _____________
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

    __________________
    Optional Arguments

        workspace_id : `int`
            Optional workspace id.
        template_id : `int`
            Optional board template id.
    """

    args = get_field_list(constants.DEFAULT_BOARD_QUERY_FIELDS)
    kwargs = get_method_arguments(constants.CREATE_BOARD_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_name'] = util.StringValue(board_name)
    kwargs['board_kind'] = util.EnumValue(board_kind)
    return execute_mutation(api_key, constants.CREATE_BOARD, *args,  **kwargs)


def get_boards(api_key: str, *args, **kwargs) -> List[Dict[str, Any]]:
    """

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        args : `tuple`
            The list of board return fields.
        kwargs : `dict`
            Optional keyword arguments for querying boards.

    _______
    Returns

        data : `dict`
            A monday.com board in dictionary form.

    _____________
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

    __________________
    Optional Arguments

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
        newest_first : `bool`
            Get the recently created boards at the top of the list.        

    """
    
    args = get_field_list(constants.DEFAULT_BOARD_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.BOARDS_OPTIONAL_PARAMS, **kwargs)
    operation = util.create_query(constants.BOARDS, *args, **kwargs)
    return requests.execute_query(api_key, operation=operation)[constants.BOARDS]   


def archive_board(api_key: str, board_id: str, *args, **kwargs):
    """

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        board_id : `str`
            The board's unique identifier.
        args : `tuple`
            The list of board return fields.
        kwargs : `dict`
            Optional keyword arguments for archiving boards.

    _______
    Returns
        
        data : `dict`
            A monday.com board in dictionary form.

    _____________
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
    
    args = get_field_list(constants.DEFAULT_BOARD_QUERY_FIELDS)
    kwargs = get_method_arguments(constants.ARCHIVE_BOARD_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    return execute_mutation(api_key, constants.ARCHIVE_BOARD, *args, **kwargs)


def add_subscribers_to_board(api_key: str, board_id: str, user_ids: list, *args, **kwargs):
    """Add subscribers to a board.

    __________
    Parameters

        api_key : `str`
            The monday.com v2 API user key.
        board_id : `str`
            The board's unique identifier.
        user_ids : `list[str]`
            User ids to subscribe to a board.
        args : `tuple`
            The list of user return fields.
        kwargs : `dict`
            Optional keyword arguments for adding board subscribers.

    _______
    Returns

        data : `dict`
            A monday.com user in dictionary form.
    
    _____________
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

    __________________
    Optional Arguments

        kind : `moncli.enums.SubscriberKind`
            Subscribers kind (subscriber / owner).
    """

    args = get_field_list(constants.DEFAULT_USER_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.ADD_SUBSCRIBERS_TO_BOARD_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['user_ids'] = util.ListValue([int(id) for id in user_ids])
    return execute_mutation(api_key, constants.ADD_SUBSCRIBERS_TO_BOARD, *args, **kwargs)


def delete_subscribers_from_board(api_key: str, board_id: str, user_ids: list, *args, **kwargs):
    """Remove subscribers from the board.

    __________
    Parameters

        api_key : `str`
            The monday.com v2 API user key.
        board_id : `str`
            The board's unique identifier.
        user_ids : `list[str]`
            User ids to unsubscribe from board.
        args : `tuple`
            The list of user return fields.
        kwargs : `dict`
            Additional keyword arguments for deleting subscribers.

    _______
    Returns

        data : `dict`
            A monday.com user in dictionary form.
    
    _____________
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
    """

    args = get_field_list(constants.DEFAULT_USER_QUERY_FIELDS, *args)
    kwargs = {
        'board_id': util.IntValue(board_id),
        'user_ids': util.ListValue([int(id) for id in user_ids])
    }
    return execute_mutation(api_key, constants.DELETE_SUBSCRIBERS_FROM_BOARD, *args, **kwargs)

    
def create_column(api_key: str, board_id: str, title: str, column_type: ColumnType, *args, **kwargs):
    """Create a new column in board.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        board_id : `str`
            The board's unique identifier.
        title : `str`
            The new column's title.
        args : `tuple`
            The list of column return fields.
        kwargs : `dict`
            Optional keyword arguments for creating columns.

    _______
    Returns
        
        data : `dict`
            A monday.com column in dictionary form.

    _____________
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

    __________________
    Optional Arguments

        column_type : `moncli.enumns.ColumnType`
            The type of column to create.
        defaults : `json`
            The new column's defaults.
    """
    
    args = get_field_list(constants.DEFAULT_COLUMN_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CREATE_COLUMN_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['title'] = util.StringValue(title)
    kwargs['column_type'] = util.EnumValue(column_type)
    return execute_mutation(api_key, constants.CREATE_COLUMN, *args, **kwargs)


def change_column_value(api_key: str, item_id: str, column_id: str, board_id: str, value: str, *args, **kwargs):
    """Change an item's column value.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
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

    _______
    Returns
        
        data : `dict`
            A monday.com column in item form.

    _____________
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
    """
    
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CHANGE_COLUMN_VALUE_OPTIONAL_PARAMS)
    kwargs['item_id'] = util.IntValue(item_id)
    kwargs['column_id'] = util.StringValue(column_id)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['value'] = util.JsonValue(value)
    return execute_mutation(api_key, constants.CHANGE_COLUMN_VALUE, *args, **kwargs)


def change_multiple_column_value(api_key: str, item_id: str, board_id: str, column_values: dict, *args, **kwargs):
    """Changes the column values of a specific item.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
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

    _______
    Returns
        
        data : `dict`
            A monday.com column in item form.

    _____________
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
    """
    
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CHANGE_MULTIPLE_COLUMN_VALUES_OPTIONAL_PARAMS, **kwargs)
    kwargs['item_id'] = util.IntValue(item_id)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['column_values'] = util.JsonValue(column_values)
    return execute_mutation(api_key, constants.CHANGE_MULTIPLE_COLUMN_VALUES, *args, **kwargs)


def get_assets(api_key: str, ids: list, *args, **kwargs):
    """Get a collection of assets by ids.

    __________
    Parameters

        api_key : `str`
            The monday.com v2 API user key.
        ids : `list[str]`
            Ids of the assets/files you want to get.
        args : `tuple`
            The list of asset return fields.
        kwargs : `dict`
            Optional arguments for querying assets.

    _______
    Returns
        
        data : `dict`
            A monday.com asset in item form.

    _____________
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
    """
    
    args = get_field_list(constants.DEFAULT_ASSET_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.ASSETS_OPTIONAL_PARAMS, **kwargs)
    ids = [util.IntValue(id).value for id in ids]
    kwargs['ids'] = util.ListValue(ids)
    return execute_query(api_key, constants.ASSETS, *args, **kwargs)


def duplicate_group(api_key: str, board_id: str, group_id: str, *args, **kwargs):
    """Duplicate a group.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        board_ id : `str`
            The board's unique identifier.
        group_id : `str`
            The group's unique identifier.
        args : `tuple`
            The list of asset return fields.
        kwargs : `dict`
            Optional arguments for querying assets.

    _______
    Returns
        
        data : `dict`
            A monday.com group in item form.

    _____________
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

    __________________
    Optional Arguments
    
        add_to_top : `bool`
            Should the new group be added to the top.
        group_title : `str`
            The group's title.
    """
    
    args = get_field_list(constants.DEFAULT_GROUP_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.DUPLICATE_GROUP_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['group_id'] = util.StringValue(group_id)
    return execute_mutation(api_key, constants.DUPLICATE_GROUP, *args, **kwargs)


def create_group(api_key: str, board_id: str, group_name: str, *args, **kwargs):
    """Creates a new group in a specific board.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        board_id : `str`
            The board's unique identifier.
        group_name : `str`
            The name of the new group.
        args : `tuple`
            The list of group return fields.
        kwargs : `dict`
            Optional arguments for querying assets.

    _______
    Returns
        
        data : `dict`
            A monday.com group in item form.

    _____________
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
    """
    
    args = get_field_list(constants.DEFAULT_GROUP_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CREATE_GROUP_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['group_name'] = util.StringValue(group_name)
    return execute_mutation(api_key, constants.CREATE_GROUP, *args, **kwargs)


def archive_group(api_key: str, board_id: str, group_id: str, *args, **kwargs):
    """Archives a group in a specific board.

    __________
    Parameters

        api_key : `str`
            The monday.com v2 API user key.
        board_id : `str`
            The board's unique identifier.
        group_id : `str`
            The group's unique identifier.
        args : `tuple`
            The list of group return fields.
        kwargs : `dict`
            Optional arguments for archiving groups.

    _______
    Returns
        
        data : `dict`
            A monday.com group in item form.

    _____________
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
    """
    
    args = get_field_list(constants.DEFAULT_GROUP_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.ARCHIVE_GROUP_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['group_id'] = util.StringValue(group_id)    
    return execute_mutation(api_key, constants.ARCHIVE_GROUP, *args, **kwargs)


def delete_group(api_key: str, board_id: str, group_id: str, *args, **kwargs):
    """Deletes a group in a specific board.

    __________
    Parameters

        api_key : `str`
            The monday.com v2 API user key.
        board_id : `str`
            The board's unique identifier.
        group_id : `str`
            The group's unique identifier.
        args : `tuple`
            The list of group return fields.
        kwargs : `dict`
            Optional arguments for deleting groups.

    _______
    Returns
        
        data : `dict`
            A monday.com group in item form.

    _____________
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
    """
    
    args = get_field_list(constants.DEFAULT_GROUP_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.DELETE_GROUP_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['group_id'] = util.StringValue(group_id)       
    return execute_mutation(api_key, constants.DELETE_GROUP, *args, **kwargs)


def create_item(api_key: str, item_name: str, board_id: str, *args, **kwargs):
    """Create a new item.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        item_name : `str`
            The new item's name.
        board_id : `str`
            The board's unique identifier.
        args : `tuple`
            The list of item return fields.
        kwargs : `dict`
            Optional arguments for creating items.

    _______
    Returns
                
        data : `dict`
            A monday.com column in item form.

    _____________
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

    __________________
    Optional Arguments
    
        group_id : `str`
            The group's unique identifier.
        column_values : `json`
            The column values of the new item.
    """
    
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CREATE_ITEM_OPTIONAL_PARAMS, **kwargs)
    kwargs['item_name'] = util.StringValue(item_name)
    kwargs['board_id'] = util.IntValue(board_id)    
    return execute_mutation(api_key, constants.CREATE_ITEM, *args, **kwargs)


def create_subitem(api_key: str, parent_item_id: str, item_name: str, *args, **kwargs):
    """Create subitem.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        parent_item_id : `str`
            The parent item's unique identifier.
        item_name : `str`
            The new item's name.
        args : `tuple`
            The list of item return fields.
        kwargs : `dict`
            Optional arguments for creating subitems.

    _______
    Returns
                
        data : `dict`
            A monday.com column in item form.

    _____________
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

    __________________
    Optional Arguments
    
        column_values : `json`
            The column values of the new item.
    """

    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CREATE_SUBITEM_OPTIONAL_PARAMS, **kwargs)
    kwargs['parent_item_id'] = util.IntValue(parent_item_id)
    kwargs['item_name'] = util.StringValue(item_name)
    return execute_mutation(api_key, constants.CREATE_SUBITEM, *args, **kwargs)


def get_items(api_key: str, *args, **kwargs):
    """Get a collection of items.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        args : `tuple`
            The list of item return fields.
        kwargs : `dict`
            Optional arguments for querying items.

    _______
    Returns
        
        data : `dict`
            A monday.com column in item form.

    _____________
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

    __________________
    Optional Arguments
    
        limit : `int`
            Number of items to get; the default is 25.
        page : `int`
            Page number to get, starting at 1.
        ids : `list[str]`
            A list of items unique identifiers.
        mewest_first : `bool`
            Get the recently created items at the top of the list.
    """
    
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.ITEMS_OPTIONAL_PARAMS, **kwargs) 
    return execute_query(api_key, constants.ITEMS, *args, **kwargs)


def get_items_by_column_values(api_key: str, board_id: str, column_id: str, column_value: str, *args, **kwargs):
    """Search items by their column values.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
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

    _______
    Returns
        
        data : `dict`
            A monday.com column in item form.

    _____________
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

    __________________
    Optional Arguments
    
        limit : `int`
            Number of items to get.
        page : `int`
            Page number to get, starting at 1.
        column_type : `str`
            The column type.
        state : `moncli.enums.State`
            The state of the item (all / active / archived / deleted); the default is active.
    """
    
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.ITEMS_BY_COLUMN_VALUES_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['column_id'] = util.StringValue(column_id)
    kwargs['column_value'] = util.StringValue(column_value)
    return execute_query(api_key, constants.ITEMS_BY_COLUMN_VALUES, *args, **kwargs)


def clear_item_updates(api_key: str, item_id: str, *args, **kwargs):
    """Clear an item's updates.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        item_id : `str`
            The item's unique identifier.
        args : `tuple`
            The list of item return fields.
        kwargs : `dict`
            Optional arguments for clearing item updates.

    _______
    Returns
        
        data : `dict`
            A monday.com column in item form.

    _____________
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
    """
    
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs['item_id'] = util.IntValue(item_id)
    return execute_mutation(api_key, constants.CLEAR_ITEM_UPDATES, *args, **kwargs)


def move_item_to_group(api_key: str, item_id: str, group_id: str, *args, **kwargs):
    """Move an item to a different group.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        item_id : `str`
            The item's unique identifier.
        group_id : `str`
            The group's unique identifier.
        args : `tuple`
            The list of item return fields.
        kwargs : `dict`
            Optional arguments for moving item to group.

    _______
    Returns
        
        data : `dict`
            A monday.com column in item form.

    _____________
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
    """
    
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.MOVE_ITEM_TO_GROUP_OPTIONAL_PARAMS, **kwargs)
    kwargs['item_id'] = util.IntValue(item_id)
    kwargs['group_id'] = util.StringValue(group_id)
    return execute_mutation(api_key, constants.MOVE_ITEM_TO_GROUP, *args, **kwargs)


def archive_item(api_key: str, item_id: str, *args, **kwargs):
    """Archive an item.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        item_id : `str`
            The item's unique identifier.
        args : `tuple`
            The list of item return fields.
        kwargs : `dict`
            Optional arguments for archiving items.

    _______
    Returns
        
        data : `dict`
            A monday.com column in item form.

    _____________
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
    """
    
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.ARCHIVE_ITEM_OPTIONAL_PARAMS, **kwargs)
    kwargs['item_id'] = util.IntValue(item_id)
    return execute_mutation(api_key, constants.ARCHIVE_ITEM, *args, **kwargs)


def delete_item(api_key: str, item_id: str, *args, **kwargs):
    """Delete an item.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        item_id : `str`
            The item's unique identifier.
        args : `tuple`
            The list of item return fields.
        kwargs : `dict`
            Optional arguments for item.

    _______
    Returns
        
        data : `dict`
            A monday.com item in dictionary form.

    _____________
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
    """
    
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.DELETE_ITEM_OPTIONAL_PARAMS, **kwargs)
    kwargs['item_id'] = util.IntValue(item_id)
    return execute_mutation(api_key, constants.DELETE_ITEM, *args, **kwargs)


def duplicate_item(api_key: str, board_id: str, item_id: str, *args, **kwargs):
    """Duplicate an item.

    __________
    Parameters

        api_key : `str`
            The monday.com v2 API user key.
        board_id : `str`
            The board's unique identifier.
        item_id : `str`
            The item's unique identifier.
        args : `tuple`
            The list of item return fields.
        kwargs : `dict`
            Optional arguments for item.

    _______
    Returns
        
        data : `dict`
            A monday.com item in dictionary form.

    _____________
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

    __________________
    Optional Arguments

        with_updates : `bool`
            Duplicate with the item's updates.
    """
    
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = {
        'board_id': util.IntValue(board_id),
        'item_id': util.IntValue(item_id)
    }
    kwargs = get_method_arguments(constants.DELETE_ITEM_OPTIONAL_PARAMS, **kwargs)
    return execute_mutation(api_key, constants.DUPLICATE_ITEM, *args, **kwargs)


def create_update(api_key: str, body: str, item_id: str, *args, **kwargs):
    """Create a new update.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        body : `str`
            The update text.
        item_id : `str`
            The item's unique identifier.
        args : `tuple`
            The list of update return fields.
        kwargs : `dict`
            Optional arguments for creating updates.

    _______
    Returns
        
        data : `dict`
            A monday.com column in dictionary form.

    _____________
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

    __________________
    Optional Arguments
    
        parent_id : `str`
            The parent post identifier.
    """
    
    args = get_field_list(constants.DEFAULT_UPDATE_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CREATE_UPDATE_OPTIONAL_PARAMS, **kwargs)
    kwargs['body'] = util.StringValue(body)
    kwargs['item_id'] = util.IntValue(item_id)
    return execute_mutation(api_key, constants.CREATE_UPDATE, *args, **kwargs)


def get_updates(api_key: str, *args, **kwargs):
    """Get a collection of updates.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        args : `tuple`
            The list of update return fields.
        kwargs : `dict`
            Optional arguments for querying updates.

    _______
    Returns
        
        data : `dict`
            A monday.com column in dictionary form.

    _____________
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

    __________________
    Optional Arguments
    
        limit : `int`
            Number of updates to get; the default is 25.
        page : `int`
            Page number to get, starting at 1.
    """
    
    args = get_field_list(constants.DEFAULT_UPDATE_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.UPDATES_OPTIONAL_PARAMS, **kwargs)
    return execute_query(api_key, constants.UPDATES, *args, **kwargs)


def delete_update(api_key: str, id: str, *args, **kwargs):
    """Delete an update.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        id : `int`
            The update's unique identifier.
        args : `tuple`
            The list of update return fields.
        kwargs : `dict`
            Optional arguments for deleting updates.

    _______
    Returns
        
        data : `dict`
            A monday.com column in dictionary form.

    _____________
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
    """
    
    args = get_field_list(constants.DEFAULT_UPDATE_QUERY_FIELDS, *args)
    kwargs['id'] = util.IntValue(id)
    return execute_mutation(api_key, constants.DELETE_UPDATE, *args, **kwargs)


def create_notification(api_key: str, text: str, user_id: str, target_id: str, target_type: NotificationTargetType, *args, **kwargs):
    """Create a new notfication.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
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

    _______
    Returns
        
        data : `dict`
            A monday.com notification in dictionary form.

    _____________
    Return Fields
    
        id : `str`
            The notification's unique identifier.
        text : `str`
            The notification text.

    __________________
    Optional Arguments
    
        payload : `json`
            The notification payload.
    """
    
    args = get_field_list(constants.DEFAULT_NOTIFICATION_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CREATE_NOTIFICATION_OPTIONAL_PARAMS, **kwargs)
    kwargs['text'] = util.StringValue(text)
    kwargs['user_id'] = util.IntValue(user_id)
    kwargs['target_id'] = util.IntValue(target_id)
    kwargs['target_type'] = util.EnumValue(target_type)    
    return execute_mutation(api_key, constants.CREATE_NOTIFICATION, *args, **kwargs)


def create_or_get_tag(api_key: str, tag_name: str, *args, **kwargs):
    """Create a new tag or get it if it already exists.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        tag_name : `str`
            The new tag's name.
        args : `tuple`
            The list of tag return fields.
        kwargs : `dict`
            Optional arguments for tag.

    _______
    Returns
        
        data : `dict`
            A monday.com tag in dictionary form.

    _____________
    Return Fields
    
        color : `str`
            The tag's color.
        id : `str`
            The tag's unique identifier.
        name : `str`
            The tag's name.

    __________________
    Optional Arguments
    
        board_id : `str`
            The private board id to create the tag at (not needed for public boards).
    """
    
    args = get_field_list(constants.DEFAULT_TAG_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CREATE_OR_GET_TAG_OPTIONAL_PARAMS, **kwargs)
    kwargs['tag_name'] = util.StringValue(tag_name)
    return execute_mutation(api_key, constants.CREATE_OR_GET_TAG, *args, **kwargs)


def get_tags(api_key: str, *args, **kwargs):
    """Get a collection of tags.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        args : `tuple`
            The list of tag return fields.
        kwargs : `dict`
            Optional arguments for tag.

    _______
    Returns
        
        data : `dict`
            A monday.com tag in dictionary form.

    _____________
    Return Fields
    
        color : `str`
            The tag's color.
        id : `str`
            The tag's unique identifier.
        name : `str`
            The tag's name.

    __________________
    Optional Arguments
    
        ids : `list[str]`
            A list of tags unique identifiers.
    """
    
    args = get_field_list(constants.DEFAULT_TAG_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.TAGS_OPTIONAL_PARAMS, **kwargs)
    return execute_query(api_key, constants.TAGS, *args, **kwargs)


def add_file_to_update(api_key: str, update_id: str, file_path: str, *args, **kwargs):
    """Add a file to an update.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        update_id : `str`
            The update to add the file to.
        file_path : `str`
            The path of the file to upload.
        args : `tuple`
            The list of asset return fields.
        kwargs : `dict`
            Optional arguments for adding file to update.

    _______
    Returns
        
        data : `dict`
            A monday.com asset in dictionary form.

    _____________
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
    """
    
    name = constants.ADD_FILE_TO_UPDATE
    args = get_field_list(constants.DEFAULT_ASSET_QUERY_FIELDS, *args)
    kwargs['file'] = util.FileValue('$file')
    kwargs['update_id'] = util.IntValue(update_id)
    operation = util.create_mutation(name, *args, **kwargs)
    operation.add_query_variable('file', 'File!')
    result = requests.upload_file(api_key, file_path, operation=operation)
    return result[name]


def add_file_to_column(api_key: str, item_id: str, column_id: str, file_path: str, *args, **kwargs):
    """Add a file to a column value.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
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

    _______
    Returns
        
        data : `dict`
            A monday.com asset in dictionary form.

    _____________
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
    """
    
    name = constants.ADD_FILE_TO_COLUMN
    args = get_field_list(constants.DEFAULT_ASSET_QUERY_FIELDS)
    kwargs['file'] = util.FileValue('$file')
    kwargs['item_id'] = util.IntValue(item_id)
    kwargs['column_id'] = util.StringValue(column_id)
    operation = util.create_mutation(name, *args, **kwargs)
    operation.add_query_variable('file', 'File!')
    result = requests.upload_file(api_key, file_path, operation=operation)
    return result[name]


def get_users(api_key: str, *args, **kwargs):
    """Get a collection of users.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        args : `tuple`
            The list of user return fields.
        kwargs : `dict`
            Optional arguments for querying users.

    _______
    Returns
        
        data : `dict`
            A monday.com user in dictionary form.

    _____________
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

    __________________
    Optional Arguments
    
        ids : `list[str]`
            A list of users unique identifiers.
        kind : `moncli.enums.UserKind`
            The kind to search users by (all / non_guests / guests / non_pending).
        newest_first : `bool`
            Get the recently created users at the top of the list.
        limit : `int`
            Nimber of users to get.
    """
    
    args = get_field_list(constants.DEFAULT_USER_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.USERS_OPTIONAL_PARAMS, **kwargs)
    return execute_query(api_key, constants.USERS, *args, **kwargs)


def get_teams(api_key: str, *args, **kwargs):
    """Get a collection of teams.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        args : `tuple`
            The list of team return fields.
        kwargs : `dict`
            Optional arguments for querying teams.

    _______
    Returns
        
        data : `dict`
            A monday.com team in dictionary form.

    _____________
    Return Fields
    
        id : `int`
            The team's unique identifier.
        name : `str`
            The team's name.
        picture_url : `str`
            The team's picture url.
        users : `moncli.entities.user.User`
            The users in the team.

    __________________
    Optional Arguments
    
        ids : `list[str]`
            A list of teams unique identifiers.
    """
    
    args = get_field_list(constants.DEFAULT_TEAM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.TEAMS_OPTIONAL_PARAMS, **kwargs)
    return execute_query(api_key, constants.TEAMS, *args, **kwargs)


def get_me(api_key: str, *args, **kwargs):
    """Get the connected user's information.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        args : `tuple`
            The list of user return fields.
        kwargs : `dict`
            Optional arguments for getting my user.

    _______
    Returns
        
        data : `dict`
            A monday.com user in dictionary form.

    _____________
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
    """
    
    args = get_field_list(constants.DEFAULT_USER_QUERY_FIELDS, *args)
    return execute_query(api_key, constants.ME, *args, **kwargs)


def get_account(api_key: str, *args, **kwargs):
    """Get the connected account's information.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        args : `tuple`
            The list of account return fields.
        kwargs : `dict`
            Optional arguments for querying accounts.

    _______
    Returns
        
        data : `dict`
            A monday.com account in dictionary form.

    _____________
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
    
    args = get_field_list(constants.DEFAULT_ACCOUNT_QUERY_FIELDS, *args)
    return execute_query(api_key, constants.ACCOUNT, *args, **kwargs)


def create_webhook(api_key: str, board_id: str, url: str, event: WebhookEventType, *args, **kwargs):
    """Create a new webhook.

    __________
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

    _______
    Returns
        
        data : `dict`
            A monday.com webhook in dictionary form.

    _____________
    Return Fields
    
        board_id : `str`
            The webhook's board id.
        id : `str`
            The webhook's unique identifier.

    __________________
    Optional Arguments
    
        config : `json`
            The webhook config.
    """
    
    args = get_field_list(constants.DEFAULT_WEBHOOK_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CREATE_WEBHOOK_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['url'] = util.StringValue(url)
    kwargs['event'] = util.EnumValue(event)
    return execute_mutation(api_key, constants.CREATE_WEBHOOK, *args, **kwargs)


def delete_webhook(api_key: str, webhook_id: str, *args, **kwargs):
    """Delete a new webhook.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        webhook_id : `str`
            The webhook's unique identifier.
        args : `tuple`
            The list of webhook return fields.
        kwargs : `dict`
            Optional arguments for deleting webhook.

    _______
    Returns
        
        data : `dict`
            A monday.com webhook in dictionary form.

    _____________
    Return Fields
    
        board_id : `str`
            The webhook's board id.
        id : `str`
            The webhook's unique identifier.
    """
    
    args = get_field_list(constants.DEFAULT_WEBHOOK_QUERY_FIELDS, *args)
    kwargs['id'] = util.IntValue(webhook_id)
    return execute_mutation(api_key, constants.DELETE_WEBHOOK, *args, **kwargs)


def create_workspace(api_key: str, name: str, kind: WorkspaceKind, *args, **kwargs):
    """Create a new workspace.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        name : `str`
            The Workspace's name
        kind : `moncli.enums.WorkspaceKind`
            The workspace's kind (open / closed)
        args : `tuple`
            The list of workspace return fields.
        kwargs : `dict`
            Optional arguments for creating workspace.

    _______
    Returns
        
        data : `dict`
            A monday.com workspace in dictionary form.

    _____________
    Return Fields
    
        id : `str`
            The workspace's unique identifier.
        name : `str`
            The workspace's name.
        kind : `str`
            The workspace's kind (open / closed)
        description : `str`
            The workspace's description

    __________________
    Optional Arguments
    
        description : `str`
            The Workspace's description.
    """
    
    args = get_field_list(constants.DEFAULT_WORKSPACE_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CREATE_WORKSPACE_OPTIONAL_PARAMS, **kwargs)
    kwargs['name'] = util.StringValue(name)
    kwargs['kind'] = util.EnumValue(kind)
    return execute_mutation(api_key, constants.CREATE_WORKSPACE, *args, **kwargs)


def execute_query(api_key:str, query_name: str, *args, **kwargs):
    """Execute query operation.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        query_name : `str`
            The name of the executed query.
        args : `tuple`
            Collection of return fields.
        kwargs : `dict`
            Mapping of field arguments.

    _______
    Returns
        
        data : `dict`
            The query response in dictionary form.
    """
    
    operation = util.create_query(query_name, *args, **kwargs)
    result = requests.execute_query(api_key, operation=operation)
    return result[query_name]


def execute_mutation(api_key: str, query_name: str, *args, **kwargs):
    """Execute mutation operation.

    __________
    Parameters
    
        api_key : `str`
            The monday.com v2 API user key.
        query_name : `str`
            The name of the executed query.
        args : `tuple`
            Collection of return fields.
        kwargs : `dict`
            Mapping of field arguments.

    _______
    Returns
        
        data : `dict`
            The query response in dictionary form.

    """
    

    if kwargs.__contains__('include_complexity'):
        raise MondayApiError(query_name, 400, '', ['Query complexity cannot be retrieved for mutation requests.'])

    if 'id' not in args:
        args += ('id',)

    operation = util.create_mutation(query_name, *args, **kwargs)
    result = requests.execute_query(api_key, operation=operation)
    return result[query_name]


def get_field_list(fields: list, *args):
    """Get list of query fields.

    __________
    Parameters
    
        fields : `list[str]`
            A predefined collection of default fields.
        args : `tuple`
            Field names passed into the request.

    _______
    Returns
        
        fields : `list[str]`
            The fields to be retrieved for the query.
    """
    
    if not args:
        return fields
    return args


def get_method_arguments(mappings: dict, **kwargs):
    """Get mapped query field arguments.

    __________
    Parameters
    
        mappings : `dict`
            A predefined set of default mappings.
        kwargs : `dict`
            Argument parameters passed into the request.


    _______
    Returns
        
        arguments : `dict`
            Arguments to be used for the query fields.
    """
    
    result = {}
    for key, value in mappings.items():   
        try:
            if isinstance(value, util.ArgumentValueKind):
                result[key] = util.create_value(kwargs[key], value)
            elif type(value) is tuple:
                data = [util.create_value(item, value[1]).format() for item in kwargs[key]]
                result[key] = util.create_value(data, value[0])
            elif type(value) is dict:
                result[key] = get_method_arguments(value, **(kwargs[key]))
        except KeyError:
            # Ignore if no kwargs found
            continue
    return result