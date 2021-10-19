import json

from nose.tools import eq_, raises

from moncli import entities as en, error as e
from moncli.enums import *


def test_should_create_creation_log_column_value_with_datetime_value_using_input_api_data():

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
    format = str(column_value.value)

    # Assert
    eq_(format,'2021-10-04 19:20:32+05:30')


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
    column_value = en.cv.create_column_value(column_type, **column_value_data)

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
    column_value = en.cv.create_column_value(column_type, **column_value_data)


    # Act 
    column_value.format()