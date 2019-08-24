from typing import List, Dict, Any

from moncli import graphql_entities as graphql
from moncli.enums import BoardKind, ColumnType, NotificationTargetType
from moncli.graphql import requests
from moncli.graphql.constants import *


def create_board(api_key: str, board_name: str, board_kind: BoardKind, *argv):

    return execute_mutation( 
        api_key,
        CREATE_BOARD, 
        *argv, 
        board_name=board_name, 
        board_kind=board_kind)


def get_boards(api_key: str, *argv, **kwargs) -> List[Dict[str, Any]]:

    return execute_query(api_key, BOARDS, *argv, **kwargs)


def archive_board(api_key: str, board_id: str, *argv):

    return execute_mutation(
        api_key,
        ARCHIVE_BOARD, 
        *argv, 
        board_id=int(board_id))

    
def create_column(api_key: str, board_id: str, title: str, column_type: ColumnType):

    return execute_mutation(
        api_key,
        CREATE_COLUMN, 
        'id',
        board_id=int(board_id), 
        title=title, 
        column_type=column_type)


def change_column_value(api_key: str, item_id: str, column_id: str, board_id: str, value: str, *argv):

    return execute_mutation(
        api_key,
        CHANGE_COLUMN_VALUE,
        *argv,
        item_id=int(item_id),
        column_id=column_id,
        board_id=int(board_id),
        value=value)


def change_multiple_column_value(api_key: str, item_id: str, board_id: str, column_values: str, *argv):

    return execute_mutation(
        api_key,
        CHANGE_MULTIPLE_COLUMN_VALUES,
        *argv,
        item_id=int(item_id),
        board_id=int(board_id))


def duplicate_group(api_key: str, board_id: str, group_id: str, *argv, **kwargs):
    
    return execute_mutation(
        api_key,
        DUPLICATE_GROUP, 
        *argv, 
        board_id=int(board_id), 
        group_id=group_id, 
        **kwargs)


def create_group(api_key: str, board_id: str, group_name: str, *argv):

    return execute_mutation(
        api_key,
        CREATE_GROUP, 
        *argv, 
        board_id=int(board_id), 
        group_name=group_name)


def archive_group(api_key: str, board_id: str, group_id: str, *argv):

    return execute_mutation(
        api_key,
        ARCHIVE_GROUP, 
        *argv, 
        board_id=int(board_id), 
        group_id=group_id)


def delete_group(api_key: str, board_id: str, group_id: str, *argv):
    
    return execute_mutation(
        api_key,
        DELETE_GROUP, 
        *argv, 
        board_id=int(board_id), 
        group_id=group_id)


def create_item(api_key: str, item_name: str, board_id: str, *argv, **kwargs):

    return execute_mutation(
        api_key,    
        CREATE_ITEM,
        *argv,
        item_name=item_name,
        board_id=int(board_id),
        **kwargs)


def get_items(api_key: str, *argv, **kwargs):

    return execute_query(api_key, ITEMS, *argv, **kwargs)


def get_items_by_column_values(api_key: str, board_id: str, column_id: str, column_value: str, *argv, **kwargs):

    return execute_query(
        api_key,
        ITEMS_BY_COLUMN_VALUES, 
        *argv,
        board_id=int(board_id), 
        column_id=column_id, 
        column_value=column_value, 
        **kwargs)


def move_item_to_group(api_key: str, item_id: str, group_id: str, *argv):

    return execute_mutation(
        api_key,
        MOVE_ITEM_TO_GROUP,
        *argv,
        item_id=int(item_id),
        group_id=group_id)


def archive_item(api_key: str, item_id: str, *argv):

    return execute_mutation(
        api_key,
        ARCHIVE_ITEM,
        *argv,
        item_id=int(item_id))


def delete_item(api_key: str, item_id: str, *argv):

    return execute_mutation(
        api_key,
        DELETE_ITEM,
        *argv,
        item_id=int(item_id))


def create_update(api_key: str, body: str, item_id: str, *argv):

    return execute_mutation(
        api_key,
        CREATE_UPDATE,
        *argv,
        body=body,
        item_id=int(item_id))


def get_updates(api_key: str, *argv, **kwargs):

    return execute_query(api_key, UPDATES, *argv, **kwargs)


def create_notification(
        api_key: str,
        text: str,
        user_id: str,
        target_id: str,
        target_type: NotificationTargetType,
        payload: str,
        *argv):

    return execute_mutation(
        api_key,
        CREATE_NOTIFICATION,
        *argv,
        text=text,
        user_id=int(user_id),
        target_id=int(target_id),
        target_type=target_type,
        payload=payload)


def create_or_get_tag(api_key: str, tag_name: str, *argv, **kwargs):

    return execute_mutation(
        api_key,
        CREATE_OR_GET_TAG,
        *argv,
        tag_name=tag_name)


def get_tags(api_key: str, *argv, **kwargs):

    return execute_query(api_key, TAGS, *argv, **kwargs)


def get_users(api_key: str, *argv, **kwargs):

    return execute_query(api_key, USERS, *argv, **kwargs)


def get_teams(api_key: str, *argv, **kwargs):

    return execute_query(api_key, TEAMS, *argv, **kwargs)


def get_me(api_key: str, *argv, **kwargs):

    return execute_query(api_key, ME, *argv, **kwargs)


def execute_query(api_key:str, name: str, *argv, **kwargs):

    operation = graphql.create_query(name, *argv, **kwargs)
    result = requests.execute_query(api_key, operation=operation)
    return result[name]


def execute_mutation(api_key: str, name: str, *argv, **kwargs):

    operation = graphql.create_mutation(name, *argv, **kwargs)
    result = requests.execute_query(api_key, operation=operation)
    return result[name]