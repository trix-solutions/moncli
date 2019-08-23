from typing import List, Dict, Any

from moncli import BoardKind, ColumnType
from moncli.graphql import constants, GraphQLOperation, OperationType, execute_query

def get_boards(api_key: str, *argv, **kwargs) -> List[Dict[str, Any]]:

    operation = GraphQLOperation(
        OperationType.QUERY, 
        constants.BOARDS, 
        *argv, 
        **kwargs)

    result = execute_query(api_key, operation=operation)
    return result[constants.BOARDS]


def create_board(api_key: str, board_name: str, board_kind: BoardKind, *argv):

    operation = GraphQLOperation(
        OperationType.MUTATION, 
        constants.CREATE_BOARD, 
        *argv, 
        board_name=board_name, 
        board_kind=board_kind)

    result = execute_query(api_key, operation=operation)
    return result[constants.CREATE_BOARD]


def archive_board(api_key: str, board_id: str, *argv):

    operation = GraphQLOperation(
        OperationType.MUTATION, 
        constants.ARCHIVE_BOARD, 
        *argv, 
        board_id=int(board_id))

    result = execute_query(api_key, operation=operation)
    return result[constants.ARCHIVE_BOARD]

    
def create_column(api_key: str, board_id: str, title: str, column_type: ColumnType):

    operation = GraphQLOperation(
        OperationType.MUTATION, 
        constants.CREATE_COLUMN, 
        'id',
        board_id=int(board_id), 
        title=title, 
        column_type=column_type)

    result = execute_query(api_key, operation=operation)
    return result[constants.CREATE_COLUMN]


def duplicate_group(api_key: str, board_id: str, group_id: str, *argv, **kwargs):
    
    operation = GraphQLOperation(
        OperationType.QUERY, 
        constants.DUPLICATE_GROUP, 
        *argv, 
        board_id=int(board_id), 
        group_id=group_id, 
        **kwargs)

    result = execute_query(api_key, operation=operation)
    return result[constants.DUPLICATE_GROUP]


def create_group(api_key: str, board_id: str, group_name: str, *argv):

    operation = GraphQLOperation(
        OperationType.QUERY, 
        constants.CREATE_GROUP, 
        *argv, 
        board_id=int(board_id), 
        group_name=group_name)

    result = execute_query(api_key, operation=operation)
    return result[constants.CREATE_GROUP]


def archive_group(api_key: str, board_id: str, group_id: str, *argv):

    operation = GraphQLOperation(
        OperationType.QUERY, 
        constants.ARCHIVE_GROUP, 
        *argv, 
        board_id=int(board_id), 
        group_id=group_id)

    result = execute_query(api_key, operation=operation)
    return result[constants.ARCHIVE_GROUP]


def delete_group(api_key: str, board_id: str, group_id: str, *argv):
    
    operation = GraphQLOperation(
        OperationType.QUERY, 
        constants.DELETE_GROUP, 
        *argv, 
        board_id=int(board_id), 
        group_id=group_id)

    result = execute_query(api_key, operation=operation)
    return result[constants.DELETE_GROUP]

def get_items(api_key: str, *argv, **kwargs):

    operation = GraphQLOperation(
        OperationType.QUERY, 
        constants.ITEMS, 
        *argv, 
        **kwargs)

    result = execute_query(api_key, operation=operation)
    return result[constants.ITEMS]


def get_items_by_column_values(api_key: str, board_id: str, column_id: str, column_value: str, *argv, **kwargs):

    operation = GraphQLOperation(
        OperationType.QUERY, 
        constants.ITEMS_BY_COLUMN_VALUES, 
        *argv,
        board_id=int(board_id), 
        column_id=column_id, 
        column_value=column_value, 
        **kwargs)

    result = execute_query(api_key, operation=operation)
    return result[constants.ITEMS_BY_COLUMN_VALUES]

def create_item(api_key: str, item_name: str, board_id: str, *argv, **kwargs):

    operation = GraphQLOperation(
        OperationType.MUTATION,
        constants.CREATE_ITEM,
        *argv,
        item_name=item_name,
        board_id=int(board_id),
        **kwargs)

    result = execute_query(api_key, operation=operation)
    return result[constants.CREATE_ITEM]
