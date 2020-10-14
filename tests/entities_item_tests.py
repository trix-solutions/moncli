import json
from unittest.mock import patch
from nose.tools import ok_, eq_, raises

import moncli.columnvalue as cv
import moncli.entities as e
from moncli.enums import ColumnType, BoardKind

USERNAME = 'test.user@foobar.org' 
GET_ME_RETURN_VALUE = e.user.User(**{'creds': None, 'id': '1', 'email': USERNAME})

@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.get_boards')
def test_item_should_get_column_values(get_boards, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1', 'board': {'id': '1'}}]
    get_boards.return_value = [{'id': '1', 'columns': [{'id': 'text_column_01', 'type': 'text'}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    get_items.return_value = [{'id': '1', 'column_values': [{'id': 'text_column_01', 'title': 'Text Column 01', 'text': 'Hello, Grandma', 'value': json.dumps('Hello, Grandma')}]}]

    # Act
    column_values = item.get_column_values()

    # Assert 
    ok_(column_values != None)
    eq_(len(column_values), 1)
    eq_(column_values[0].title, 'Text Column 01')
    eq_(column_values[0].text, 'Hello, Grandma')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.get_boards')
def test_item_should_get_column_values_for_status_column(get_boards, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1', 'board': {'id': '1'}}]
    get_boards.return_value = [{'id': '1', 'columns': [{'id': 'status_column_01', 'type': 'color', 'settings_str': json.dumps({'labels': {'1': 'Test'}})}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    get_items.return_value = [{'id': '1', 'column_values': [{'id': 'status_column_01', 'title': 'Status Column 01', 'text': 'Test', 'value': json.dumps({'index': 1})}]}]

    # Act
    column_values = item.get_column_values()

    # Assert 
    ok_(column_values != None)
    eq_(len(column_values), 1)
    eq_(column_values[0].title, 'Status Column 01')
    eq_(column_values[0].index, 1)
    eq_(column_values[0].text, 'Test')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.get_boards')
@raises(e.exceptions.NotEnoughGetColumnValueParameters)
def test_item_should_fail_to_retrieve_column_value_from_too_few_parameters(get_boards, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1', 'board': {'id': '1'}}]
    get_boards.return_value = [{'id': '1', 'columns': [{'id': 'text_column_01', 'type': 'text'}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    get_items.return_value = [{'id': '1', 'column_values': [{'id': 'text_column_01', 'title': 'Text Column 01', 'text': 'Hello, Grandma', 'value': json.dumps('Hello, Grandma')}]}]

    # Act
    item.get_column_value()


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.get_boards')
@raises(e.exceptions.TooManyGetColumnValueParameters)
def test_item_should_fail_to_retrieve_column_value_from_too_many_parameters(get_boards, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1', 'board': {'id': '1'}}]
    get_boards.return_value = [{'id': '1', 'columns': [{'id': 'text_column_01', 'type': 'text'}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    get_items.return_value = [{'id': '1', 'column_values': [{'id': 'text_column_01', 'title': 'Text Column 01', 'text': 'Hello, Grandma', 'value': json.dumps('Hello, Grandma')}]}]

    # Act
    item.get_column_value(id='text_column_01', title='Text Column 01')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.get_boards')
def test_item_should_get_column_value_by_id(get_boards, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1', 'board': {'id': '1'}}]
    get_boards.return_value = [{'id': '1', 'columns': [{'id': 'text_column_01', 'type': 'text'}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    get_items.return_value = [{'id': '1', 'column_values': [{'id': 'text_column_01', 'title': 'Text Column 01', 'text': 'Hello, Grandma', 'value': json.dumps('Hello, Grandma')}]}]

    # Act
    column_value = item.get_column_value(id='text_column_01')

    # Assert 
    ok_(column_value != None)
    eq_(column_value.title, 'Text Column 01')
    eq_(column_value.text, 'Hello, Grandma')
    eq_(type(column_value), cv.TextValue)


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.get_boards')
def test_item_should_get_column_value_by_title(get_boards, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1', 'board': {'id': '1'}}]
    get_boards.return_value = [{'id': '1', 'columns': [{'id': 'text_column_01', 'type': 'text'}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    get_items.return_value = [{'id': '1', 'column_values': [{'id': 'text_column_01', 'title': 'Text Column 01', 'text': 'Hello, Grandma', 'value': json.dumps('Hello, Grandma')}]}]

    # Act
    column_value = item.get_column_value(title='Text Column 01')

    # Assert 
    ok_(column_value != None)
    eq_(column_value.title, 'Text Column 01')
    eq_(column_value.text, 'Hello, Grandma')
    eq_(type(column_value), cv.TextValue)


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.get_boards')
def test_item_should_get_column_value_with_extra_id(get_boards, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1', 'board': {'id': '1'}}]
    get_boards.return_value = [{'id': '1', 'columns': [{'id': 'text_column_01', 'type': 'long-text'}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    get_items.return_value = [{'id': '1', 'column_values': [{'id': 'text_column_01', 'title': 'Text Column 01', 'text': 'Hello, Grandma', 'value': json.dumps({'id': '1', 'text': 'Hello, Grandma'})}]}]

    # Act
    column_value = item.get_column_value(title='Text Column 01')

    # Assert 
    ok_(column_value != None)
    eq_(column_value.title, 'Text Column 01')
    eq_(column_value.text, 'Hello, Grandma')
    eq_(type(column_value), cv.LongTextValue)


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@raises(e.exceptions.InvalidColumnValue)
def test_item_should_fail_to_update_column_value_with_invalid_column_value(get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1', 'board': {'id': '1'}}]
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    item.change_column_value(column_value='5')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@raises(e.exceptions.InvalidColumnValue)
def test_item_should_fail_to_update_column_value_with_invalid_column_value_with_id(get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1', 'board': {'id': '1'}}]
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    item.change_column_value(column_id='text_column_01', column_value=[1,2,3,4,5])


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.change_column_value')
def test_item_should_change_column_value_with_string(change_column_value, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}]
    change_column_value.return_value = {'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    item = item.change_column_value(column_id='text_column_01', column_value='Let\'s eat grandma!')

    # Assert 
    ok_(item != None)
    eq_(item.name, 'Test Item 01')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.change_multiple_column_value')
def test_item_should_change_multiple_column_values_with_dictionary(change_multiple_column_value, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}]
    change_multiple_column_value.return_value = {'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    item = item.change_multiple_column_values({'text_column_01': 'Hello, world!'})

    # Assert 
    ok_(item != None)
    eq_(item.name, 'Test Item 01')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.change_multiple_column_value')
def test_item_should_change_multiple_column_values_with_column_value_list(change_multiple_column_value, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}]
    change_multiple_column_value.return_value = {'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    column_value = cv.create_column_value(id='text_column_01', column_type=ColumnType.text, value='Hello, world!')
    item = item.change_multiple_column_values([column_value])

    # Assert 
    ok_(item != None)
    eq_(item.name, 'Test Item 01')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.move_item_to_group')
def test_item_should_move_item_to_group(move_item_to_group, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}]
    move_item_to_group.return_value = {'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    item = item.move_to_group('group_01')

    # Assert 
    ok_(item != None)
    eq_(item.name, 'Test Item 01')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.archive_item')
def test_item_should_archive_item(archive_item, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}]
    archive_item.return_value = {'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    item = item.archive()

    # Assert 
    ok_(item != None)
    eq_(item.name, 'Test Item 01')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.delete_item')
def test_item_should_delete_item(delete_item, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}]
    delete_item.return_value = {'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    item = item.delete()

    # Assert 
    ok_(item != None)
    eq_(item.name, 'Test Item 01')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.create_update')
def test_item_should_add_update(create_update, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}]
    create_update.return_value = {'id': '1', 'body': 'This is a text body'}
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    # Act
    update = item.add_update('This is a text body')

    # Assert 
    ok_(update != None)
    eq_(update.body, 'This is a text body')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.add_file_to_column')
def test_item_should_add_file(add_file_to_column, get_items, get_me):
    
    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}]
    add_file_to_column.return_value = {'id': '12345', 'name': '33.jpg', 'url': 'https://test.monday.com/12345/33.jpg'}
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]
    file_column = cv.create_column_value('files', ColumnType.file, 'Files', files=[])

    # Act
    asset = item.add_file(file_column, '/Users/test/33.jpg')

    # Assert 
    ok_(asset != None)
    eq_(asset.id, '12345')
    eq_(asset.name, '33.jpg')
    eq_(asset.url, 'https://test.monday.com/12345/33.jpg')