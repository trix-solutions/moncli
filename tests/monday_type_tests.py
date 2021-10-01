import json
from datetime import datetime

from unittest.mock import patch
from nose.tools import eq_

from moncli import client, entities as en
from moncli.entities import column_value as cv
from moncli.enums import ColumnType
from moncli import types as t


@patch.object(en.Item,'get_column_values')
@patch('moncli.api_v2.get_items') 
def test_text_type_should_succeed_when_to_native_returns_a_str_when_passing_in_a_textvalue_value_with_api_get_itemdata(get_items,get_column_values):

    # Arrange
    text_value = en.cv.create_column_value(ColumnType.text,id="text1",title="text")
    text_value.value='new text'
    get_items.return_value = [{'id': '1697598380', 'name': 'edited item'}]
    get_column_values.return_value = [text_value]
    item = client.get_items()[0]
    column_value = item.get_column_values()[0]

    # Act
    text_type = t.TextType(id=1)
    value = text_type.to_native(column_value)

    # Assert
    eq_(value,"new text")


def test_text_type_should_succeed_when_to_native_returns_a_str_when_passing_in_either_int_or_floats():

    # Arrange
    
    text_type = t.TextType(title='Text Column 1')

    # Act
    int_value = text_type.to_native(1)
    float_value = text_type.to_native(1.0)

    # Assert
    eq_(int_value,'1')
    eq_(float_value,"1.0")


@patch('moncli.api_v2.get_items')
def test_text_type_should_succeed_when_to_native_returns_none_when_passing_in_none(get_items):

    # Arrange
    text_type = t.TextType(id=1)

    # Act

    value = text_type.to_native(None)

    # Assert
    eq_(value,None)


def test_text_type_should_succeed_when_to_primitive_returns_an_empty_str_when_passed_in_a_none():

    # Arrange
    text_type = t.TextType(id=1)

    # Act
    value = text_type.to_primitive(None)

    # Assert
    eq_(value,'')

def test_text_type_should_succeed_when_to_primitive_returns_str_when_passed_in_an_int_float_or_str():

    # Arrange
    text_type = t.TextType(id=1)

    # Act
    int_value = text_type.to_primitive(1)
    float_value = text_type.to_primitive(1.0)
    str_value = text_type.to_primitive("text")
    
    # Assert
    eq_(int_value,'1')
    eq_(float_value,'1.0')
    eq_(str_value,'text')


def test_number_type_should_succeed_when_to_native_returns_an_int_or_float_when_passed_a_numbervalue_value_with_api_data():
    # Arrange
    number_type = t.NumberType(id='number_1')
    column_value = cv.create_column_value(ColumnType.numbers, id='number_1', value=json.dumps(1))

    # Act
    int_value = number_type.to_native(column_value)

    # Assert 
    eq_(int_value, 1)
    

def test_number_type_should_succeed_when_to_native_returns_a_int_or_float_when_passed_a_int_or_float_value():
    # Arrange
    number_type = t.NumberType(id=1)

    # Act

    int_value = number_type.to_native(1)
    float_value  = number_type.to_native(1.0)

    # Assert
    eq_(int_value,1)
    eq_(float_value,1.0)


def test_number_type_should_succeed_when_to_native_returns_a_none_when_passed_a_none():
    # Arrange
    number_type = t.NumberType(id=1)

    # Act

    value = number_type.to_native(None)

    # Assert
    eq_(value,None)


def test_number_type_should_succeed_when_to_primitive_returns_empty_str_when_passed_a_none():
    # Arrange
    number_type = t.NumberType(id=1)

    # Act
    value = number_type.to_primitive(None)

    # Assert
    eq_(value,'')


def test_number_type_should_succeed_when_to_primitive_returns_export_string_when_passed_a_int_or_float_value():
    # Arrange
    number_type = t.NumberType(id=1)

    # Act
    int_value = number_type.to_primitive(1)
    float_value = number_type.to_primitive(1.0)

    # Assert
    eq_(int_value,'1')
    eq_(float_value,'1.0')


def test_date_type_should_succeed_when_to_native_returns_a_datetime_when_passing_a_datevalue_value_with_api_data():

    # Arrange
    id = 'date_1'
    title = 'Date'
    column_type = ColumnType.date
    date = datetime(2021, 9, 29, 17, 48, 35)
    date = {'date': str(date.date()), 'time': str(date.time())}
    value = json.dumps(date)
    date_value = en.cv.create_column_value(column_type, id=id, title=title,value=value)

    # Act
    date_type = t.DateType(id='date_column_1')
    value = date_type.to_native(date_value)

    # Assert
    eq_(value, date_value.value)


def test_date_type_should_succeed_when_to_native_returns_a_datetime_when_passing_a_integer_or_string_value():

    # Arrange
    date_type = t.DateType(id='date_column_2', has_time=True)

    # Act
    value_1 = date_type.to_native(1632917915)
    value_2 = date_type.to_native('2021-09-29 17:48:35')

    # Assert
    eq_(value_1, datetime(2021, 9, 29, 17, 48, 35))
    eq_(value_2, datetime(2021, 9, 29, 17, 48, 35))


def test_date_type_should_succeed_when_to_native_returns_none_when_passing_none():

    # Arrange
    date_type = t.DateType(id='date_column_3')

    # Act
    value = date_type.to_native(None)

    # Assert
    eq_(value, None)


def test_date_type_should_succeed_when_to_primitive_returns_empty_dict_when_passing_none():

    # Arrange
    date_type = t.DateType(id='date_column_4')

    # Act
    value = date_type.to_primitive(None)

    # Assert
    eq_(value, {})


def test_date_type_should_succeed_when_to_primitive_returns_export_dict_when_passing_datetime_value():

    # Arrange
    date_type = t.DateType(id='date_column_5')
    value = datetime(2021, 9, 29)

    # Act
    value = date_type.to_primitive(value)

    # Assert
    eq_(value['date'], '2021-09-29')
    eq_(value['time'], None)


def test_date_type_should_succeed_when_to_primitive_returns_export_dict_with_time_when_passing_datetime_value_and_has_time_is_true():

    # Arrange
    date_type = t.DateType(id='date_column_6', has_time=True)
    value = datetime(2021, 9, 29, 17, 48, 35)

    # Act
    value = date_type.to_primitive(value)

    # Assert
    eq_(value['date'], '2021-09-29')
    eq_(value['time'], '17:48:35')




