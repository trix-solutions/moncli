from unittest.mock import patch
from nose.tools import ok_

from moncli.api_v2 import handlers, constants
from moncli.enums import BoardKind

EXECUTE_QUERY_PATCH = 'moncli.api_v2.requests.execute_query'

def setup():
    print('SETUP')


def teardown():
    print('TEARDOWN')

@patch(EXECUTE_QUERY_PATCH)
def test_create_board(execute_query):

    # Mock setup
    execute_query.return_value = {constants.CREATE_BOARD: {'id': '1', 'name': 'Test', 'board_kind': 'public'}}

    # Act
    board = handlers.create_board('', 'Test', BoardKind.public, 'id', 'name', 'board_kind')
    
    # Assert
    ok_(board != None)
    ok_(board['name'] == 'Test')
    ok_(board['board_kind'] == 'public')


@patch(EXECUTE_QUERY_PATCH)
def test_get_board(execute_query):

    # Mock setup
    execute_query.return_value = {constants.BOARDS: [{'id': '1'}, {'id': '2'}, {'id': '3'}, {'id': '4'}, {'id': '5'}]}

    # Act
    boards = handlers.get_boards('', 'id', limit=5)
    
    # Assert
    ok_(len(boards) == 5)