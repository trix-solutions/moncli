import json

from nose.tools import eq_, raises

from moncli import entities as en, error as e
from moncli.enums import *


def test_should_create_dependency_column_value_with_no_api_input_data():

    # Arrange
    id = 'dependency'
    title="New dependency"
    column_type = ColumnType.dependency

    column_value = en.cv.create_column_value(column_type,id=id,title=title)

    # Act
    format = column_value.format()

    # Assert
    eq_(format,{})


def test_should_create_dependency_column_value_with_api_input_data():

    # Arrange
    id = 'dependency'
    title="New dependency"
    column_type = ColumnType.dependency
    value =  json.dumps({'linkedPulseIds' : [{'linkedPulseId': 123456789 }]})

    column_value = en.cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    format = column_value.format()

    # Assert
    eq_(format['item_ids'],[123456789])


def test_should_create_dependency_column_value_with_api_with_no_value_data():
    # Arrange
    id = 'dependency'
    title="New dependency"
    column_type = ColumnType.dependency
    value =  json.dumps({'linkedPulseIds' : []})

    column_value = en.cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    value = column_value.value

    # Assert
    eq_(value,[])


def test_should_create_dependency_column_value_with_null_value():
    # Arrange
    id = 'dependency'
    title="New dependency"
    column_type = ColumnType.dependency
    value =  json.dumps({'linkedPulseIds' : [{'linkedPulseId': 123456789 }]})

    column_value = en.cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    column_value.value = None
    value = column_value.value

    # Assert
    eq_(value,[])


def test_should_append_dependency_column_value_with_new_int_value():
    # Arrange
    id = 'dependency'
    title="New dependency"
    column_type = ColumnType.dependency
    value =  json.dumps({'linkedPulseIds' : [{'linkedPulseId': 123456789 }]})

    column_value = en.cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    column_value.value.append(123456790)
    format = column_value.format()

    # Assert
    eq_(format['item_ids'],[123456789,123456790])


def test_should_append_dependency_column_value_with_new_str_value():
    # Arrange
    id = 'dependency'
    title="New dependency"
    column_type = ColumnType.dependency
    value =  json.dumps({'linkedPulseIds' : [{'linkedPulseId': 123456789 }]})

    column_value = en.cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    column_value.value.append('123456790')
    format = column_value.format()

    # Assert
    eq_(format['item_ids'],[123456789,123456790])


@raises(e.ColumnValueError)
def test_should_fail_to_add_invalid_value_to_dependency_column_value():

    # Arrange
    id = 'dependency'
    title="New dependency"
    column_type = ColumnType.dependency

    column_value = en.cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value.append('not a value')
    column_value.format()