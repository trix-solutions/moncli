from datetime import datetime, timezone

from nose.tools import eq_, raises

from moncli import entities as en, error as e
from moncli.enums import *


def test_should_create_last_updated_column_value_with_datetime_value_using_input_api_data():

    # Arrange
    value = datetime(2021, 10, 4, 19, 45, 20, tzinfo=timezone.utc)
    column_value_data = {
        'id': 'last_updated_1',
        'title': 'Last Updated',
        'text': datetime.strftime(value, '%Y-%m-%d %H:%M:%S %Z'),
        'value': None
    }
    column_type = ColumnType.last_updated

    # Act
    column_value = en.cv.create_column_value(column_type, **column_value_data)

    # Assert
    eq_(column_value.value, value.astimezone(datetime.now().tzinfo))


@raises(e.ColumnValueError)
def test_should_raise_columnvalueerror_when_trying_to_set_a_valuet_to_create_last_updated():

    # Arrange
    column_value_data = {
        'id': 'last_updated_1',
        'title': 'Last Updated',
        'text': '2021-10-04 19:45:20 UTC',
        'value': None
    }
    column_type = ColumnType.last_updated
    column_value = en.cv.create_column_value(column_type,**column_value_data)

    # Act
    column_value.value = None


@raises(e.ColumnValueError)
def test_shoucl_raise_columnvalueerror_when_calling_to_format_create_last_updated():

    # Arrange
    column_value_data = {
        'id': 'last_updated_1',
        'title': 'Last Updated',
        'text': '2021-10-04 19:45:20 UTC',
        'value': None
    }
    column_type = ColumnType.last_updated
    column_value = en.cv.create_column_value(column_type,**column_value_data)


    # Act 
    column_value.format() 