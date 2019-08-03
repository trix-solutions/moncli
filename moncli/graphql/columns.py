from moncli.constants import ColumnType
from moncli.graphql import constants, GraphQLOperation, OperationType, execute_query


def get_board_columns(api_key: str, board_id: str):

    operation = GraphQLOperation(OperationType.QUERY, constants.BOARDS, ids=int(board_id))
    columns = operation.add_fields('columns').get_field(constants.BOARDS + '.columns')
    columns.add_fields('id', 'title', 'type', 'archived', 'settings_str', 'width')

    result = execute_query(api_key, operation=operation)
    return result[constants.BOARDS][0]['columns']

    
def create_column(api_key: str, board_id: str, title: str, column_type: ColumnType):

    operation = GraphQLOperation(OperationType.MUTATION, constants.CREATE_COLUMN, board_id=int(board_id), title=title, column_type=column_type)
    operation.add_fields('id')

    result = execute_query(api_key, operation=operation)
    return result[constants.CREATE_COLUMN]
