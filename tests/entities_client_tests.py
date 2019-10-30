from unittest.mock import patch
from nose.tools import ok_, eq_, raises

from moncli.api_v2 import constants
from moncli.entities import client as c, user as u, exceptions as ex
from moncli.enums import BoardKind

USERNAME = 'test.user@foobar.org' 
GET_ME_RETURN_VALUE = u.User(**{'creds': None, 'id': '1', 'email': USERNAME})

@patch.object(c.MondayClient, 'get_me')
@raises(ex.AuthorizationError)
def test_should_fail_monday_client_authorization(get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE

    # Act
    c.MondayClient('not.my.username@whatever.gov', '', '')


@patch.object(c.MondayClient, 'get_me')
def test_should_create_monday_client(get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE

    # Act
    client = c.MondayClient(USERNAME, '', '')

    # Assert
    ok_(client != None)


@patch('moncli.api_v2.create_board')
@patch.object(c.MondayClient, 'get_me')
def test_should_create_a_new_board(get_me, create_board):

    # Arrange
    board_name = 'New Board 1'
    board_kind = BoardKind.private
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': board_name, 'board_kind': board_kind.name}
    client = c.MondayClient(USERNAME, '', '')

    # Act
    board = client.create_board(board_name, board_kind=board_kind)

    # Assert 
    ok_(board != None)
    eq_(board.name, board_name)
    eq_(board.board_kind, board_kind.name)
