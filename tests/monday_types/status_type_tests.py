import json
from schematics.exceptions import ConversionError, DataError
from nose.tools import eq_,raises
from unittest.mock import patch
from enum import Enum

from moncli import entities as en
from moncli import client
from moncli.entities import board
from moncli.enums import ColumnType
from moncli.models import MondayModel
from moncli.types import StatusType

# default class and data mapping declaration for common use
class Status(Enum):
    ready = 0
    in_progress = 1
    done = 2

data_mapping = {
            'Ready': Status.ready,
            'In Progress': Status.in_progress,
            'Done': Status.done
            }


def test_should_succeed_when_to_native_returns_a_str_when_passing_in_a_statusvalue_value_with_api_data_to_status_type():
    
    # Arrange
    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 1}),settings_str=settings_str)


    # Act
    status_type = StatusType(title='Status')
    format = status_type.to_native(column_value)

    # Assert
    eq_(format,'In Progress')


def test_should_succeed_when_to_native_returns_an_enum_class_when_passing_in_a_status_value_value_with_api_data_and_statustype_has_data_mapping_to_status_type():
    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 1}),settings_str=settings_str)


    # Act
    status_type = StatusType(title='Status',data_mapping=data_mapping)
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

def test_should_succeed_when_to_native_returns_an_enum_class_when_passing_in_a_str_or_int_value_and_statustype_has_data_mapping_to_status_type():

    # Arrange
    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 1}),settings_str=settings_str)
    status_type = StatusType(title='Status',data_mapping=data_mapping)
    
    # Act
    status_type.to_native(column_value)
    format = status_type.to_native(1)

    # Assert
    eq_(format,Status.in_progress)

@raises(ConversionError)
def test_should_succeed_when_to_native_raises_a_conversionerror_when_passed_either_an_invalid_int_or_str_to_status_type():
    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 1}),settings_str=settings_str)


    # Act
    status_type = StatusType(title='Status',data_mapping=data_mapping)
    status_type.to_native(column_value)
    format = status_type.to_native('Not Done')

def test_should_succeed_when_to_primitive_returns_empty_dict_when_passed_in_a_none_to_status_type():
    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 1}),settings_str=settings_str)


    # Act
    status_type = StatusType(title='Status',data_mapping=data_mapping)
    status_type.to_native(column_value)
    format = status_type.to_primitive(None)
    # Assert
    eq_(format,{})


def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_in_a_str_or_enum_class_value__to_status_type():
    settings_str = json.dumps({'labels': {'0': 'Ready','1':'In Progress','2': 'Done'}})
    column_value = en.cv.create_column_value(ColumnType.status, id='status', title='Status 1',value=json.dumps({'index': 1}),settings_str=settings_str)


    # Act
    status_type = StatusType(title='Status',data_mapping=data_mapping)
    status_type.to_native(column_value)
    format = status_type.to_primitive(Status.done)
    # Assert
    eq_(format,{'index': 2})