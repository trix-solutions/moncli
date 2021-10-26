from schematics.exceptions import ConversionError
from nose.tools import eq_,raises
from enum import Enum
import json

from moncli import entities as en
from moncli.enums import ColumnType
from moncli.models import MondayModel
from moncli import types as t

# Common Column Value

# Arrange
id = 'dropdown_1'
column_type = ColumnType.dropdown
title = 'Dropdown'
dropdown_value = {
    'ids': [1],
    'changed_at': '2021-09-19T21:51:49.093Z'
}
settings = {
    "hide_footer": False,
    "labels": [
        {"id": 1, "name": "Date"},
        {"id": 2, "name": "Datetime"},
        {"id": 3, "name": "Text"},
        {"id": 4, "name": "Text Array"},
        {"id": 5, "name": "Text with Label"},
        {"id": 6, "name": "Numeric"},
        {"id": 7, "name": "Boolean"},
        {"id": 8, "name": "User Emails"}
    ]
}

class DropdownEnum(Enum):
    date='Date'
    datetime='Datetime'
    text='Text'
    text_array='Text Array'
    text_with_label='Text with Label'
    numeric='Numeric'
    boolean='Boolean'
    user_email='User Email'

value = json.dumps(dropdown_value)
settings_str = json.dumps(settings)
column_value = en.cv.create_column_value(
    column_type, id=id, title=title, value=value, settings_str=settings_str)

    
def test_should_succeed_when_to_native_returns_a_list_when_passed_a_dropdownvalue_value_with_api_data_to_dropdown_type():

    # Arrange
    dropdown_type = t.DropdownType(title='Dropdown')

    # Act 
    format = dropdown_type.to_native(column_value)[0]

    # Assert    
    eq_(format, 'Date')


def test_should_succeed_when_to_native_returns_an_empty_list_when_passed_a_none_to_dropdown_type():

    # Arrange
    dropdown_type = t.DropdownType(title='Dropdown')

    # Act 
    format = dropdown_type.to_native(None)

    # Assert    
    eq_(format, [])


def test_should_succeed_when_to_native_returns_a_list_of_str_labels_when_passed_a_list_of_str_or_int_index_or_label_values_and_element_type_is_str_to_dropdown_type():

    # Arrange
    dropdown_type = t.DropdownType(title='Dropdown')
    dropdown_type.to_native(column_value)

    # Act 
    format = dropdown_type.to_native([1,2,3])

    # Assert
    eq_(format,['Date', 'Datetime', 'Text'])


def test_should_succeed_when_to_native_returns_a_list_of_mapped_values_when_passed_a_list_of_str_or_int_index_or_label_values_and_element_type_is_an_enum_class_to_dropdown_type():

    # Arrange    
    dropdown_type = t.DropdownType(title='Dropdown',as_enum=DropdownEnum)
    dropdown_type.to_native(column_value)

    # Act
    format = dropdown_type.to_native([1,'Text'])

    # Assert
    eq_(format,[DropdownEnum.date,DropdownEnum.text])


def test_should_succeed_when_to_primitive_returns_an_empty_dict_when_passed_a_none_or_empty_list_to_dropdown_type():

    # Arrange
    dropdown_type = t.DropdownType(title='Dropdown')

    # Act 
    format = dropdown_type.to_primitive(None)

    # Assert    
    eq_(format, {})


def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_in_a_list_value_containing_str_labels_and_element_type_is_str_to_dropdown_type():

    # Arrange
    dropdown_type = t.DropdownType(title='Dropdown',as_enum=DropdownEnum)
    dropdown_type.to_native(column_value)

    # Act 
    format = dropdown_type.to_primitive(['Date','Text'])

    # Assert
    eq_(format['ids'],[1,3])


def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_a_list_of_values_containing_mapped_data_when_element_type_is_enum_class_to_dropdown_type():

    # Arrange
    dropdown_type = t.DropdownType(title='Dropdown',as_enum=DropdownEnum)
    dropdown_type.to_native(column_value)

    # Act 
    format = dropdown_type.to_primitive([DropdownEnum.date,DropdownEnum.text])

    # Assert
    eq_(format['ids'],[1,3])


@raises(ConversionError)
def test_should_raise_a_conversionerror_when_passed_a_list_containing_an_invalid_int_or_str_index_value():

    # Arrange
    dropdown_type = t.DropdownType(title='Dropdown',as_enum=DropdownEnum)
    dropdown_type.to_native(column_value)

    # Act 
    dropdown_type.to_primitive([23])


@raises(ConversionError)
def test_should_raise_conversionerror_when_passed_a_list_containing_an_invalid_str_label_value():

    # Arrange
    dropdown_type = t.DropdownType(title='Dropdown',as_enum=DropdownEnum)
    dropdown_type.to_native(column_value)

    # Act 
    dropdown_type.to_primitive(['Data','Table'])

