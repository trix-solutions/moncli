import json

from unittest.mock import patch
from nose.tools import ok_, eq_, raises
from schematics.common import NONEMPTY

from moncli import client, entities as en
from moncli.entities import column_value as cv
from moncli.enums import ColumnType
from moncli import types as t


def test_should_succeed_when_to_native_returns_an_int_or_float_when_passed_a_numbervalue_value_with_api_data():
    pass
    
def test_should_succeed_when_to_native_returns_a_int_or_float_when_passed_a_int_or_float_value():
    # Arrange
    number_type = t.NumberType(id=1)

    # Act

    int_value = number_type.to_native(1)
    float_value  = number_type.to_native(1.0)

    # Assert
    eq_(int_value,1)
    eq_(float_value,1.0)

def test_should_succeed_when_to_native_returns_a_none_when_passed_a_none():
    # Arrange
    number_type = t.NumberType(id=1)

    # Act

    value = number_type.to_native(None)

    # Assert
    eq_(value,None)


def test_should_succeed_when_to_primitive_returns_empty_str_when_passed_a_none():
    # Arrange
    number_type = t.NumberType(id=1)

    # Act
    value = number_type.to_primitive(None)

    # Assert
    eq_(value,'')


def test_should_succeed_when_to_primitive_returns_export_string_when_passed_a_int_or_float_value():
    # Arrange
    number_type = t.NumberType(id=1)

    # Act
    int_value = number_type.to_primitive(1)
    float_value = number_type.to_primitive(1.0)

    

    # Assert
    eq_(int_value,'1')
    eq_(float_value,'1.0')
