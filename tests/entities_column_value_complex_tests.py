import collections
import json
from datetime import datetime
from nose.tools import ok_, eq_, raises
from moncli.entities.column_value.objects import Week
from moncli import entities as en, error as e
from moncli.enums import *
from datetime import datetime

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

def test_should_week_column_with_no_api_data():

    # Arrange
    id = 'week1'
    title="New Week"
    column_type = ColumnType.week
    value = None
    column_value = en.cv.create_column_value(column_type,id=id,title=title)

    # Act
    format = column_value.format()

    # Assert 
    eq_(format,{})

def test_should_week_column_with_api_data():

    # Arrange
    id = 'week1'
    title="New Week"
    column_type = ColumnType.week
    api_return_value = { 
        'week': {
            'startDate': '2021-09-20',
            'endDate': '2021-09-26'
        }
    }
    value = json.dumps(api_return_value)
    column_value = en.cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    format = column_value.format()

    # Assert 
    eq_(format['week']['startDate'],'2021-09-20')

def test_should_set_none_value_to_week_column_value():
    id = 'week1'
    title="New Week"
    column_type = ColumnType.week
    value = None
    column_value = en.cv.create_column_value(column_type,id=id,title=title)
    # Act
    column_value.value = value

    # Assert 
    eq_(column_value.value,value)

def test_should_test_week_value_to_week_column_value():
    id = 'week1'
    title="New Week"
    column_type = ColumnType.week
    startDate = datetime(year=2021, month=9, day=27)
    endDate= datetime(year=2021, month=10, day=3)
    value = Week(start=startDate,end=endDate)
    column_value = en.cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value = value
    
    # Assert
    eq_(column_value.value.start, value.start)
    eq_(column_value.value.end, value.end)

def test_should_set_dict_value_to_week_column_value():
    id = 'week1'
    title="New Week"
    column_type = ColumnType.week
    value =   {
                'start': datetime(year=2021, month=9, day=27),
                'end': datetime(year=2021, month=10, day=3)
            }
    startDate = datetime(year=2021, month=9, day=27)
    endDate= datetime(year=2021, month=10, day=3)
    week = Week(start=startDate,end=endDate)
    column_value = en.cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value = value
    
    # Assert
    eq_(column_value.value.start, value['start'])
    eq_(column_value.value.end, value['end'])

@raises(e.ColumnValueError)
def test_should_set_invalid_dict_value_to_week_column_value():
    id = 'week1'
    title="New Week"
    column_type = ColumnType.week
    value =   { 'this': 'dictionary is invalid'}
    column_value = en.cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value = value 

def test_should_set_none_start_value_to_week_column_value():
    id = 'week1'
    title="New Week"
    column_type = ColumnType.week
    value=Week(start=None,end=None)
    column_value = en.cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value = value
    format = column_value.format()
    
    # Assert
    eq_(format, {})