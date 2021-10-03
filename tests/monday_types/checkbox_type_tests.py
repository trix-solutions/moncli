import json

from nose.tools import eq_


from moncli import entities as en
from moncli.enums import ColumnType
from moncli.types import CheckboxType


def test_checkbox_type_should_succeed_when_to_native_returns_a_bool_when_passing_a_checkboxvalue_value_with_api_data():

    # Arrange
    id = 'checkbox_1'
    column_type = ColumnType.checkbox
    title = 'Checkbox'
    value = json.dumps({'checked': 'true'})
    checkbox_value = en.cv.create_column_value(column_type, id=id, title=title, value=value)

    # Act
    checkbox_type = CheckboxType(id='check_1')
    value = checkbox_type.to_native(checkbox_value)

    # Assert
    eq_(value, checkbox_value.value)


def test_checkbox_type_should_succeed_when_to_native_returns_a_bool_when_passing_an_integer_or_string_value():

    # Arrange
    checkbox_type = CheckboxType(id='check_2')

    # Act
    value_1 = checkbox_type.to_native(1)
    value_2 = checkbox_type.to_native('check')

    # Assert
    eq_(value_1, True)
    eq_(value_2, True)


def test_checkbox_type_should_succeed_when_to_native_returns_default_native_when_passing_none():

    # Arrange
    checkbox_type = CheckboxType(id='check_3')

    # Act
    value = checkbox_type.to_native(None)

    # Assert
    eq_(value, False)


def test_checkbox_type_should_succeed_when_to_primitive_returns_an_empty_dict_when_passing_none():

    # Arrange
    checkbox_type = CheckboxType(id='check_4')

    # Act
    value = checkbox_type.to_primitive(None)

    # Assert
    eq_(value, {})


def test_checkbox_type_should_succeed_when_to_primitive_returns_an_export_dict_when_passing_a_bool_value():

    # Arrange
    checkbox_type = CheckboxType(id='check_5')

    # Act
    value = checkbox_type.to_primitive(True)

    # Assert
    eq_(value, {'checked': 'true'})