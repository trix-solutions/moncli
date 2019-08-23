from moncli.graphql import constants, GraphQLOperation, OperationType, execute_query

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