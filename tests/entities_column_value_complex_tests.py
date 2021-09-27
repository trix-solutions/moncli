import collections
import json
from datetime import datetime
from nose.tools import ok_, eq_, raises

from moncli import entities as en, error as e
from moncli.enums import *

def test_should_item_link_column_with_no_api_data():

    # Arrange
    id = 'item_link'
    title="Item Link"
    column_type = ColumnType.board_relation
    value=None

    # Act
    column_value = en.cv.create_column_value(column_type,id=id,title=title,value=value)
    format = column_value.format()

    # Assert 
    eq_(format,{})

def test_should_item_link_column_with_api_data():

    # Arrange
    id = 'item_link'
    title="Item Link"
    column_type = ColumnType.board_relation
    api_value={
                'linkedPulseIds' : [
                    {'linkedPulseId': 123456789 }
                ]
                }
    value = json.dumps(api_value)
    column_value = en.cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    format = column_value.format()

    # Assert 
    eq_(format['item_ids'],[123456789])

def test_should_set_null_item_link_column_value():
    id = 'item_link'
    title="Item Link"
    column_type = ColumnType.board_relation
    column_value = en.cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value = {}

    # Assert 
    eq_(column_value.value,[])

def test_should_append_integer_id_to_item_link_column_value():
    id = 'item_link'
    title="Item Link"
    column_type = ColumnType.board_relation
    column_value = en.cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value.append(123456789)
    format = column_value.format()
    format_dict={
        'item_ids':[123456789]
    }

    # Assert 
    eq_(format,format_dict)
    eq_(format['item_ids'],[123456789])

def test_should_append_string_id_to_item_link_column_value():
    id = 'item_link'
    title="Item Link"
    column_type = ColumnType.board_relation
    column_value = en.cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value.append('123456789')
    format = column_value.format()
    format_dict={
        'item_ids':[123456789]
    }

    # Assert 
    eq_(format,format_dict)
    eq_(format['item_ids'],[123456789])

@raises(e.ColumnValueError)
def test_should_append_invalid_string_id_to_item_link_column_value():
    id = 'item_link'
    title="Item Link"
    column_type = ColumnType.board_relation
    column_value = en.cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value.append('not a valid string')
    column_value.format()


def test_should_item_link_column_with_api_data_with_no_linkedpulseid_key():

    # Arrange
    id = 'item_link'
    title="Item Link"
    column_type = ColumnType.board_relation
    api_value={
                'id' : [
                    {'linkedPulseId': 123456789 }
                ]
                }
    value = json.dumps(api_value)

    # Act
    column_value = en.cv.create_column_value(column_type,id=id,title=title,value=value)


    # Assert 
    eq_(column_value.value,[])

def test_should_set_checkbox_column_value_with_no_api_input_data():

    # Arrange
    id = 'checkbox_1'
    column_type = ColumnType.checkbox
    title = 'Checkbox'
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    format = column_value.format()

    # Assert
    eq_(format, {})


def test_should_set_checkbox_column_value_with_api_input_data():

    # Arrange
    id = 'checkbox_2'
    column_type = ColumnType.checkbox
    title = 'Checkbox'
    value = json.dumps({'checked': 'true'})
    column_value = en.cv.create_column_value(column_type, id=id, title=title, value=value)

    # Act
    format = column_value.format()

    # Assert
    eq_(format, {'checked': 'true'})


def test_should_return_checkbox_column_value_as_false_when_value_is_set_to_none():

     # Arrange
    id = 'checkbox_3'
    column_type = ColumnType.checkbox
    title = 'Checkbox'
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = None

    # Assert
    eq_(column_value.value, False)
    

def test_should_set_checkbox_column_value_with_bool_value():

     # Arrange
    id = 'checkbox_4'
    column_type = ColumnType.checkbox
    title = 'Checkbox'
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = True

    # Assert
    eq_(column_value.value, True)


def test_should_set_checkbox_column_value_with_string_value():

    # Arrange
    id = 'checkbox_5'
    column_type = ColumnType.checkbox
    title = 'Checkbox'
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = 'true'

    # Assert
    eq_(column_value.value, True)


def test_should_set_checkbox_column_value_with_int_value():

    # Arrange
    id = 'checkbox_6'
    column_type = ColumnType.checkbox
    title = 'Checkbox'
    column_value = en.cv.create_column_value(column_type, id=id, title=title)
    value = 1234
    # Act
    column_value.value = value

    # Assert
    eq_(column_value.value, bool(value))

