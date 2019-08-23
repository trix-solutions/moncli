from typing import List, Dict, Any

from moncli import graphql_entities as graphql
from moncli.enums import *
from moncli.graphql.requests import execute_query
from moncli.graphql.constants import *

def get_boards(api_key: str, *argv, **kwargs) -> List[Dict[str, Any]]:

    operation = graphql.create_query( 
        BOARDS, 
        *argv, 
        **kwargs)

    result = execute_query(api_key, operation=operation)
    return result[BOARDS]


def create_board(api_key: str, board_name: str, board_kind: BoardKind, *argv):

    operation = graphql.create_mutation( 
        CREATE_BOARD, 
        *argv, 
        board_name=board_name, 
        board_kind=board_kind)

    result = execute_query(api_key, operation=operation)
    return result[CREATE_BOARD]


def archive_board(api_key: str, board_id: str, *argv):

    operation = graphql.create_mutation(
        ARCHIVE_BOARD, 
        *argv, 
        board_id=int(board_id))

    result = execute_query(api_key, operation=operation)
    return result[ARCHIVE_BOARD]

    
def create_column(api_key: str, board_id: str, title: str, column_type: ColumnType):

    operation = graphql.create_mutation(
        CREATE_COLUMN, 
        'id',
        board_id=int(board_id), 
        title=title, 
        column_type=column_type)

    result = execute_query(api_key, operation=operation)
    return result[CREATE_COLUMN]


def duplicate_group(api_key: str, board_id: str, group_id: str, *argv, **kwargs):
    
    operation = graphql.create_mutation(
        DUPLICATE_GROUP, 
        *argv, 
        board_id=int(board_id), 
        group_id=group_id, 
        **kwargs)

    result = execute_query(api_key, operation=operation)
    return result[DUPLICATE_GROUP]


def create_group(api_key: str, board_id: str, group_name: str, *argv):

    operation = graphql.create_mutation(
        CREATE_GROUP, 
        *argv, 
        board_id=int(board_id), 
        group_name=group_name)

    result = execute_query(api_key, operation=operation)
    return result[CREATE_GROUP]


def archive_group(api_key: str, board_id: str, group_id: str, *argv):

    operation = graphql.create_mutation(
        ARCHIVE_GROUP, 
        *argv, 
        board_id=int(board_id), 
        group_id=group_id)

    result = execute_query(api_key, operation=operation)
    return result[ARCHIVE_GROUP]


def delete_group(api_key: str, board_id: str, group_id: str, *argv):
    
    operation = graphql.create_mutation(
        DELETE_GROUP, 
        *argv, 
        board_id=int(board_id), 
        group_id=group_id)

    result = execute_query(api_key, operation=operation)
    return result[DELETE_GROUP]

def get_items(api_key: str, *argv, **kwargs):

    operation = graphql.create_query(
        ITEMS, 
        *argv, 
        **kwargs)

    result = execute_query(api_key, operation=operation)
    return result[ITEMS]


def get_items_by_column_values(api_key: str, board_id: str, column_id: str, column_value: str, *argv, **kwargs):

    operation = graphql.create_mutation(
        ITEMS_BY_COLUMN_VALUES, 
        *argv,
        board_id=int(board_id), 
        column_id=column_id, 
        column_value=column_value, 
        **kwargs)

    result = execute_query(api_key, operation=operation)
    return result[ITEMS_BY_COLUMN_VALUES]

def create_item(api_key: str, item_name: str, board_id: str, *argv, **kwargs):

    operation = graphql.create_mutation(
        CREATE_ITEM,
        *argv,
        item_name=item_name,
        board_id=int(board_id),
        **kwargs)

    result = execute_query(api_key, operation=operation)
    return result[CREATE_ITEM]
