import json

from nose.tools import eq_

from moncli import entities as en
from moncli.enums import ColumnType
from moncli.types import TextType


def test_text_type_should_succeed_when_to_native_returns_a_str_when_passing_in_a_textvalue_value_with_api_get_itemdata():

    # Arrange
    text_value = en.cv.create_column_value(ColumnType.text,id="text1",title="text", value=json.dumps('new text'))
    text_type = TextType(id=1)

    # Act
    value = text_type.to_native(text_value)

    # Assert
    eq_(value,text_value.value)


def test_text_type_should_succeed_when_to_native_returns_a_str_when_passing_in_either_int_or_floats():

    # Arrange
    
    text_type = TextType(title='Text Column 1')

    # Act
    int_value = text_type.to_native(1)
    float_value = text_type.to_native(1.0)

    # Assert
    eq_(int_value,'1')
    eq_(float_value,"1.0")


def test_text_type_should_succeed_when_to_native_returns_none_when_passing_in_none():

    # Arrange
    text_type = TextType(id=1)

    # Act
    value = text_type.to_native(None)

    # Assert
    eq_(value,None)


def test_text_type_should_succeed_when_to_primitive_returns_an_empty_str_when_passed_in_a_none():

    # Arrange
    text_type = TextType(id=1)

    # Act
    value = text_type.to_primitive(None)

    # Assert
    eq_(value,'')


def test_text_type_should_succeed_when_to_primitive_returns_str_when_passed_in_an_int_float_or_str():

    # Arrange
    text_type = TextType(id=1)

    # Act
    int_value = text_type.to_primitive(1)
    float_value = text_type.to_primitive(1.0)
    str_value = text_type.to_primitive("text")
    
    # Assert
    eq_(int_value,'1')
    eq_(float_value,'1.0')
    eq_(str_value,'text')