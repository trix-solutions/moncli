import json

from unittest.mock import patch
from nose.tools import eq_, raises

from moncli import client, entities as en
from moncli.entities import column_value as cv
from moncli.enums import ColumnType
from moncli import types as t
from moncli.models import MondayModel


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


@patch.object(en.Item,'get_column_values')
@patch('moncli.api_v2.get_items')
def test_should_succeed_when_to_native_returns_a_str_when_passed_a_timezonevalue_value_with_api_data_to_world_clock_type(get_items,get_column_values):

    # Arrange
    id = "timezone"
    title = 'Time Zone Column 1'
    column_type = ColumnType.world_clock
    column_value = en.cv.create_column_value(column_type,id=id,title=title)
    column_value.value = 'America/New_York'
    get_items.return_value = [{'id': '1697598380', 'name': 'edited item'}]
    get_column_values.return_value = [column_value]
    item = client.get_items()[0]
    column_value = item.get_column_values()[0]

    # Act
    timezone_type = t.WorldClockType(title=title)
    value = timezone_type.to_native(column_value)

    # Assert
    eq_(value,'America/New_York')

def test_should_succeed_when_to_native_returns_a_none_when_passed_a_none_to_world_clock_type():

    # Arrange
    timezone_type = t.WorldClockType(title='Time Zone Column 1')

    # Act
    timezone_value = timezone_type.to_native(None)

    # Assert
    eq_(timezone_value,None)


def test_should_succeed_when_to_primitive_returns_an_empty_dict_when_passed_a_none_to_world_clock_type():

    # Arrange
    timezone_type = t.WorldClockType(title='Time Zone Column 1')

    # Act
    timezone_value = timezone_type.to_primitive(None)

    # Assert
    eq_(timezone_value,{})


def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_in_a_str_timezone_value_to_world_clock_type():

    # Arrange
    timezone_type = WorldClockModel(id='some_id', name='some_name', raw_data={'timezone_field': 'Invalid/Timezone'})

    # Act
    timezone_value = timezone_type.to_primitive('America/Phoenix')

    # Assert
    eq_(timezone_value['timezone'],'America/Phoenix')

@raises(t.ValidationError)
def test_should_fail_when_to_primitive_raises_a_validation_error_when_passed_a_str_timezone_that_is_invalid_to_world_clock_type():

    # Arrange
    timezone_type = WorldClockModel(id='some_id', name='some_name', raw_data={'timezone_field': 'Invalid/Timezone'})

    # Act
    timezone_type.validate()

class WorldClockModel(MondayModel):
    timezone_field = t.WorldClockType(title='Time Zone Column 1')