import json
from schematics.exceptions import ConversionError
from nose.tools import eq_,raises
from enum import Enum

from moncli import entities as en
from moncli.enums import ColumnType
from moncli.types import StatusType

# default class and data mapping declaration for common use
class Status(Enum):
  ready = 'Ready'
  in_progress = 'In Progress'
  done = 'Done'




def test_should_succeed_when_to_native_returns_a_str_when_passing_in_a_statusvalue_value_with_api_data_to_status_type():
    
    # Arrange
    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 1}),settings_str=settings_str)


    # Act
    status_type = StatusType(title='Status')
    format = status_type.to_native(column_value)

    # Assert
    eq_(format,'In Progress')


def test_should_succeed_when_to_native_returns_an_enum_class_when_passing_in_a_status_value_value_with_api_data_has_enum_type_to_status_type():
        
    # Arrange

    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 2}),settings_str=settings_str)


    # Act

    status_type = StatusType(title='Status',as_enum=Status)
    status_type.to_native(column_value)
    format = status_type.to_native('Done')

    # Assert

    eq_(format,Status.done)

def test_should_succeed_when_to_native_returns_a_str_when_passing_in_a_int_value_to_status_type():

    # Arrange

    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 1}),settings_str=settings_str)

    # Act

    status_type = StatusType(title='Status')
    status_type.to_native(column_value)
    format = status_type.to_native(1)

    # Assert

    eq_(format,'In Progress')

def test_should_succeed_when_to_native_returns_a_str_when_passed_a_str_value_that_is_a_valid_label_index_int_to_status_type():

   # Arrange
    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 1}),settings_str=settings_str)
    
    # Act
    status_type = StatusType(title='Status')
    status_type.to_native(column_value)
    format = status_type.to_native("1")

    # Assert
    eq_(format,'In Progress')

def test_should_succeed_when_to_native_returns_a_str_when_passed_a_str_value_that_is_a_valid_label_to_status_type():

   # Arrange
    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 1}),settings_str=settings_str)
    
    # Act
    status_type = StatusType(title='Status')
    status_type.to_native(column_value)
    format = status_type.to_native('In Progress')

    # Assert
    eq_(format,'In Progress')

def test_should_suceed_when_to_native_return_enum_value_when_pass_str_and_status_type_has_enum_value_to_status_type():
           
    # Arrange

    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 2}),settings_str=settings_str)


    # Act

    status_type = StatusType(title='Status',as_enum=Status)
    status_type.to_native(column_value)
    format = status_type.to_native('Done')

    # Assert

    eq_(format,Status.done)

def test_should_suceed_when_to_native_return_enum_value_when_pass_enum_value_and_status_type_has_enum_value_to_status_type():
           
    # Arrange

    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 2}),settings_str=settings_str)


    # Act

    status_type = StatusType(title='Status',as_enum=Status)
    status_type.to_native(column_value)
    format = status_type.to_native(Status.done)

    # Assert

    eq_(format,Status.done)

@raises(ConversionError)
def test_should_succeed_when_to_native_raises_a_conversionerror_when_passed_either_an_invalid_int_or_str_to_status_type():

    # Arrange

    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 1}),settings_str=settings_str)
    status_type = StatusType(title='Status')
    status_type.to_native(column_value)


    # Act
    status_type.to_native('Not Done')

@raises(ConversionError)
def test_should_succeed_when_to_native_raises_a_conversionerror_when_passed_invalid_value_with_enum_class_to_status_type():
    
    # Arrange
    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 1}),settings_str=settings_str)
    status_type = StatusType(title='Status',as_enum=Status)
    status_type.to_native(column_value)


    # Act
    status_type.to_native('Not Done')

def test_should_succeed_when_to_primitive_returns_empty_dict_when_passed_in_a_none_to_status_type():
    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 1}),settings_str=settings_str)


    # Act
    status_type = StatusType(title='Status',as_enum=Status)
    status_type.to_native(column_value)
    format = status_type.to_primitive(None)
    # Assert
    eq_(format,{})

def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_in_a_str_value_to_status_type():
    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 1}),settings_str=settings_str)


    # Act
    status_type = StatusType(title='Status',as_enum=Status)
    status_type.to_native(column_value)
    format = status_type.to_primitive("Done")
    # Assert
    eq_(format,{'index': 2})

def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_in_a_str_or_enum_class_value__to_status_type():
    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 1}),settings_str=settings_str)


    # Act
    status_type = StatusType(title='Status',as_enum=Status)
    status_type.to_native(column_value)
    format = status_type.to_primitive(Status.done)
    # Assert
    eq_(format,{'index': 2})