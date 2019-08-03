from moncli.graphql import constants, GraphQLOperation, OperationType, execute_query


def get_board_columns(api_key: str, board_id: str):

    operation = GraphQLOperation(OperationType.QUERY, constants.BOARDS, ids=int(board_id))
    columns = operation.add_fields('columns').get_field(constants.BOARDS + '.columns')
    columns.add_fields('id', 'title', 'type', 'archived', 'settings_str', 'width')

    result = execute_query(api_key, operation=operation)
    return result['boards'][0]['columns']

    

