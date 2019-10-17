from unittest.mock import patch
from nose.tools import ok_

from moncli.api_v2 import handlers, constants

def setup():
    print('SETUP')


def teardown():
    print('TEARDOWN')

@patch('moncli.api_v2.requests.execute_query')
def test_get_board(execute_query):
    print('Test Get Board')
    print('Should return a list of boards')

    execute_query.return_value = {'boards': [{'id': '1'}, {'id': '2'}, {'id': '3'}, {'id': '4'}, {'id': '5'}]}
    boards = handlers.get_boards('', 'id', limit=5)
    
    ok_(len(boards) == 5)

    print('Test Successful!')