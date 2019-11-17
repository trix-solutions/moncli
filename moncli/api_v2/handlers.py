from typing import List, Dict, Any

from ..enums import BoardKind, ColumnType, NotificationTargetType
from . import graphql, requests, constants
from .graphql import StringValue, IntValue, ListValue, EnumValue, JsonValue, create_value


def create_board(api_key: str, board_name: str, board_kind: BoardKind, *argv, **kwargs):

    kwargs = get_method_arguments(constants.CREATE_BOARD_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_name'] = StringValue(board_name)
    kwargs['board_kind'] = EnumValue(board_kind)

    return execute_mutation(api_key, constants.CREATE_BOARD, *argv,  **kwargs)


def get_boards(api_key: str, *argv, **kwargs) -> List[Dict[str, Any]]:

    kwargs = get_method_arguments(constants.BOARDS_OPTIONAL_PARAMS, **kwargs)
    return execute_query(api_key, constants.BOARDS, *argv, **kwargs)


def archive_board(api_key: str, board_id: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.ARCHIVE_BOARD_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = IntValue(board_id)

    return execute_mutation(api_key, constants.ARCHIVE_BOARD, *argv, **kwargs)

    
def create_column(api_key: str, board_id: str, title: str, column_type: ColumnType, *argv, **kwargs):

    kwargs = get_method_arguments(constants.CREATE_COLUMN_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = IntValue(board_id)
    kwargs['title'] = StringValue(title)
    kwargs['column_type'] = EnumValue(column_type)

    return execute_mutation(api_key, constants.CREATE_COLUMN, *argv, **kwargs)


def change_column_value(api_key: str, item_id: str, column_id: str, board_id: str, value: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.CHANGE_COLUMN_VALUE_OPTIONAL_PARAMS)
    kwargs['item_id'] = IntValue(item_id)
    kwargs['column_id'] = StringValue(column_id)
    kwargs['board_id'] = IntValue(board_id)
    kwargs['value'] = JsonValue(value)

    return execute_mutation(api_key, constants.CHANGE_COLUMN_VALUE, *argv, **kwargs)


def change_multiple_column_value(api_key: str, item_id: str, board_id: str, column_values: dict, *argv, **kwargs):

    kwargs = get_method_arguments(constants.CHANGE_MULTIPLE_COLUMN_VALUES_OPTIONAL_PARAMS, **kwargs)
    kwargs['item_id'] = IntValue(item_id)
    kwargs['board_id'] = IntValue(board_id)
    kwargs['column_values'] = JsonValue(column_values)

    return execute_mutation(api_key, constants.CHANGE_MULTIPLE_COLUMN_VALUES, *argv, **kwargs)


def duplicate_group(api_key: str, board_id: str, group_id: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.DUPLICATE_GROUP_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = IntValue(board_id)
    kwargs['group_id'] = StringValue(group_id)
    
    return execute_mutation(api_key, constants.DUPLICATE_GROUP, *argv, **kwargs)


def create_group(api_key: str, board_id: str, group_name: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.CREATE_GROUP_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = IntValue(board_id)
    kwargs['group_name'] = StringValue(group_name)

    return execute_mutation(api_key, constants.CREATE_GROUP, *argv, **kwargs)


def archive_group(api_key: str, board_id: str, group_id: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.ARCHIVE_GROUP_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = IntValue(board_id)
    kwargs['group_id'] = StringValue(group_id)    

    return execute_mutation(api_key, constants.ARCHIVE_GROUP, *argv, **kwargs)


def delete_group(api_key: str, board_id: str, group_id: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.DELETE_GROUP_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = IntValue(board_id)
    kwargs['group_id'] = StringValue(group_id)    
    
    return execute_mutation(api_key, constants.DELETE_GROUP, *argv, **kwargs)


def create_item(api_key: str, item_name: str, board_id: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.CREATE_ITEM_OPTIONAL_PARAMS, **kwargs)
    kwargs['item_name'] = StringValue(item_name)
    kwargs['board_id'] = IntValue(board_id)    

    return execute_mutation(api_key, constants.CREATE_ITEM, *argv, **kwargs)


def get_items(api_key: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.ITEMS_OPTIONAL_PARAMS, **kwargs)
    return execute_query(api_key, constants.ITEMS, *argv, **kwargs)


def get_items_by_column_values(api_key: str, board_id: str, column_id: str, column_value: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.ITEMS_BY_COLUMN_VALUES_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = IntValue(board_id)
    kwargs['column_id'] = StringValue(column_id)
    kwargs['column_value'] = StringValue(column_value)

    return execute_query(api_key, constants.ITEMS_BY_COLUMN_VALUES, *argv, **kwargs)


def move_item_to_group(api_key: str, item_id: str, group_id: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.MOVE_ITEM_TO_GROUP_OPTIONAL_PARAMS, **kwargs)
    kwargs['item_id'] = IntValue(item_id)
    kwargs['group_id'] = StringValue(group_id)

    return execute_mutation(api_key, constants.MOVE_ITEM_TO_GROUP, *argv, **kwargs)


def archive_item(api_key: str, item_id: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.ARCHIVE_ITEM_OPTIONAL_PARAMS, **kwargs)
    kwargs['item_id'] = IntValue(item_id)

    return execute_mutation(api_key, constants.ARCHIVE_ITEM, *argv, **kwargs)


def delete_item(api_key: str, item_id: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.DELETE_ITEM_OPTIONAL_PARAMS, **kwargs)
    kwargs['item_id'] = IntValue(item_id)

    return execute_mutation(api_key, constants.DELETE_ITEM, *argv, **kwargs)


def create_update(api_key: str, body: str, item_id: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.CREATE_UPDATE_OPTIONAL_PARAMS, **kwargs)
    kwargs['body'] = StringValue(body)
    kwargs['item_id'] = IntValue(item_id)

    return execute_mutation(api_key, constants.CREATE_UPDATE, *argv, **kwargs)


def get_updates(api_key: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.UPDATES_OPTIONAL_PARAMS, **kwargs)
    return execute_query(api_key, constants.UPDATES, *argv, **kwargs)


def create_notification(api_key: str, text: str, user_id: str, target_id: str, target_type: NotificationTargetType, *argv, **kwargs):

    kwargs = get_method_arguments(constants.CREATE_NOTIFICATION_OPTIONAL_PARAMS, **kwargs)
    kwargs['text'] = StringValue(text)
    kwargs['user_id'] = IntValue(user_id)
    kwargs['target_id'] = IntValue(target_id)
    kwargs['target_type'] = EnumValue(target_type)    

    return execute_mutation(api_key, constants.CREATE_NOTIFICATION, *argv, **kwargs)


def create_or_get_tag(api_key: str, tag_name: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.CREATE_OR_GET_TAG_OPTIONAL_PARAMS, **kwargs)
    kwargs['tag_name'] = StringValue(tag_name)

    return execute_mutation(api_key, constants.CREATE_OR_GET_TAG, *argv, **kwargs)


def get_tags(api_key: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.TAGS_OPTIONAL_PARAMS, **kwargs)
    return execute_query(api_key, constants.TAGS, *argv, **kwargs)


def get_users(api_key: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.USERS_OPTIONAL_PARAMS, **kwargs)
    return execute_query(api_key, constants.USERS, *argv, **kwargs)


def get_teams(api_key: str, *argv, **kwargs):

    kwargs = get_method_arguments(constants.TEAMS_OPTIONAL_PARAMS, **kwargs)
    return execute_query(api_key, constants.TEAMS, *argv, **kwargs)


def get_me(api_key: str, *argv, **kwargs):

    return execute_query(api_key, constants.ME, *argv, **kwargs)


def execute_query(api_key:str, name: str, *argv, **kwargs):

    operation = graphql.create_query(name, *argv, **kwargs)
    result = requests.execute_query(api_key, operation=operation)
    return result[name]


def execute_mutation(api_key: str, name: str, *argv, **kwargs):

    if 'id' not in argv:
        argv += ('id',)

    operation = graphql.create_mutation(name, *argv, **kwargs)
    result = requests.execute_query(api_key, operation=operation)
    return result[name]


def get_method_arguments(mappings: dict, **kwargs):

    result = {}

    for key, value in kwargs.items():
        
        if mappings.__contains__(key):
            result[key] = create_value(value, mappings[key])

    return result