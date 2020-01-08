from unittest.mock import patch
from nose.tools import ok_, eq_, raises

from moncli import MondayClient, entities as en
from moncli.enums import BoardKind

USERNAME = 'test.user@foobar.org' 
GET_ME_RETURN_VALUE = en.User(**{'creds': None, 'id': '1', 'email': USERNAME})

@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_group')
@patch('moncli.api_v2.duplicate_group')
def test_should_duplicate_a_group(duplicate_group, create_group, create_board, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    create_group.return_value = {'id': 'group_01', 'title': 'Group 1'}
    duplicate_group.return_value = {'id': 'group_01', 'title': 'Group 1 (copy)'}
    client = MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)
    group = board.add_group('Group 1')

    # Act 
    group = group.duplicate()

    # Assert
    ok_(group != None)
    eq_(group.title, 'Group 1 (copy)')


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_group')
@patch('moncli.api_v2.archive_group')
def test_should_archive_a_group(archive_group, create_group, create_board, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    create_group.return_value = {'id': 'group_01', 'title': 'Group 1'}
    archive_group.return_value = {'id': 'group_01', 'title': 'Group 1', 'archived': 'true'}
    client = MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)
    group = board.add_group('Group 1')

    # Act 
    group = group.archive()

    # Assert
    ok_(group != None)
    eq_(group.title, 'Group 1')
    eq_(group.archived, True)


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_group')
@patch('moncli.api_v2.delete_group')
def test_should_delete_a_group(delete_group, create_group, create_board, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    create_group.return_value = {'id': 'group_01', 'title': 'Group 1'}
    delete_group.return_value = {'id': 'group_01', 'title': 'Group 1', 'deleted': 'true'}
    client = MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)
    group = board.add_group('Group 1')

    # Act 
    group = group.delete()

    # Assert
    ok_(group != None)
    eq_(group.title, 'Group 1')
    eq_(group.deleted, True)


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_group')
@patch('moncli.api_v2.create_item')
def test_should_create_an_item(create_item, create_group, create_board, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    create_group.return_value = {'id': 'group_01', 'title': 'Group 1'}
    create_item.return_value = {'id': '1', 'name': 'Item 1'}
    client = MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)
    group = board.add_group('Group 1')

    # Act 
    item = group.add_item('Item 1')

    # Assert
    ok_(item != None)
    eq_(item.name, 'Item 1')


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_group')
@patch('moncli.api_v2.get_boards')
@patch('moncli.api_v2.get_items')
def test_should_retrieve_a_list_of_items(get_items, get_boards, create_group, create_board, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    create_group.return_value = {'id': 'group_01', 'title': 'Group 1'}
    get_boards.return_value = [
        {'id': '1', 'groups': [
            {'id': 'group_01', 'items':[
                {'id': '1', 'name': 'Item 1'}]}]}]
    client = MondayClient(USERNAME, '', '')
    board = client.create_board('Test Board 1', BoardKind.public)
    group = board.add_group('Group 1')

    # Act 
    items = group.get_items()

    # Assert
    ok_(items != None)
    eq_(len(items), 1)
    eq_(items[0].name, 'Item 1')