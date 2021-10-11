import json
from schematics.exceptions import ConversionError, DataError
from nose.tools import eq_,raises

from moncli import entities as en
from moncli.enums import ColumnType
from moncli.models import MondayModel
from moncli.types import DependencyType


def test_should_succeed_when_to_native_returns_a_list_when_passing_in_a_dependency_value_value_with_api_data_to_dependency_type():
    
    # Arrange

    id = "dependency"
    title = "Dependency 1"
    column_type = ColumnType.dependency
    value =  json.dumps({'linkedPulseIds' : [{'linkedPulseId': 123456789 }]})
    column_value =  en.cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    dependency_type = DependencyType(id='dependency')
    format =  dependency_type.to_native(column_value)

    # Assert
    eq_(format,[123456789])


def test_should_succeed_when_to_native_returns_empty_list_when_passed_none_to_dependency_type():
    # Arrange
    dependency_type = DependencyType(id='dependency')

    # Act
    format =  dependency_type.to_native(None)

    # Assert
    eq_(format,[])

@raises(ConversionError)
def test_should_succeed_when_to_native_raises_a_conversion_error_when_passed_a_list_containing_invalid_int_values_to_dependency_type():

    # Arrange
    dependency_type = DependencyType(id='dependency')

    # Act
    dependency_type.to_native( ["invalid value",124])


def test_should_succeed_when_to_primitive_returns_empty_dict_when_passed_in_a_none_to_dependency_type():
    # Arrange
    dependency_type = DependencyType(id='dependency')

    # Act
    format = dependency_type.to_primitive(None)

    # Assert
    eq_(format,{})


def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_in_a_list_with_int_values_to_dependency_type():
   
    # Arrange
    
    dependency_type = DependencyType(id='dependency')
    
    # Act
    format =  dependency_type.to_primitive([12345, 67890])['item_ids']

    # Assert
    eq_(format,[12345, 67890])