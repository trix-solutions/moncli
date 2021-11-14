from datetime import datetime, timezone

from nose.tools import eq_, raises

from moncli import column_value as cv, error as e
from moncli.enums import *


def test_should_create_creation_log_column_value_with_datetime_value_using_input_api_data():

    # Arrange
    value = datetime(2021, 10, 4, 19, 20, 32, tzinfo=timezone.utc)
    column_value_data = {
        'id': 'creation_log_1',
        'title': 'Created',
        'text': datetime.strftime(value, '%Y-%m-%d %H:%M:%S %Z'),
        'value': None
        }
    column_type = ColumnType.creation_log
    column_value = cv.create_column_value(column_type,**column_value_data)

    # Assert
    eq_(column_value.value, value.astimezone(datetime.now().tzinfo))


@raises(e.ColumnValueError)
def test_should_raise_columnvalueerror_when_trying_to_set_a_value_to_creation_log():

    # Arrange
    column_value_data = {
        'id': 'creation_log_1',
        'title': 'Created',
        'text': '2021-10-04 19:20:32 UTC',
        'value': None
        }
    column_type = ColumnType.creation_log
    column_value = cv.create_column_value(column_type, **column_value_data)

    # Act
    column_value.value = None


@raises(e.ColumnValueError)
def test_should_raise_columnvalueerror_when_calling_format_for_creation_log():

    # Arrange
    column_value_data = {
        'id': 'creation_log_1',
        'title': 'Created',
        'text': '2021-10-04 19:20:32 UTC',
        'value': None
        }
    column_type = ColumnType.creation_log
    column_value = cv.create_column_value(column_type, **column_value_data)


    # Act 
    column_value.format()