import json

from nose.tools import eq_

from moncli import entities as en
from moncli.enums import ColumnType
from moncli.types import NumberType


def test_number_type_should_succeed_when_to_native_returns_an_int_or_float_when_passed_a_numbervalue_value_with_api_data():
    # Arrange
    number_type = NumberType(id='number_1')
    column_value = en.cv.create_column_value(ColumnType.numbers, id='number_1', value=json.dumps(1))

    # Act
    int_value = number_type.to_native(column_value)

    # Assert 
    eq_(int_value, 1)
    

def test_number_type_should_succeed_when_to_native_returns_a_int_or_float_when_passed_a_int_or_float_value():
    # Arrange
    number_type = NumberType(id=1)

    # Act

    int_value = number_type.to_native(1)
    float_value  = number_type.to_native(1.0)

    # Assert
    eq_(int_value,1)
    eq_(float_value,1.0)


def test_number_type_should_succeed_when_to_native_returns_a_none_when_passed_a_none():
    # Arrange
    number_type = NumberType(id=1)

    # Act

    value = number_type.to_native(None)

    # Assert
    eq_(value,None)


def test_number_type_should_succeed_when_to_primitive_returns_empty_str_when_passed_a_none():
    # Arrange
    number_type = NumberType(id=1)

    # Act
    value = number_type.to_primitive(None)

    # Assert
    eq_(value,'')


def test_number_type_should_succeed_when_to_primitive_returns_export_string_when_passed_a_int_or_float_value():
    # Arrange
    number_type = NumberType(id=1)

    # Act
    int_value = number_type.to_primitive(1)
    float_value = number_type.to_primitive(1.0)

    # Assert
    eq_(int_value,'1')
    eq_(float_value,'1.0')