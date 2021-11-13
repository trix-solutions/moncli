import json
from datetime import datetime

from nose.tools import eq_, raises

from moncli import column_value as cv, error as e
from moncli.config import DATE_FORMAT
from moncli.enums import *


def test_should_create_item_link_column_value_with_no_api_data():

    # Arrange
    id = 'item_link'
    title="Item Link"
    column_type = ColumnType.board_relation
    value=None

    # Act
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)
    format = column_value.format()

    # Assert 
    eq_(format,{})


def test_should_create_item_link_column_value_with_api_data():

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
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    format = column_value.format()

    # Assert 
    eq_(format['item_ids'],[123456789])


def test_should_set_null_item_link_column_value():
    id = 'item_link'
    title="Item Link"
    column_type = ColumnType.board_relation
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value = {}

    # Assert 
    eq_(column_value.value,[])


def test_should_append_integer_id_to_item_link_column_value():
    id = 'item_link'
    title="Item Link"
    column_type = ColumnType.board_relation
    column_value = cv.create_column_value(column_type,id=id,title=title)

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
    column_value = cv.create_column_value(column_type,id=id,title=title)

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
    column_value = cv.create_column_value(column_type,id=id,title=title)

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
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)


    # Assert 
    eq_(column_value.value,[])


def test_should_set_checkbox_column_value_with_no_api_input_data():

    # Arrange
    id = 'checkbox_1'
    column_type = ColumnType.checkbox
    title = 'Checkbox'
    column_value = cv.create_column_value(column_type, id=id, title=title)
    
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
    column_value = cv.create_column_value(column_type, id=id, title=title, value=value)

    # Act
    format = column_value.format()

    # Assert
    eq_(format, {'checked': 'true'})


def test_should_return_checkbox_column_value_as_false_when_value_is_set_to_none():

     # Arrange
    id = 'checkbox_3'
    column_type = ColumnType.checkbox
    title = 'Checkbox'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = None

    # Assert
    eq_(column_value.value, False)
    

def test_should_set_checkbox_column_value_with_bool_value():

     # Arrange
    id = 'checkbox_4'
    column_type = ColumnType.checkbox
    title = 'Checkbox'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = True

    # Assert
    eq_(column_value.value, True)


def test_should_set_checkbox_column_value_with_string_value():

    # Arrange
    id = 'checkbox_5'
    column_type = ColumnType.checkbox
    title = 'Checkbox'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = 'true'

    # Assert
    eq_(column_value.value, True)


def test_should_set_checkbox_column_value_with_int_value():

    # Arrange
    id = 'checkbox_6'
    column_type = ColumnType.checkbox
    title = 'Checkbox'
    column_value = cv.create_column_value(column_type, id=id, title=title)
    value = 1234
    # Act
    column_value.value = value

    # Assert
    eq_(column_value.value, bool(value))


def test_should_create_timeline_column_value_with_no_api_data():

    # Arrange
    id = 'timeline1'
    title = 'timeline 1'
    column_type = ColumnType.timeline
    column_value = cv.create_column_value(column_type,id=id,title=title,value=None)
    
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

    # Act
    column_value = cv.create_column_value(column_type, id=id, title=title, value=value)
    format = column_value.format()

    # Assert
    eq_(format['from'], from_date)
    eq_(format['to'], to_date)


def test_should_set_timeline_column_value_to_None():
    
    # Arrange
    id = 'timeline1'
    title = 'timeline 3'
    column_type = ColumnType.timeline
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value=None

    # Assert
    eq_(column_value.value,None)


def test_should_set_timeline_column_value_with_valid_dict():
    # Arrange
    id = 'timeline1'
    title = 'timeline 4'
    column_type = ColumnType.timeline
    column_value = cv.create_column_value(column_type,id=id,title=title)
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
    column_value = cv.create_column_value(column_type,id=id,title=title)

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
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)
    
    # Act
    column_value.value.from_date = None
    format = column_value.format()

    # Assert
    eq_(format, cv.COMPLEX_NULL_VALUE)


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
    column_value = cv.create_column_value(column_type,id=id,title=title)
    
    # Act
    column_value.value = value


def test_should_week_column_with_no_api_data():

    # Arrange
    id = 'week1'
    title="New Week"
    column_type = ColumnType.week
    column_value = cv.create_column_value(column_type,id=id,title=title)

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
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    format = column_value.format()

    # Assert 
    eq_(format['week']['startDate'],'2021-09-20')


def test_should_set_none_value_to_week_column_value():
    id = 'week1'
    title="New Week"
    column_type = ColumnType.week
    value = None
    column_value = cv.create_column_value(column_type,id=id,title=title)
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
    value = cv.Week(start=startDate,end=endDate)
    column_value = cv.create_column_value(column_type,id=id,title=title)

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
    week = cv.Week(start=startDate,end=endDate)
    column_value = cv.create_column_value(column_type,id=id,title=title)

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
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value = value 


def test_should_set_none_start_value_to_week_column_value():
    id = 'week1'
    title="New Week"
    column_type = ColumnType.week
    value=cv.Week(start=None,end=None)
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value = value
    format = column_value.format()
    
    # Assert
    eq_(format, {})
    

def test_should_create_country_column_value_with_no_api_input_data():

    # Arrange
    id = 'country_value_1'
    title = "Country"
    column_type = ColumnType.country
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    format = column_value.format()

    # Assert
    eq_(format, {})


def test_should_create_country_column_value_with_api_input_data():

    # Arrange
    id = 'country_value_2'
    title = "Country"
    column_type = ColumnType.country
    name = 'United States'
    code = 'US'
    value = json.dumps({'countryName': name, 'countryCode': code})
    column_value = cv.create_column_value(column_type, id=id, title=title, value=value)

    # Act
    format = column_value.format()

    # Assert
    eq_(format['countryName'], name)
    eq_(format['countryCode'], code)


def test_should_set_country_column_value_to_none():

    # Arrange
    id = 'country_value_3'
    title = "Country"
    column_type = ColumnType.country
    value = None
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = value

    # Assert
    eq_(column_value.value, None)
    
    
def test_should_set_country_column_value_to_country_value():

    # Arrange
    id = 'country_value_4'
    title = "Country"
    column_type = ColumnType.country
    name = 'United States'
    code = 'US'
    value = cv.Country(name=name, code=code)
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = value

    # Assert
    eq_(column_value.value.name, name)
    eq_(column_value.value.code, code)


def test_should_set_country_column_value_to_valid_dict_value():

    # Arrange
    id = 'country_value_5'
    title = "Country"
    column_type = ColumnType.country
    name = 'United States'
    code = 'US'
    value = {'name': name, 'code': code}
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = value

    # Assert
    eq_(column_value.value.name, name)
    eq_(column_value.value.code, code)


@raises(e.ColumnValueError)
def test_should_set_country_column_value_to_invalid_dict_value():

    # Arrange
    id = 'country_value_6'
    title = "Country"
    column_type = ColumnType.country
    value = {'this': 'No such Country'}
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = value


def test_should_create_country_column_value_with_name_set_to_none():

    # Arrange
    id = 'country_value_7'
    title = "Country"
    column_type = ColumnType.country
    name = None
    code = 'US'
    value = cv.Country(name=name, code=code)
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = value
    format = column_value.format()
    
    # Assert
    eq_(format, {})


def test_should_create_country_column_value_with_code_set_to_none():

    # Arrange
    id = 'country_value_7'
    title = "Country"
    column_type = ColumnType.country
    name = 'United States'
    code = None
    value = cv.Country(name=name, code=code)
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = value
    format = column_value.format()
    
    # Assert
    eq_(format, {})


def test_should_create_tags_column_value_with_no_api_input_data():

    # Arrange
    id = 'tags_value_1'
    title = "Tags"
    column_type = ColumnType.tags
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    format = column_value.format()

    # Assert
    eq_(format, {})


def test_should_create_tags_column_value_with_api_input_data():

    # Arrange
    id = 'tags_value_2'
    title = "Tags"
    column_type = ColumnType.tags
    value = json.dumps({'tag_ids': [12345, 12346]})
    column_value = cv.create_column_value(column_type, id=id, title=title, value=value)

    # Act
    format = column_value.format()

    # Assert
    eq_(format['tag_ids'], [12345, 12346])


def test_should_set_tags_column_value_to_none():

    # Arrange
    id = 'tags_value_3'
    title = "Tags"
    column_type = ColumnType.tags
    value = None
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = value

    # Assert
    eq_(column_value.value, [])


def test_should_append_tags_column_value_with_integer_id():

    # Arrange
    id = 'tags_value_4'
    title = "Tags"
    column_type = ColumnType.tags
    value = 12347
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value.append(value)
    format = column_value.format()

    # Assert
    eq_(format['tag_ids'], [12347])


def test_should_append_tags_column_value_with_string_id():

    # Arrange
    id = 'tags_value_5'
    title = "Tags"
    column_type = ColumnType.tags
    value = '12347'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value.append(value)
    format = column_value.format()

    # Assert
    eq_(format['tag_ids'], [12347])


@raises(e.ColumnValueError)
def test_should_fail_to_append_invalid_string_id_to_tags_column_value():

    # Arrange
    id = 'tags_value_6'
    title = "Tags"
    column_type = ColumnType.tags
    value = 'invalid_tag_id'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value.append(value)
    column_value.format()


def test_should_create_hour_column_value_with_no_api_data():

    # Arrange
    id = 'hour'
    title="hour"
    column_type = ColumnType.hour

    # Act
    column_value = cv.create_column_value(column_type,id=id,title=title)
    format = column_value.format()

    # Assert 
    eq_(format,{})


def test_should_create_hour_column_value_with_api_data():

    # Arrange
    id = 'hour'
    title="hour"
    column_type = ColumnType.hour
    hour_value = {
                'hour': 23,
                'minute': 59
                }
    value = json.dumps(hour_value)
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    format = column_value.format()

    # Assert 
    eq_(format, hour_value)


def test_should_set_none_to_hour_column_value():

    # Arrange
    id = 'hour'
    title="hour"
    column_type = ColumnType.hour

    # Act
    column_value = cv.create_column_value(column_type,id=id,title=title)
    column_value.value = None

    # Assert 
    eq_(column_value.value, None)


def test_should_set_hour_value_to_hour_column_value():
    id = 'hour'
    title="hour"
    column_type = ColumnType.hour
    hour_value = cv.Hour(hour=1,minute=1)

    # Act
    column_value = cv.create_column_value(column_type,id=id,title=title)
    column_value.value = hour_value

    # Assert 
    eq_(column_value.value, hour_value)


def test_should_set_valid_dict_to_hour_column_value():
    id = 'hour'
    title="hour"
    column_type = ColumnType.hour
    value = {
                'hour': 23,
                'minute': 59
                }
    hour_value = cv.Hour(hour=23,minute=59)
    column_value = cv.create_column_value(column_type,id=id,title=title)
    
    # Act
    column_value.value = value

    # Assert 
    eq_(column_value.value.hour, hour_value.hour)


@raises(e.ColumnValueError)
def test_should_set_invalid_dict_to_hour_column_value():
    id = 'hour'
    title="hour"
    column_type = ColumnType.hour
    value = {
            'this': 'clock looks messed up...'
            }
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act 
    column_value.value = value


def test_should_set_hour_value_to_none_for_hour_column_value():
    
    # Arrange
    id = 'hour'
    title="hour"
    column_type = ColumnType.hour
    hour_value = {
                'hour': 23,
                'minute': 59
                }
    value = json.dumps(hour_value)
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)
    
    # Act
    column_value.value.hour = None
    format = column_value.format()

    # Assert 
    eq_(format, cv.COMPLEX_NULL_VALUE)


def test_should_set_minute_value_to_none_for_hour_column_value():
    id = 'hour'
    title="hour"
    column_type = ColumnType.hour
    hour_value = {
                'hour': 23,
                'minute': 59
                }
    value = json.dumps(hour_value)
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)
    
    # Act
    column_value.value.minute = None
    format = column_value.format()

    # Assert 
    eq_(format['minute'],0)


def test_should_create_rating_column_value_with_no_api_input_data():
    
    # Arrange
    id = 'rating'
    title = 'rating 1'
    column_type = ColumnType.rating
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act
    format = column_value.format()

    # Assert
    eq_(format,{})


def test_should_create_rating_column_value_with_api_input_data():
    
    # Arrange
    id = 'rating'
    title = 'rating 1'
    column_type = ColumnType.rating
    rating_value = { 'rating': 4 }
    value = json.dumps(rating_value)
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    format = column_value.format()

    # Assert
    eq_(format,rating_value)


def test_should_set_rating_column_value_with_none_value():
    
    # Arrange
    id = 'rating'
    title = 'rating 1'
    column_type = ColumnType.rating
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value=None

    # Assert
    eq_(column_value.value,None)


def test_should_set_rating_column_value_with_int_value():
    
    # Arrange
    id = 'rating'
    title = 'rating 1'
    column_type = ColumnType.rating
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value=4

    # Assert
    eq_(column_value.value,4)


def test_should_timezone_column_value_with_no_api_data():

    # Arrange
    id = 'timezone1'
    title="New timezone"
    column_type = ColumnType.world_clock
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act
    format = column_value.format()

    # Assert 
    eq_(format,{})


def test_should_timezone_column_value_with_api_data():

    # Arrange
    id = 'timezone1'
    title="New timezone"
    column_type = ColumnType.world_clock
    tz_value = {'timezone':'America/New_York'}
    value = json.dumps(tz_value)
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    format = column_value.format()

    # Assert     
    eq_(format,tz_value)


def test_should_set_none_value_to_timezone_column_value():
    id = 'timezone1'
    title="New timezone"
    column_type = ColumnType.world_clock
    value = None
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value = value

    # Assert
    eq_(column_value.value,value)


def test_should_timezone_column_value_str_timezone_value():

    # Arrange
    id = 'timezone1'
    title="New timezone"
    column_type = ColumnType.world_clock

    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value = 'Asia/Kolkata'
    format = column_value.format()

    # Assert 
    eq_(format['timezone'],'Asia/Kolkata')

