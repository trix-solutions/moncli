from unittest.mock import patch
from nose.tools import ok_, eq_, raises

import moncli.entities as e
from moncli.enums import ColumnType, BoardKind

USERNAME = 'test.user@foobar.org' 
GET_ME_RETURN_VALUE = e.user.User(**{'creds': None, 'id': '1', 'email': USERNAME})

@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_column')
def test_should_add_new_column(create_column, create_board, get_me):

    # Arrange
    title = 'Text Column 1'
    column_type = ColumnType.text
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    create_column.return_value = {'id': '1', 'title': title, 'type': column_type}
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)

    # Act 
    column = board.add_column(title, column_type)

    # Assert
    ok_(column != None)
    eq_(column.title, title)
    eq_(column.type, column_type)

