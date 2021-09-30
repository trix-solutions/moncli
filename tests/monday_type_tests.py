import json

from unittest.mock import patch
from nose.tools import ok_, eq_, raises
from schematics.common import NONEMPTY

from moncli import client, entities as en
from moncli.entities import column_value as cv
from moncli.enums import ColumnType
from moncli import types as t


@patch.object(en.Item,'get_column_values')
@patch('moncli.api_v2.get_items') 
def test_should_succeed_when_to_native_returns_a_str_when_passing_in_a_textvalue_value_with_api_get_itemdata(get_items,get_column_values):

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


def test_should_succeed_when_to_native_returns_a_str_when_passing_in_either_int_or_floats():

    # Arrange
    
    text_type = t.TextType(title='Text Column 1')

    # Act
    int_value = text_type.to_native(1)
    float_value = text_type.to_native(1.0)

    # Assert
    eq_(int_value,'1')
    eq_(float_value,"1.0")


@patch('moncli.api_v2.get_items')
def test_should_succeed_when_to_native_returns_none_when_passing_in_none(get_items):

    # Arrange
    text_type = t.TextType(id=1)

    # Act

    value = text_type.to_native(None)

    # Assert
    eq_(value,None)


def test_should_succeed_when_to_primitive_returns_an_empty_str_when_passed_in_a_none():

    # Arrange
    text_type = t.TextType(id=1)

    # Act
    value = text_type.to_primitive(None)

    # Assert
    eq_(value,'')

def test_should_succeed_when_to_primitive_returns_str_when_passed_in_an_int_float_or_str():

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



def test_should_succeed_when_to_native_returns_a_bool_when_passing_a_checkboxvalue_value_with_api_data():

    # Arrange
    id = 'checkbox_1'
    column_type = ColumnType.checkbox
    title = 'Checkbox'
    value = json.dumps({'checked': 'true'})
    checkbox_value = en.cv.create_column_value(column_type, id=id, title=title, value=value)

    # Act
    checkbox_type = t.CheckboxType(id='check_1')
    value = checkbox_type.to_native(checkbox_value)

    # Assert
    eq_(value, checkbox_value.value)


def test_should_succeed_when_to_native_returns_a_bool_when_passing_an_integer_or_string_value():

    # Arrange
    checkbox_type = t.CheckboxType(id='check_2')

    # Act
    value_1 = checkbox_type.to_native(1)
    value_2 = checkbox_type.to_native('check')

    # Assert
    eq_(value_1, True)
    eq_(value_2, True)


def test_should_succeed_when_to_native_returns_none_when_passing_none():

    # Arrange
    checkbox_type = t.CheckboxType(id='check_3')

    # Act
    value = checkbox_type.to_native(None)

    # Assert
    eq_(value, False)


def test_should_succeed_when_to_primitive_returns_an_empty_dict_when_passing_none():

    # Arrange
    checkbox_type = t.CheckboxType(id='check_4')

    # Act
    value = checkbox_type.to_primitive(None)

    # Assert
    eq_(value, {})


def test_should_succeed_when_to_primitive_returns_an_export_dict_when_passing_a_bool_value():

    # Arrange
    checkbox_type = t.CheckboxType(id='check_4')

    # Act
    value = checkbox_type.to_primitive(True)

    # Assert
    eq_(value, {'checked': 'true'})






