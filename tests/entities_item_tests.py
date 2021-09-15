import json
from moncli.api_v2.handlers import get_boards

from unittest.mock import patch
from nose.tools import ok_, eq_, raises

from moncli import client, entities as en
from moncli.entities import column_value as cv
from moncli.enums import ColumnType

@patch('moncli.api_v2.get_items')
def test_item_should_get_board(get_items):

    # Arrange
    id = '12345'
    name = 'Test Board 1'
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    item = client.get_items()[0]
    get_items.return_value = [{'id': '1', 'board': {'id': '1'}, 'board': {'id': id, 'name': name}}]

    # Act
    board = item.get_board()

    # Assert 
    ok_(board != None)
    eq_(board.id, id)
    eq_(board.name, name)


@patch('moncli.api_v2.get_items')
def test_item_should_get_group(get_items):

    # Arrange
    id = 'group_1'
    title = 'Test Group 1'
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    item = client.get_items()[0]
    get_items.return_value = [{'id': '1', 'board': {'id': '1'}, 'group': {'id': id, 'title': title}}]

    # Act
    group = item.get_group()

    # Assert 
    ok_(group != None)
    eq_(group.id, id)
    eq_(group.title, title)

@patch('moncli.api_v2.get_items')
@patch.object(en.Item, 'get_board')
@patch.object(en.Board, 'get_columns')
def test_item_should_get_column_values(get_columns, get_board, get_items):

    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
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


@patch('moncli.api_v2.get_items')
@patch.object(en.Item, 'get_board')
@patch.object(en.Board, 'get_columns')
def test_item_should_get_column_values_for_default_status_column(get_columns, get_board, get_items):

    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    item = client.get_items()[0]
    get_board.return_value = en.Board(**{'id': '1', 'name': 'Test Board 1'})
    get_columns.return_value = [en.Column({'id': 'status_column_01', 'type': 'color', 'settings_str': json.dumps({'labels': {'1': 'Test'}})})]
    get_items.return_value = [{'id': '1', 'column_values': [{'id': 'status_column_01', 'title': 'Status Column 01', 'text': 'Test', 'additional_info': None, 'value': None}]}]

    # Act
    column_values = item.get_column_values()

    # Assert 
    ok_(column_values != None)
    eq_(len(column_values), 1)
    eq_(column_values[0].title, 'Status Column 01')
    eq_(column_values[0].index, None)
    eq_(column_values[0].label, 'Test')


@patch('moncli.api_v2.get_items')
@patch.object(en.Item, 'get_board')
@patch.object(en.Board, 'get_columns')
def test_item_should_get_column_values_for_status_column(get_columns, get_board, get_items):

    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    item = client.get_items()[0]
    get_board.return_value = en.Board(**{'id': '1', 'name': 'Test Board 1'})
    get_columns.return_value = [en.Column({'id': 'status_column_01', 'type': 'color', 'settings_str': json.dumps({'labels': {'1': 'Test'}})})]
    get_items.return_value = [{'id': '1', 'column_values': [{'id': 'status_column_01', 'title': 'Status Column 01', 'text': 'Test', 'additional_info': json.dumps({'label': 'Test'}), 'value': json.dumps({'index': 1})}]}]

    # Act
    column_values = item.get_column_values()

    # Assert 
    ok_(column_values != None)
    eq_(len(column_values), 1)
    eq_(column_values[0].title, 'Status Column 01')
    eq_(column_values[0].index, 1)
    eq_(column_values[0].label, 'Test')


@patch('moncli.api_v2.get_items')
@raises(en.board.NotEnoughGetColumnValueParameters)
def test_item_should_fail_to_retrieve_column_value_from_too_few_parameters(get_items):

    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    item = client.get_items()[0]

    # Act
    item.get_column_value()


@patch('moncli.api_v2.get_items')
@raises(en.board.TooManyGetColumnValueParameters)
def test_item_should_fail_to_retrieve_column_value_from_too_many_parameters(get_items):

    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    item = client.get_items()[0]

    # Act
    item.get_column_value(id='text_column_01', title='Text Column 01')



@patch('moncli.api_v2.get_items')
def test_item_should_get_column_value_by_id(get_items):

    # Arrange
    column_id = 'text_column_01'
    column_title = 'Text Column 01'
    text_value = 'Hello, Grandma!'
    column_value = cv.create_column_value(ColumnType.text, **{'id': column_id, 'title': column_title, 'text': text_value, 'value': json.dumps(text_value)})
    column = en.Column({'id': column_id, 'title': column_title, 'type': 'text'})
    board = en.Board(id='1', name='Test Board 1', columns=[column.to_primitive()])
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1', 'board': board.to_primitive(), 'column_values': [column_value.to_primitive()]}]
    item = client.get_items()[0]

    # Act
    column_value = item.get_column_value(id='text_column_01')

    # Assert 
    ok_(column_value != None)
    eq_(column_value.title, column_title)
    eq_(column_value.text, text_value)
    eq_(type(column_value), cv.TextValue)


@patch('moncli.api_v2.get_items')
def test_item_should_get_column_value_by_title(get_items):

    # Arrange 
    column_id = 'text_column_01'
    column_title = 'Text Column 01'
    text_value = 'Gello, Hrandma!'
    column_value = cv.create_column_value(ColumnType.text, **{'id': column_id, 'title': column_title, 'text': text_value, 'value': json.dumps(text_value)})
    column = en.Column({'id': column_id, 'title': column_title, 'type': 'text'})
    board = en.Board(id='1', name='Test Board 1', columns=[column.to_primitive()])
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1', 'board': board.to_primitive(), 'column_values': [column_value.to_primitive()]}]
    item = client.get_items()[0]

    # Act
    column_value = item.get_column_value(title=column_title)

    # Assert 
    ok_(column_value != None)
    eq_(column_value.title, column_title)
    eq_(column_value.text, text_value)
    eq_(type(column_value), cv.TextValue)


@patch('moncli.api_v2.get_items')
@patch.object(en.Item, 'get_column_values')
def test_item_should_get_column_value_with_extra_id(get_column_values, get_items):

    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    item = client.get_items()[0]
    get_column_values.return_value = en.BaseColumnCollection([cv.LongTextValue(**{
        'id': 'text_column_01', 
        'title': 'Text Column 01', 
        'text': 'Hello, Grandma', 
        'value': json.dumps({'id': '1', 'text': 'Hello, Grandma'})})
    ])

    # Act
    column_value = item.get_column_value(title='Text Column 01')

    # Assert 
    ok_(column_value != None)
    eq_(column_value.title, 'Text Column 01')
    eq_(column_value.long_text, 'Hello, Grandma')
    eq_(type(column_value), cv.LongTextValue)


@patch('moncli.api_v2.get_items')
@patch.object(en.Item, 'get_board')
@raises(en.InvalidColumnValue)
def test_item_should_fail_to_update_column_value_with_invalid_column_value(get_board, get_items):

    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    get_board.return_value = en.Board(creds=None, id='1', name='Test Board 1')
    item = client.get_items()[0]

    # Act
    item.change_column_value(column_value='5')


@patch('moncli.api_v2.get_items')
@raises(en.InvalidColumnValue)
def test_item_should_fail_to_update_column_value_with_invalid_column_value_with_id(get_items):

    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    item = client.get_items()[0]

    # Act
    item.change_column_value(column_value=[1,2,3,4,5])


@patch('moncli.api_v2.get_items')
@raises(en.item.TooManyChangeSimpleColumnValueParameters)
def test_should_fail_to_change_simple_column_value_with_too_many_parameters(get_items):
    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    
    item = client.get_items()[0]
    id = "long_text"
    title = "mock title"

    # Act 

    item.change_simple_column_value(id,title,value="change value")


@patch('moncli.api_v2.get_items')
@raises(en.item.NotEnoughChangeSimpleColumnValueParameters)
def test_should_fail_to_change_column_value_from_too_few_parameters( get_items):
    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    item = client.get_items()[0]
    

    # Act 

    item.change_simple_column_value(value="change value")


@patch('moncli.api_v2.get_items')
@patch.object(en.Item,'get_board')
@patch.object(en.Item, 'get_column_values')
@patch('moncli.api_v2.change_simple_column_value')
def test_should_update_simple_column_value(change_simple_column_value, get_column_values,get_board, get_items):
    
    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    get_board.return_value = en.Board(**{'id': '1', 'name': 'Test Board 1'})
    column_value = cv.create_column_value(
        ColumnType.long_text, 
        id= 'long_text', 
        title= 'Description', 
        text= "My previous keyword doesn't work", 
        value= 'My previous keyword' )
    get_column_values.return_value = en.BaseColumnCollection([column_value])
    item = client.get_items()[0]
    change_simple_column_value.return_value = {'id': '1', 'name': 'Test Item 01'}

    # Act
    item = item.change_simple_column_value(id=column_value.id,title=None,value="new value")
    
    # Assert 
    ok_(item != None)
    eq_(item.id, '1'),
    eq_(item.name, 'Test Item 01')

    
@patch('moncli.api_v2.get_items')
@patch.object(en.Item, 'get_board')
@patch.object(en.Item, 'get_column_values')
@patch('moncli.api_v2.change_simple_column_value')
def test_should_update_simple_column_value_for_status(change_simple_column_value,get_column_values, get_board, get_items):
    
    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    get_board.return_value = en.Board(**{'id': '1', 'name': 'Test Board 1'})
    item = client.get_items()[0]
    column_value = cv.create_column_value(
        ColumnType.status, 
        id= 'long_text', 
        title= 'Description', 
        text= "My previous keyword doesn't work", 
        value= json.dumps({"index":14,"post_id": None,"changed_at":"2020-05-30T19:51:09.981Z"}),
        settings_str='{}' )
    get_column_values.return_value = en.BaseColumnCollection([column_value])
    change_simple_column_value.return_value = {'id': '1', 'name': 'Test Item 01'}

    # Act
    item = item.change_simple_column_value(id=column_value.id,value="new value")
    
    # Assert 
    ok_(item != None)
    eq_(item.id, '1'),
    eq_(item.name, 'Test Item 01')


@patch('moncli.api_v2.get_items')
@patch.object(en.Item, 'get_board')
@patch('moncli.api_v2.change_multiple_column_value')
def test_item_should_change_multiple_column_values_with_dictionary(change_multiple_column_value, get_board, get_items):

    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    get_board.return_value = en.Board(**{'id': '1', 'name': 'Test Board 1'})
    change_multiple_column_value.return_value = {'id': '1', 'name': 'Test Item 01'}
    item = client.get_items()[0]

    # Act
    item = item.change_multiple_column_values({'text_column_01': 'Hello, world!'})
    
    # Assert 
    ok_(item != None)
    eq_(item.name, 'Test Item 01')



@patch('moncli.api_v2.get_items')
@patch.object(en.Item, 'get_board')
@patch('moncli.api_v2.change_multiple_column_value')
def test_item_should_change_multiple_column_values_with_column_value_list(change_multiple_column_value, get_board, get_items):

    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    get_board.return_value = en.Board(id='1', name='Test Board 01')
    change_multiple_column_value.return_value = {'id': '1', 'name': 'Test Item 01'}
    item = client.get_items()[0]

    # Act
    column_value = cv.create_column_value(ColumnType.text, id='text_column_01', title='Text Column 01', text='Hello, world!', value=json.dumps('Hello, world!'))
    item = item.change_multiple_column_values([column_value])

    # Assert 
    ok_(item != None)
    eq_(item.name, 'Test Item 01')


@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.create_subitem')
def test_item_should_add_a_subitem(create_subitem, get_items):

    # Arrange
    id = '2'
    name = 'Test Subitem 01'
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    create_subitem.return_value = {'id': id, 'name': name}
    item = client.get_items()[0]

    # Act
    subitem = item.create_subitem(name)

    # Assert 
    ok_(subitem != None)
    eq_(subitem.id, id)
    eq_(subitem.name, name)


@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.move_item_to_group')
def test_item_should_move_item_to_group(move_item_to_group, get_items):

    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    move_item_to_group.return_value = {'id': '1', 'name': 'Test Item 01'}
    item = client.get_items()[0]

    # Act
    item = item.move_to_group('group_01')

    # Assert 
    ok_(item != None)
    eq_(item.name, 'Test Item 01')


@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.archive_item')
def test_item_should_archive_item(archive_item, get_items):

    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    archive_item.return_value = {'id': '1', 'name': 'Test Item 01'}
    item = client.get_items()[0]

    # Act
    item = item.archive()

    # Assert 
    ok_(item != None)
    eq_(item.name, 'Test Item 01')


@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.delete_item')
def test_item_should_delete_item(delete_item, get_items):

    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    delete_item.return_value = {'id': '1', 'name': 'Test Item 01'}
    item = client.get_items()[0]

    # Act
    item = item.delete()

    # Assert 
    ok_(item != None)
    eq_(item.name, 'Test Item 01')


@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.duplicate_item')
def test_item_should_duplicate_itself(duplicate_item, get_items):

    # Arrange
    id = '2'
    name = 'Test Item 01 Dupe'   
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01', 'board':{'id': '1', 'name': 'Test Board'}}]
    duplicate_item.return_value = {'id': id, 'name': name}
    item = client.get_items()[0]

    # Act
    duplicate = item.duplicate()

    # Assert 
    ok_(duplicate)
    eq_(duplicate.id, id)
    eq_(duplicate.name, name)


@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.create_update')
def test_item_should_add_update(create_update, get_items):

    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    create_update.return_value = {'id': '1', 'body': 'This is a text body'}
    item = client.get_items()[0]

    # Act
    update = item.add_update('This is a text body')

    # Assert 
    ok_(update != None)
    eq_(update.body, 'This is a text body')


@patch('moncli.api_v2.get_items')
def test_item_should_get_list_of_item_updates(get_items):

    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    item = client.get_items()[0]
    get_items.return_value = [{'id': '1', 'updates':[{'id': '2', 'item_id': '1', 'creator_id': '1', 'replies': [{'id': '3', 'creator_id': '1'}]}]}]

    # Act
    updates = item.get_updates()

    # Assert 
    ok_(updates != None)
    eq_(len(updates), 1)
    eq_(updates[0].to_primitive(), item.updates[0].to_primitive())
    eq_(len(updates[0].replies), 1)


@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.delete_update')
def test_item_should_delete_update(delete_update, get_items):

    # Arrange
    id = '2'
    item_id = '1'
    creator_id = '1'
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    item = client.get_items()[0]
    get_items.return_value = [{'id': '1', 'updates':[{'id': id, 'item_id': item_id, 'creator_id': creator_id, 'replies': [{'id': '3', 'creator_id': '1'}]}]}]
    delete_update.return_value = {'id': id, 'item_id': item_id, 'creator_id': creator_id}

    # Act
    update = item.delete_update(id)

    # Assert 
    ok_(update)
    eq_(update.id, id)
    eq_(update.item_id, item_id)
    eq_(update.creator_id, creator_id)


@patch('moncli.api_v2.get_items')
@raises(en.UpdateNotFound)
def test_item_should_fail_to_delete_update(get_items):

    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01'}]
    item = client.get_items()[0]
    get_items.return_value = [{'id': '1', 'updates':[{'id': '2', 'item_id': '1', 'creator_id': '1', 'replies': [{'id': '3', 'creator_id': '1'}]}]}]

    # Act
    item.delete_update(5)


@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.clear_item_updates')
def test_item_should_clear_item_updates(clear_item_updates, get_items):

    # Arrange
    id = '1'
    get_items.return_value = [{'id': id, 'updates':[{'id': '2', 'item_id': '1', 'creator_id': '1', 'replies': [{'id': '3', 'creator_id': '1'}]}]}]
    clear_item_updates.return_value = {'id': id, 'updates':[]}
    item = client.get_items()[0]

    # Act
    updated_item = item.clear_updates()

    # Assert 
    ok_(updated_item)
    eq_(updated_item.id, id)
    eq_(len(updated_item.updates), 0)


@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.add_file_to_column')
def test_item_should_add_file(add_file_to_column, get_items):
    
    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}]
    add_file_to_column.return_value = {'id': '12345', 'name': '33.jpg', 'url': 'https://test.monday.com/12345/33.jpg'}
    item = client.get_items()[0]
    file_column = cv.create_column_value(ColumnType.file, id='files', title='Files')

    # Act
    asset = item.add_file(file_column, '/Users/test/33.jpg')

    # Assert 
    ok_(asset != None)
    eq_(asset.id, '12345')
    eq_(asset.name, '33.jpg')
    eq_(asset.url, 'https://test.monday.com/12345/33.jpg')


@patch('moncli.api_v2.get_items')
def test_item_should_get_files(get_items):
    
    # Arrange
    asset_id = '12345'
    name = '33.jpg'
    url = 'https://test.monday.com/12345/33.jpg'
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}]
    item = client.get_items()[0]
    get_items.return_value = [{'id': '1','assets': [{'id': asset_id, 'name': name, 'url': url}]}]

    # Act
    assets = item.get_files()

    # Assert 
    ok_(assets != None)
    eq_(assets[0].id, '12345')
    eq_(assets[0].name, '33.jpg')
    eq_(assets[0].url, 'https://test.monday.com/12345/33.jpg')


@patch('moncli.api_v2.get_items')
@patch('moncli.api_v2.change_column_value')
def test_item_should_remove_files(change_column_value, get_items):
    
    # Arrange
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}]
    change_column_value.return_value = get_items.return_value[0]
    item = client.get_items()[0]
    file_column = cv.create_column_value(ColumnType.file, id='files', title='Files')

    # Act
    item = item.remove_files(file_column)

    # Assert 
    ok_(item != None)
    eq_(item.id, '1')
    eq_(item.name, 'Test Item 01')
    eq_(item.board.id, '1')


@patch('moncli.api_v2.get_boards')
@patch('moncli.api_v2.get_items')
def test_should_get_activity_logs(get_items, get_boards):

    # Arrange
    id = '12345'
    account_id = '123456'
    get_items.return_value = [{'id': '1', 'name': 'Test Item 01', 'board': {'id': '1'}}]
    item = client.get_items(ids=['1'])[0]
    get_boards.return_value = [{'id': '1', 'name': 'Test Board 1', 'activity_logs': [{'id': id, 'account_id': account_id}]}]

    # Act 
    activity_logs = item.get_activity_logs()

    # Assert
    ok_(activity_logs)
    eq_(activity_logs[0].id, id)
    eq_(activity_logs[0].account_id, account_id)