import json
from nose.tools import eq_, raises

from moncli import column_value as cv, error as e
from moncli.enums import *


def test_should_create_file_column_value_with_empty_list_value_using_no_input_api_data():
    
    # Arrange
    id = 'file1'
    title = "file"
    column_type = ColumnType.file
    value = []

    # Act
    column_value = cv.create_column_value(column_type, id=id, title=title,value=value)

    # Assert
    eq_(column_value.value,[])


def test_should_create_file_column_value_with_an_item_id_list_value_using_input_api_data():
    
    # Arrange
    id = 'file1'
    title = "file"
    column_type = ColumnType.file
    value={
        'files': [
            {
            'fileType': 'ASSET', 
            'assetId': 300958781, 
            'name': 'test.png', 
            'isImage': 'true', 
            'createdAt': 1632860467966, 
            'createdBy': '7882361'
            }
        ]
        }

    # Act
    column_value = cv.create_column_value(column_type, id=id, title=title,value=json.dumps(value))
    val = column_value.value

    # Assert
    eq_(val, value['files'])

@raises(e.ColumnValueError)
def test_should_raiseerror_when_trying_to_set_a_value_to_file_column_value():
    
    # Arrange
    id = 'file1'
    title = "file"
    column_type = ColumnType.file
    value={
        'files': [
            {
            'fileType': 'ASSET', 
            'assetId': 300958781, 
            'name': 'test.png', 
            'isImage': 'true', 
            'createdAt': 1632860467966, 
            'createdBy': '7882361'
            }
        ]
        }
    column_value = cv.create_column_value(column_type, id=id, title=title,value=json.dumps(value))

    # Act
    column_value.value = {
        'files': [
            {
            'fileType': 'ASSET', 
            'assetId': 300958781, 
            'name': 'test.png', 
            'isImage': 'true', 
            'createdAt': 1632860467966, 
            'createdBy': '7882361'
            }
        ]
        }

@raises(e.ColumnValueError)
def test_shoucl_raise_column_value_error_when_calling_format_for_a_file_column_value():
    
    # Arrange
    id = 'file1'
    title = "file"
    column_type = ColumnType.file
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.format()