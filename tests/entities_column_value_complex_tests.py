import collections
import json
from datetime import datetime
from moncli.entities.column_value.constants import COMPLEX_NULL_VALUE
from moncli.config import DATE_FORMAT
from moncli.entities import column_value
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


def test_should_create_timeline_column_value_with_no_api_data():

    # Arrange
    id = 'timeline1'
    title = 'timeline 1'
    column_type = ColumnType.timeline
    column_value = en.cv.create_column_value(column_type,id=id,title=title,value=None)

    # Act
    format = column_value.format()

    # Assert
    eq_(format, {})

def test_should_create_timeline_column_value_with_api_data():

    # Arrange
    id = 'timeline'
    title = 'timeline 2'
    column_type = ColumnType.timeline
    from_date=  '2021-01-01'
    to_date = '2021-12-31'
    type= 'milestone'
    dict_value = {
        'from': from_date,
        'to': to_date,
        'visualization_type': type
    }
    value = json.dumps(dict_value)
    column_value = en.cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    format = column_value.format()

    # Assert
    eq_(format['from'], from_date)
    eq_(format['to'], to_date)

def test_should_set_timeline_column_value_to_None():
    
    # Arrange
    id = 'timeline1'
    title = 'timeline 3'
    column_type = ColumnType.timeline
    column_value = en.cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value=None

    # Assert
    eq_(column_value.value,None)

def test_should_set_timeline_column_value_with_valid_dict():
    # Arrange
    id = 'timeline1'
    title = 'timeline 4'
    column_type = ColumnType.timeline
    column_value = en.cv.create_column_value(column_type,id=id,title=title)
    from_date=  '2021-01-01'
    to_date = '2021-12-31'
    value = {
              'from': '2021-12-31',
               'to': '2021-12-31',
               'visualization_type': 'milestone'
            }
    from_date = datetime.strptime(value['from'],DATE_FORMAT)
    to_date = datetime.strptime(value['to'],DATE_FORMAT)
    # Act
    column_value.value = value

    # Assert
    eq_(column_value.value.from_date,from_date) 
    eq_(column_value.value.to_date,to_date)

@raises(e.ColumnValueError)
def test_should_set_invalid_dict_value_to_timeline_value():

    # Arrange
    id = 'timeline1'
    title = 'timeline 4'
    column_type = ColumnType.timeline
    column_value = en.cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value = {'this': 'is an invalid dict'}

def test_should_set_date_value_to_none_for_timeline_column_value():
    id = 'timeline1'
    title = 'timeline 4'
    column_type = ColumnType.timeline
    from_date=  '2021-01-01'
    to_date = '2021-12-31'
    dict_value = {
    'from': from_date,
    'to': to_date,
    }
    value = json.dumps(dict_value)
    column_value = en.cv.create_column_value(column_type,id=id,title=title,value=value)
    
    # Act
    column_value.value.from_date = None
    format = column_value.format()

    # Assert
    eq_(format,COMPLEX_NULL_VALUE)

@raises(e.ColumnValueError)
def test_should_set_from_date_greater_than_to_date_timeline_column_value():
    id = 'timeline1'
    title = 'timeline 4'
    column_type = ColumnType.timeline
    from_date=  '2021-12-31'
    to_date = '2021-01-01'
    dict_value = {
    'from': from_date,
    'to': to_date,
    }
    value = json.dumps(dict_value)
    column_value = en.cv.create_column_value(column_type,id=id,title=title)
    
    # Act
    column_value.value = value
