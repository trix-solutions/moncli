from unittest.mock import patch
from nose.tools import ok_

from moncli.api_v2 import handlers, constants
from moncli.enums import BoardKind, ColumnType

EXECUTE_QUERY_PATCH = 'moncli.api_v2.requests.execute_query'

def setup():
    print('SETUP')


def teardown():
    print('TEARDOWN')

@patch(EXECUTE_QUERY_PATCH)
def test_create_board(execute_query):

    # Arrange
    execute_query.return_value = {constants.CREATE_BOARD: {'id': '1', 'name': 'Test', 'board_kind': 'public'}}

    # Act
    board = handlers.create_board('', 'Test', BoardKind.public, 'id', 'name', 'board_kind')
    
    # Assert
    ok_(board != None)
    ok_(board['name'] == 'Test')
    ok_(board['board_kind'] == 'public')


@patch(EXECUTE_QUERY_PATCH)
def test_get_board(execute_query):

    # Arrange
    execute_query.return_value = {constants.BOARDS: [{'id': '1'}, {'id': '2'}, {'id': '3'}, {'id': '4'}, {'id': '5'}]}

    # Act
    boards = handlers.get_boards('', 'id', limit=5)
    
    # Assert
    ok_(len(boards) == 5)


@patch(EXECUTE_QUERY_PATCH)
def test_archive_board(execute_query):

    # Arrange
    execute_query.return_value = {constants.ARCHIVE_BOARD: {'id': '1', 'state': 'archived'}}

    # Act
    archived_board = handlers.archive_board('', '1', 'id', 'state')
    
    # Assert
    ok_(archived_board != None)
    ok_(archived_board['state'] == 'archived')


@patch(EXECUTE_QUERY_PATCH)
def test_create_column(execute_query):

    # Arrange
    title = 'Text Column One'
    execute_query.return_value = {constants.CREATE_COLUMN: {'id': 'text_column_1', 'title': title, 'type': 'text'}}

    # Act
    new_column = handlers.create_column('', '1', title, ColumnType.text, 'id', 'title', 'type')
    
    # Assert
    ok_(new_column != None)
    ok_(new_column['title'] == title)
    ok_(new_column['type'] == ColumnType.text.name)


@patch(EXECUTE_QUERY_PATCH)
def test_change_column_value(execute_query):

    # Arrange
    execute_query.return_value = {constants.CHANGE_COLUMN_VALUE: {'id': '1'}}

    # Act
    updated_item = handlers.change_column_value('', '1', 'text_column_1', '1', 'Hello, world!', 'id')
    
    # Assert
    ok_(updated_item != None)
    ok_(updated_item['id'] == '1')


@patch(EXECUTE_QUERY_PATCH)
def test_change_multiple_column_value(execute_query):

    # Arrange
    column_values = {'text_column_1': 'Let\'s eat, Grandma!', 'numbers_column_1': 8675309}
    execute_query.return_value = {constants.CHANGE_MULTIPLE_COLUMN_VALUES: {'id': '1'}}

    # Act
    updated_item = handlers.change_multiple_column_value('', '1', '1', column_values, 'id')
    
    # Assert
    ok_(updated_item != None)
    ok_(updated_item['id'] == '1')


@patch(EXECUTE_QUERY_PATCH)
def test_duplicate_group(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass


@patch(EXECUTE_QUERY_PATCH)
def test_create_group(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass


@patch(EXECUTE_QUERY_PATCH)
def test_archive_group(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass


@patch(EXECUTE_QUERY_PATCH)
def test_delete_group(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass


@patch(EXECUTE_QUERY_PATCH)
def test_create_item(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass


@patch(EXECUTE_QUERY_PATCH)
def test_get_items(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass


@patch(EXECUTE_QUERY_PATCH)
def test_get_items_by_column_values(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass


@patch(EXECUTE_QUERY_PATCH)
def test_archive_item(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass


@patch(EXECUTE_QUERY_PATCH)
def test_delete_item(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass


@patch(EXECUTE_QUERY_PATCH)
def test_create_update(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass


@patch(EXECUTE_QUERY_PATCH)
def test_get_updates(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass


@patch(EXECUTE_QUERY_PATCH)
def test_create_notification(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass


@patch(EXECUTE_QUERY_PATCH)
def test_create_or_get_tag(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass


@patch(EXECUTE_QUERY_PATCH)
def test_get_tags(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass


@patch(EXECUTE_QUERY_PATCH)
def test_get_users(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass


@patch(EXECUTE_QUERY_PATCH)
def test_get_teams(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass


@patch(EXECUTE_QUERY_PATCH)
def test_get_me(execute_query):

    # Arrange

    # Act
    
    # Assert
    pass