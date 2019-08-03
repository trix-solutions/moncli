from moncli.constants import BoardKind
from moncli.graphql import constants, GraphQLOperation, OperationType, execute_query

def get_boards(api_key: str, **kwargs):

    operation = GraphQLOperation(OperationType.QUERY, constants.BOARDS, **kwargs)
    operation.add_fields('id', 'name')

    result = execute_query(api_key, operation=operation)
    return result[constants.BOARDS]


def create_board(api_key: str, board_name: str, board_kind: BoardKind):

    operation = GraphQLOperation(OperationType.MUTATION, constants.CREATE_BOARD, board_name=board_name, board_kind=board_kind)
    operation.add_fields('id', 'name')

    result = execute_query(api_key, operation=operation)
    return result[constants.CREATE_BOARD]


def archive_board(api_key: str, board_id: str):

    operation = GraphQLOperation(OperationType.MUTATION, constants.ARCHIVE_BOARD, board_id=int(board_id))
    operation.add_fields('id', 'state')

    result = execute_query(api_key, operation=operation)
    return result[constants.ARCHIVE_BOARD]