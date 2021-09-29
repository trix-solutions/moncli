import json
from nose.tools import ok_, eq_, raises

from moncli import entities as en, error as e
from moncli.enums import *

def test_should_create_column_value_with_empty_list_value_using_no_input_api_data():
    
    # Arrange
    id = 'file1'
    title = "file"
    column_type = ColumnType.file
    value = []

    # Act
    column_value = en.cv.create_column_value(column_type, id=id, title=title,value=value)

    # Assert
    eq_(column_value.value,[])


def test_should_create_column_value_with_an_item_id_list_value_using_input_api_data():
    
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
    column_value = en.cv.create_column_value(column_type, id=id, title=title,value=json.dumps(value))
    cv = column_value.value

    # Assert
    eq_(cv,value['files'])

@raises(e.ColumnValueError)
def test_should_raiseerror_when_trying_to_set_a_value():
    
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
    column_value = en.cv.create_column_value(column_type, id=id, title=title,value=json.dumps(value))

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
def test_shoucl_raise_columnvalueerror_when_calling_format():
    
    # Arrange
    id = 'file1'
    title = "file"
    column_type = ColumnType.file
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.format()