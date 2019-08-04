from moncli.constants import State
from moncli.graphql import constants, OperationType, GraphQLOperation, execute_query

def get_items(api_key: str, **kwargs):

    operation = GraphQLOperation(OperationType.QUERY, constants.ITEMS, **kwargs)
    operation.add_fields('board', 'column_values', 'creator_id', 'group', 'id', 'name', 'updates')
    operation.get_field(constants.ITEMS + '.board').add_fields('id')
    operation.get_field(constants.ITEMS + '.group').add_fields('id')
    operation.get_field(constants.ITEMS + '.column_values').add_fields('id', 'text', 'title', 'value', 'additional_info')
    operation.get_field(constants.ITEMS + '.updates').add_fields('id')

    result = execute_query(api_key, operation=operation)
    return result[constants.ITEMS]

def get_items_by_column_values(api_key: str, board_id: str, column_id: str, column_value: str, **kwargs):

    operation = GraphQLOperation(
        OperationType.QUERY, 
        constants.ITEMS_BY_COLUMN_VALUES, 
        board_id=int(board_id), 
        column_id=column_id, 
        column_value=column_value, 
        **kwargs)
    operation.add_fields('column_values', 'creator_id', 'group', 'id', 'name', 'updates')
    operation.get_field(constants.ITEMS_BY_COLUMN_VALUES + '.group').add_fields('id')
    operation.get_field(constants.ITEMS_BY_COLUMN_VALUES + '.column_values').add_fields('id', 'text', 'title', 'value', 'additional_info')
    operation.get_field(constants.ITEMS_BY_COLUMN_VALUES + '.updates').add_fields('id')

    result = execute_query(api_key, operation=operation)
    return result[constants.ITEMS_BY_COLUMN_VALUES]