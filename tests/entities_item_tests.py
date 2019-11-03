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

    get_items.return_value = [{'id': '1', 'column_values': [{'id': 'text_column_01', 'title': 'Text Column 01', 'value': json.dumps('Hello, Grandma')}]}]

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
@raises(e.exceptions.NotEnoughGetColumnValueParameters)
def test_item_should_fail_to_retrieve_column_value_from_too_few_parameters(get_boards, get_items, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1', 'board': {'id': '1'}}]
    get_boards.return_value = [{'id': '1', 'columns': [{'id': 'text_column_01', 'type': 'text'}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    item = client.get_items()[0]

    get_items.return_value = [{'id': '1', 'column_values': [{'id': 'text_column_01', 'title': 'Text Column 01', 'value': json.dumps('Hello, Grandma')}]}]

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

    get_items.return_value = [{'id': '1', 'column_values': [{'id': 'text_column_01', 'title': 'Text Column 01', 'value': json.dumps('Hello, Grandma')}]}]

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

    get_items.return_value = [{'id': '1', 'column_values': [{'id': 'text_column_01', 'title': 'Text Column 01', 'value': json.dumps('Hello, Grandma')}]}]

    # Act
    column_value = item.get_column_value(id='text_column_01')

    # Assert 
    ok_(column_value != None)
    eq_(column_value.title, 'Text Column 01')
    eq_(column_value.text, 'Hello, Grandma')


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

    get_items.return_value = [{'id': '1', 'column_values': [{'id': 'text_column_01', 'title': 'Text Column 01', 'value': json.dumps('Hello, Grandma')}]}]

    # Act
    column_value = item.get_column_value(title='Text Column 01')

    # Assert 
    ok_(column_value != None)
    eq_(column_value.title, 'Text Column 01')
    eq_(column_value.text, 'Hello, Grandma')