from schematics.exceptions import ConversionError, DataError, ValidationError
from nose.tools import eq_,raises
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
api_value = {
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
value = json.dumps(api_value)
settings_str = json.dumps(settings)
column_value = en.cv.create_column_value(
    column_type, id=id, title=title, value=value, settings_str=settings_str)

    
def test_should_succeed_when_to_native_returns_a_list_when_passed_a_dropdownvalue_value_with_api_data_to_dropdown_type():


    # Act 
    dropdown_type = t.DropdownType(title='Dropdown')
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

    eq_(format,[])


def test_should_succeed_when_to_native_returns_a_list_of_mapped_values_when_passed_a_list_of_str_or_int_index_or_label_values_and_element_type_is_an_enum_class_to_dropdown_type():

    pass


def test_should_succeed_when_to_primitive_returns_an_empty_dict_when_passed_a_none_or_empty_list_to_dropdown_type():

    pass


def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_in_a_list_value_containing_str_labels_and_element_type_is_str_to_dropdown_type():

    pass


def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_a_list_of_values_containing_mapped_data_when_element_type_is_enum_class__to_dropdown_type():

    pass