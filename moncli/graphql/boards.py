from typing import List, Dict, Any

from moncli.constants import BoardKind
from moncli.graphql import constants, GraphQLOperation, OperationType, execute_query

def get_boards(api_key: str, *argv, **kwargs) -> List[Dict[str, Any]]:

    operation = GraphQLOperation(OperationType.QUERY, constants.BOARDS, *argv, **kwargs)

    result = execute_query(api_key, operation=operation)
    return result[constants.BOARDS]


def create_board(api_key: str, board_name: str, board_kind: BoardKind, *argv):

    operation = GraphQLOperation(OperationType.MUTATION, constants.CREATE_BOARD, *argv, board_name=board_name, board_kind=board_kind)

    result = execute_query(api_key, operation=operation)
    return result[constants.CREATE_BOARD]


def archive_board(api_key: str, board_id: str, *argv):

    operation = GraphQLOperation(OperationType.MUTATION, constants.ARCHIVE_BOARD, *argv, board_id=int(board_id))

    result = execute_query(api_key, operation=operation)
    return result[constants.ARCHIVE_BOARD]