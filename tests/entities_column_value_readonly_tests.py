from nose.tools import ok_, eq_, raises
from moncli import entities as en, error as e
from moncli.enums import *
import json


def test_should_create_subitems_column_value_with_no_api_input_data():

    # Arrange
    id = 'subitem_1'
    column_type = ColumnType.subitems
    title = 'Subitems'
    
    # Act
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Assert
    eq_(column_value.value, [])


def test_should_create_subitems_column_value_with_api_input_data():

    # Arrange
    id = 'subitem_2'
    column_type = ColumnType.subitems
    title = 'Subitems'
    value = json.dumps({'linkedPulseIds': [{'linkedPulseId': 1234567890}]})
    
    # Act
    column_value = en.cv.create_column_value(column_type, id=id, title=title, value=value)

    # Assert
    eq_(column_value.value, [1234567890])


@raises(e.ColumnValueError)
def test_should_raise_column_value_error_when_setting_subitems_column_value_to_a_value():

    # Arrange
    id = 'subitem_3'
    column_type = ColumnType.subitems
    title = 'Subitems'
    value = [123456789]
    column_value = en.cv.create_column_value(column_type, id=id, title=title)
    
    # Act
    column_value.value = value


@raises(e.ColumnValueError)
def test_should_raise_column_value_error_when_formatting_subitems_column_value():

    # Arrange
    id = 'subitem_4'
    column_type = ColumnType.subitems
    title = 'Subitems'
    column_value = en.cv.create_column_value(column_type, id=id, title=title)
    
    # Act
    column_value.format()

