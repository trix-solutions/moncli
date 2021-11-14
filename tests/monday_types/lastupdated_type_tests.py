import json
from datetime import datetime,timezone
from nose.tools import eq_

from moncli import column_value as cv
from moncli.enums import ColumnType
from moncli.types import LastUpdatedType

def test_should_suceed_when_to_native_returns_a_local_datetime_when_passed_a_last_updatedvalue_value_with_api_data_to_last_updated_type():

    # Arrange 
    value = datetime(2021, 10, 4, 19, 45, 20, tzinfo=timezone.utc)
    column_value_data = {
        'id': 'last_updated_1',
        'title': 'Last Updated',
        'text': datetime.strftime(value, '%Y-%m-%d %H:%M:%S %Z'),
        'value': None
        }
    column_type = ColumnType.creation_log
    column_value = cv.create_column_value(column_type,**column_value_data)

    # Act
    creation_value_type = LastUpdatedType(title='Last Updated')
    format = creation_value_type.to_native(column_value.value)

    # Assert
    eq_(format,value.astimezone(datetime.now().tzinfo))


