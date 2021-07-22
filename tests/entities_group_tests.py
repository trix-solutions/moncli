from unittest.mock import patch
from nose.tools import ok_, eq_

from moncli import client
from moncli.enums import BoardKind


@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_group')
@patch('moncli.api_v2.duplicate_group')
def test_should_duplicate_a_group(duplicate_group, create_group, create_board):

    # Arrange
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    create_group.return_value = {'id': 'group_01', 'title': 'Group 1'}
    duplicate_group.return_value = {'id': 'group_01', 'title': 'Group 1 (copy)'}
    board = client.create_board('Test Board 1', BoardKind.public)
    group = board.add_group('Group 1')

    # Act 
    group = group.duplicate()

    # Assert
    ok_(group != None)
    eq_(group.title, 'Group 1 (copy)')



@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_group')
@patch('moncli.api_v2.archive_group')
def test_should_archive_a_group(archive_group, create_group, create_board):

    # Arrange
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    create_group.return_value = {'id': 'group_01', 'title': 'Group 1'}
    archive_group.return_value = {'id': 'group_01', 'title': 'Group 1', 'archived': 'true'}
    
    board = client.create_board('Test Board 1', BoardKind.public)
    group = board.add_group('Group 1')

    # Act 
    group = group.archive()

    # Assert
    ok_(group != None)
    eq_(group.title, 'Group 1')
    eq_(group.archived, True)



@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_group')
@patch('moncli.api_v2.delete_group')
def test_should_delete_a_group(delete_group, create_group, create_board):

    # Arrange
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    create_group.return_value = {'id': 'group_01', 'title': 'Group 1'}
    delete_group.return_value = {'id': 'group_01', 'title': 'Group 1', 'deleted': 'true'}
    
    board = client.create_board('Test Board 1', BoardKind.public)
    group = board.add_group('Group 1')

    # Act 
    group = group.delete()

    # Assert
    ok_(group != None)
    eq_(group.title, 'Group 1')
    eq_(group.deleted, True)



@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_group')
@patch('moncli.api_v2.create_item')
def test_should_create_an_item(create_item, create_group, create_board):

    # Arrange
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    create_group.return_value = {'id': 'group_01', 'title': 'Group 1'}
    create_item.return_value = {'id': '1', 'name': 'Item 1'}
    
    board = client.create_board('Test Board 1', BoardKind.public)
    group = board.add_group('Group 1')

    # Act 
    item = group.add_item('Item 1')

    # Assert
    ok_(item != None)
    eq_(item.name, 'Item 1')



@patch('moncli.api_v2.create_board')
@patch('moncli.api_v2.create_group')
@patch('moncli.api_v2.get_boards')
@patch('moncli.api_v2.get_items')
def test_should_retrieve_a_list_of_items(get_items, get_boards, create_group, create_board):

    # Arrange
    create_board.return_value = {'id': '1', 'name': 'Test Board 1'}
    create_group.return_value = {'id': 'group_01', 'title': 'Group 1'}
    get_boards.return_value = [
        {'id': '1', 'groups': [
            {'id': 'group_01', 'items':[
                {'id': '1', 'name': 'Item 1'}]}]}]
    
    board = client.create_board('Test Board 1', BoardKind.public)
    group = board.add_group('Group 1')

    # Act 
    items = group.get_items()

    # Assert
    ok_(items != None)
    eq_(len(items), 1)
    eq_(items[0].name, 'Item 1')