import json

from nose.tools import eq_

from moncli import column_value as cv
from moncli.enums import ColumnType
from moncli.types import LongTextType


def test_longtext_type_should_succeed_when_to_native_returns_a_str_when_passing_a_longtext_value_with_api_data():

    # Arrange
    id = 'long_text_1'
    column_type = ColumnType.long_text
    title = 'Long Text'
    text = 'Some long text'
    value = json.dumps({'text': text})
    longtext_value = cv.create_column_value(column_type, id=id, title=title, value=value)

    # Act
    longtext_type = LongTextType(id='longtext_column_1')
    value = longtext_type.to_native(longtext_value)

    # Assert
    eq_(value, text)


def test_longtext_type_should_succeed_when_to_native_returns_a_str_when_passing_an_integer_or_float_value():

    # Arrange
    longtext_type = LongTextType(id='longtext_column_2')

    # Act
    value_1 = longtext_type.to_native(1)
    value_2 = longtext_type.to_native(420.69)

    # Assert
    eq_(value_1, '1')
    eq_(value_2, '420.69')


def test_longtext_type_should_succeed_when_to_native_returns_none_when_passing_none():

    # Arrange
    longtext_type = LongTextType(id='longtext_column_3')

    # Act
    value = longtext_type.to_native(None)

    # Assert
    eq_(value, None)


def test_longtext_type_should_succeed_when_to_primitive_returns_empty_dict_when_passing_none():

    # Arrange
    longtext_type = LongTextType(id='longtext_column_4')

    # Act
    value = longtext_type.to_primitive(None)

    # Assert
    eq_(value, {})


def test_longtext_type_should_succeed_when_to_primitive_returns_export_dict_when_passing_string_value():

     # Arrange
    longtext_type = LongTextType(id='longtext_column_5')

    # Act
    value = longtext_type.to_primitive('longtext')

    # Assert
    eq_(value, {'text': 'longtext'})
