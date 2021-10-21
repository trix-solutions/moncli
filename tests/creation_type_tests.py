import json
from datetime import datetime
from schematics.exceptions import ConversionError, DataError
from nose.tools import eq_,raises

from moncli import entities as en
from moncli.enums import ColumnType
from moncli.types import CreationLogType

def test_should_suceed_when_to_native_returns_a_local_datetime_when_passed_a_creationlogvalue_value_with_api_data_to_creationlog_type():

    # Arrange 
    column_value_data = {
        'id': 'creation_log_1',
        'title': 'Created',
        'text': '2021-10-04 19:20:32 UTC',
        'value': None
        }
    column_type = ColumnType.creation_log
    column_value = en.cv.create_column_value(column_type,**column_value_data)

    # Act
    creation_value_type = CreationLogType(title='Created')
    format = creation_value_type.to_native(column_value.value)

    # Assert
    eq_(format,{})
