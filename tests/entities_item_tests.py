import json

from unittest.mock import patch
from nose.tools import ok_, eq_, raises

from moncli import MondayClient, entities as en
from moncli.entities import column_value as cv
from moncli.enums import ColumnType, BoardKind

USERNAME = 'test.user@foobar.org' 
GET_ME_RETURN_VALUE = en.User(**{'creds': None, 'id': '1', 'email': USERNAME})

@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch.object(en.Item, 'get_board')
@patch.object(en.Board, 'get_columns')
def test_item_should_get_column_values(get_columns, get_board, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    get_board.return_value = en.Board(**{'id': '1', 'name': 'Test Board 1'})
    get_columns.return_value = [en.Column({'id': 'text_column_01', 'type': 'text'})]
    get_items.return_value = [{'id': '1', 'column_values': [{'id': 'text_column_01', 'title': 'Text Column 01', 'value': json.dumps('Hello, Grandma')}]}]

    # Act
    column_values = item.get_column_values()

    # Assert 
    ok_(column_values != None)
    eq_(len(column_values), 1)
    eq_(column_values[0].title, 'Text Column 01')
    eq_(column_values[0].text_value, 'Hello, Grandma')


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch.object(en.Item, 'get_board')
@patch.object(en.Board, 'get_columns')
def test_item_should_get_column_values_for_status_column(get_columns, get_board, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    get_board.return_value = en.Board(**{'id': '1', 'name': 'Test Board 1'})
    get_columns.return_value = [en.Column({'id': 'status_column_01', 'type': 'color', 'settings_str': json.dumps({'labels': {'1': 'Test'}})})]
    get_items.return_value = [{'id': '1', 'column_values': [{'id': 'status_column_01', 'title': 'Status Column 01', 'value': json.dumps({'index': 1})}]}]

    # Act
    column_values = item.get_column_values()

    # Assert 
    ok_(column_values != None)
    eq_(len(column_values), 1)
    eq_(column_values[0].title, 'Status Column 01')
    eq_(column_values[0].index, 1)


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@raises(en.board.NotEnoughGetColumnValueParameters)
def test_item_should_fail_to_retrieve_column_value_from_too_few_parameters(get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    item.get_column_value()


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@raises(en.board.TooManyGetColumnValueParameters)
def test_item_should_fail_to_retrieve_column_value_from_too_many_parameters(get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    item.get_column_value(id='text_column_01', title='Text Column 01')


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch.object(en.Item, 'get_column_values')
def test_item_should_get_column_value_by_id(get_column_values, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    get_column_values.return_value = [cv.TextValue(**{'id': 'text_column_01', 'title': 'Text Column 01', 'text': 'Hello, Grandma', 'value': json.dumps('Hello, Grandma')})]
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    column_value = item.get_column_value(id='text_column_01')

    # Assert 
    ok_(column_value != None)
    eq_(column_value.title, 'Text Column 01')
    eq_(column_value.text, 'Hello, Grandma')
    eq_(type(column_value), cv.TextValue)


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch.object(en.Item, 'get_column_values')
def test_item_should_get_column_value_by_title(get_column_values, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    get_column_values.return_value = [cv.TextValue(**{'id': 'text_column_01', 'title': 'Text Column 01', 'text': 'Hello, Grandma', 'value': json.dumps('Hello, Grandma')})]
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    column_value = item.get_column_value(title='Text Column 01')

    # Assert 
    ok_(column_value != None)
    eq_(column_value.title, 'Text Column 01')
    eq_(column_value.text, 'Hello, Grandma')
    eq_(type(column_value), cv.TextValue)


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch.object(en.Item, 'get_column_values')
def test_item_should_get_column_value_with_extra_id(get_column_values, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    get_column_values.return_value = [cv.LongTextValue(**{
        'id': 'text_column_01', 
        'title': 'Text Column 01', 
        'text': 'Hello, Grandma', 
        'value': json.dumps({'id': '1', 'text': 'Hello, Grandma'})})
    ]

    # Act
    column_value = item.get_column_value(title='Text Column 01')

    # Assert 
    ok_(column_value != None)
    eq_(column_value.title, 'Text Column 01')
    eq_(column_value.long_text, 'Hello, Grandma')
    eq_(type(column_value), cv.LongTextValue)


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch.object(en.Item, 'get_board')
@raises(en.InvalidColumnValue)
def test_item_should_fail_to_update_column_value_with_invalid_column_value(get_board, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    get_board.return_value = en.Board(creds=None, id='1', name='Test Board 1')
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    item.change_column_value(column_value='5')


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@raises(en.InvalidColumnValue)
def test_item_should_fail_to_update_column_value_with_invalid_column_value_with_id(get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    item.change_column_value(column_id='text_column_01', column_value=[1,2,3,4,5])


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch.object(en.Item, 'get_board')
@patch('moncli.api_v2.change_multiple_column_value')
def test_item_should_change_multiple_column_values_with_dictionary(change_multiple_column_value, get_board, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    get_board.return_value = en.Board(**{'id': '1', 'name': 'Test Board 1'})
    change_multiple_column_value.return_value = {'id': '1', 'name': 'Test Item 01'}
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    item = item.change_multiple_column_values({'text_column_01': 'Hello, world!'})

    # Assert 
    ok_(item != None)
    eq_(item.name, 'Test Item 01')


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch.object(en.Item, 'get_board')
@patch('moncli.api_v2.change_multiple_column_value')
def test_item_should_change_multiple_column_values_with_column_value_list(change_multiple_column_value, get_board, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    get_board.return_value = en.Board(id='1', name='Test Board 01')
    change_multiple_column_value.return_value = {'id': '1', 'name': 'Test Item 01'}
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    column_value = cv.create_column_value(ColumnType.text, id='text_column_01', title='Text Column 01', text='Hello, world!', value=json.dumps('Hello, world!'))
    item = item.change_multiple_column_values([column_value])

    # Assert 
    ok_(item != None)
    eq_(item.name, 'Test Item 01')


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.move_item_to_group')
def test_item_should_move_item_to_group(move_item_to_group, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    move_item_to_group.return_value = {'id': '1', 'name': 'Test Item 01'}
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    item = item.move_to_group('group_01')

    # Assert 
    ok_(item != None)
    eq_(item.name, 'Test Item 01')


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.archive_item')
def test_item_should_archive_item(archive_item, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    archive_item.return_value = {'id': '1', 'name': 'Test Item 01'}
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    item = item.archive()

    # Assert 
    ok_(item != None)
    eq_(item.name, 'Test Item 01')


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.delete_item')
def test_item_should_delete_item(delete_item, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    delete_item.return_value = {'id': '1', 'name': 'Test Item 01'}
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    item = item.delete()

    # Assert 
    ok_(item != None)
    eq_(item.name, 'Test Item 01')


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.create_update')
def test_item_should_add_update(create_update, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    create_update.return_value = {'id': '1', 'body': 'This is a text body'}
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    update = item.add_update('This is a text body')

    # Assert 
    ok_(update != None)
    eq_(update.body, 'This is a text body')


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
def test_item_should_get_list_of_item_updates(get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]
    get_items.return_value = [{'id': '1', 'updates':[{'id': '2', 'item_id': '1', 'creator_id': '1', 'replies': [{'id': '3', 'creator_id': '1'}]}]}]

    # Act
    updates = item.get_updates()

    # Assert 
    ok_(updates != None)
    eq_(len(updates), 1)
    eq_(updates[0].to_primitive(), item.updates[0].to_primitive())
    eq_(len(updates[0].replies), 1)


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.add_file_to_column')
def test_item_should_add_file(add_file_to_column, get_items, get_me):
    
    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}]
    add_file_to_column.return_value = {'id': '12345', 'name': '33.jpg', 'url': 'https://test.monday.com/12345/33.jpg'}
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]
    file_column = cv.create_column_value(ColumnType.file, id='files', title='Files')

    # Act
    asset = item.add_file(file_column, '/Users/test/33.jpg')

    # Assert 
    ok_(asset != None)
    eq_(asset.id, '12345')
    eq_(asset.name, '33.jpg')
    eq_(asset.url, 'https://test.monday.com/12345/33.jpg')


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
def test_item_should_get_files(get_items, get_me):
    
    # Arrange
    asset_id = '12345'
    name = '33.jpg'
    url = 'https://test.monday.com/12345/33.jpg'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}]
    
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    get_items.return_value = [{'id': '1','assets': [{'id': asset_id, 'name': name, 'url': url}]}]

    # Act
    assets = item.get_files()

    # Assert 
    ok_(assets != None)
    eq_(assets[0].id, '12345')
    eq_(assets[0].name, '33.jpg')
    eq_(assets[0].url, 'https://test.monday.com/12345/33.jpg')


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.change_column_value')
def test_item_should_remove_files(change_column_value, get_items, get_me):
    
    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}]
    change_column_value.return_value = get_items.return_value[0]
    client = MondayClient(USERNAME, '', '')
    item = client.get_items()[0]
    file_column = cv.create_column_value(ColumnType.file, id='files', title='Files')

    # Act
    item = item.remove_files(file_column)

    # Assert 
    ok_(item != None)
    eq_(item.id, '1')
    eq_(item.name, 'Test Item 01')
    eq_(item.board.id, '1')