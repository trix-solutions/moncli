from unittest.mock import patch
from nose.tools import ok_, eq_, raises

import moncli.entities as e
from moncli.enums import BoardKind

USERNAME = 'test.user@foobar.org' 
GET_ME_RETURN_VALUE = e.user.User(**{'creds': None, 'id': '1', 'email': USERNAME})

@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_group')
@patch('moncli.api_v2.duplicate_group')
def test_should_duplicate_a_group(duplicate_group, create_group, create_board, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    create_group.return_value = {'id': 'group_01', 'title': 'Group 1'}
    duplicate_group.return_value = {'id': 'group_01', 'title': 'Group 1 (copy)'}
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)
    group = board.add_group('Group 1')

    # Act 
    group = group.duplicate()

    # Assert
    ok_(group != None)
    eq_(group.title, 'Group 1 (copy)')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_group')
@patch('moncli.api_v2.archive_group')
def test_should_archive_a_group(archive_group, create_group, create_board, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    create_group.return_value = {'id': 'group_01', 'title': 'Group 1'}
    archive_group.return_value = {'id': 'group_01', 'title': 'Group 1', 'archived': 'true'}
    client = e.client.MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)
    group = board.add_group('Group 1')

    # Act 
    group = group.archive()

    # Assert
    ok_(group != None)
    eq_(group.title, 'Group 1')
    eq_(group.archived, 'true')