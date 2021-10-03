import json
from datetime import datetime

from unittest.mock import patch
from nose.tools import eq_
from nose.tools.nontrivial import raises
from schematics.exceptions import ConversionError

from moncli import client, entities as en
from moncli.entities import column_value as cv
from moncli.enums import ColumnType
from moncli import types as t



def test_date_type_should_succeed_when_to_native_returns_a_datetime_when_passing_a_datevalue_value_with_api_data_to_date_type():

    # Arrange
    id = 'date_1'
    title = 'Date'
    column_type = ColumnType.date
    date = datetime(2021, 9, 29, 17, 48, 35)
    date = {'date': str(date.date()), 'time': str(date.time())}
    value = json.dumps(date)
    date_value = en.cv.create_column_value(column_type, id=id, title=title,value=value)

    # Act
    date_type = t.DateType(id='date_column_1')
    value = date_type.to_native(date_value)

    # Assert
    eq_(value, date_value.value)


def test_date_type_should_succeed_when_to_native_returns_a_datetime_when_passing_a_integer_or_string_value_to_date_type():

    # Arrange
    date_type = t.DateType(id='date_column_2', has_time=True)

    # Act
    value_1 = date_type.to_native(1632952115)
    value_2 = date_type.to_native('2021-09-29 17:48:35')

    # Assert
    eq_(value_1, datetime(2021, 9, 29, 17, 48, 35))
    eq_(value_2, datetime(2021, 9, 29, 17, 48, 35))


def test_date_type_should_succeed_when_to_native_returns_none_when_passing_none_to_date_type():

    # Arrange
    date_type = t.DateType(id='date_column_3')

    # Act
    value = date_type.to_native(None)

    # Assert
    eq_(value, None)


@raises(ConversionError)
def test_should_succeed_when_to_native_raisies_a_conversionerror_when_passed_a_str_with_an_invalid_date_format():
    # Arrange
    date_type = t.DateType(id='date_column_2')

    # Act
    date_type.to_native('999999999999')


@raises(ConversionError)
def test_should_succeed_when_to_native_raises_a_conversionerror_when_passed_a_str_with_an_invalid_time_format():
    # Arrange
    date_type = t.DateType(id='date_column_2', has_time=True)

    # Act
    date_type.to_native('2021-09-29 not:a:string')


def test_date_type_should_succeed_when_to_primitive_returns_empty_dict_when_passing_none_to_date_type():

    # Arrange
    date_type = t.DateType(id='date_column_4')

    # Act
    value = date_type.to_primitive(None)

    # Assert
    eq_(value, {})


def test_date_type_should_succeed_when_to_primitive_returns_export_dict_when_passing_datetime_value_to_date_type():

    # Arrange
    date_type = t.DateType(id='date_column_5')
    value = datetime(2021, 9, 29)

    # Act
    value = date_type.to_primitive(value)

    # Assert
    eq_(value['date'], '2021-09-29')
    eq_(value['time'], None)


def test_date_type_should_succeed_when_to_primitive_returns_export_dict_with_time_when_passing_datetime_value_and_has_time_is_true():

    # Arrange
    date_type = t.DateType(id='date_column_6', has_time=True)
    value = datetime(2021, 9, 29, 17, 48, 35)

    # Act
    value = date_type.to_primitive(value)

    # Assert
    eq_(value['date'], '2021-09-29')
    eq_(value['time'], '17:48:35')