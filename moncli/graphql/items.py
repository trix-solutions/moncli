from moncli.constants import State
from moncli.graphql import constants, OperationType, GraphQLOperation, execute_query

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