from schematics.exceptions import ConversionError, DataError
from nose.tools import eq_,raises

from moncli import column_value as cv
from moncli.enums import ColumnType
from moncli.models import MondayModel
from moncli.types import TimelineType

import json
from datetime import datetime


def test_should_succeed_when_to_native_returns_a_timeline_when_passed_a_timeline_value_with_api_data():

    # Arrange
    id = 'timeline_1'
    column_type = ColumnType.timeline
    title = 'Timeline'
    from_date = '2021-09-01'
    to_date = '2021-10-01'
    value = json.dumps({'from': from_date, 'to': to_date})
    timeline_value = cv.create_column_value(column_type, id=id, title=title, value=value, settings_str='{}')

    # Act
    timeline_type = TimelineType(title='Timeline Column 1')
    value = timeline_type.to_native(timeline_value)

    # Assert
    eq_(value.from_date, datetime(2021, 9, 1))
    eq_(value.to_date, datetime(2021, 10, 1))


def test_should_succeed_when_to_native_returns_a_none_when_passed_none():

    # Arrange
    timeline_type = TimelineType(title='Timeline Column 2')

    # Act
    value = timeline_type.to_native(None)

    # Assert
    eq_(value, None)


def test_should_succeed_when_to_native_returns_a_timeline_when_passed_valid_import_dict():

    # Arrange
    timeline_type = TimelineType(title='Timeline Column 3')
    value = {'from': datetime(2021, 9, 1), 'to': datetime(2021, 10, 1)}

    # Act
    value = timeline_type.to_native(value)

    # Assert
    eq_(value.from_date, datetime(2021, 9, 1))
    eq_(value.to_date, datetime(2021, 10, 1))


@raises(ConversionError)
def test_should_succeed_when_to_native_raises_a_conversionerror_when_passed_an_invalid_import_dict():

    # Arrange
    timeline_type = TimelineType(title='Timeline Column 4')

    # Act
    timeline_type.to_native({'bad': 'dict'})


def test_should_succeed_when_to_primitive_returns_empty_dict_when_passed_a_none():

    # Arrange
    timeline_type = TimelineType(title='Timeline Column 5')

    # Act
    value = timeline_type.to_primitive(None)

    # Assert
    eq_(value,{})


def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_a_timeline_value():

    # Arrange
    timeline_type = TimelineType(title='Timeline Column 6')

    # Act
    timeline = cv.Timeline(datetime(2021, 9, 1), datetime(2021, 10, 1))
    value = timeline_type.to_primitive(timeline)

    # Assert

    eq_(value['from'], '2021-09-01')
    eq_(value['to'], '2021-10-01')


def test_should_succeed_when_to_primitive_returns_an_empty_dict_when_passed_a_timeline_with_a_none_for_fromdate_or_todate():

    # Arrange
    timeline_type = TimelineType(title='Timeline Column 7')

    # Act
    timeline = cv.Timeline(None, None)
    value = timeline_type.to_primitive(timeline)

    # Assert

    eq_(value, {})


@raises(DataError)
def test_should_succeed_when_validate_timeline_raises_a_validationerror_when_passed_a_timeline_with_a_fromdate_greater_than_todate():

    # Arrange
    class TestModel(MondayModel):
        timeline_type = TimelineType(title='Timeline Column 8')
    test = TestModel(id='item_id', name='Item Name')

    # Act
    test.timeline_type = cv.Timeline(datetime(2021, 10, 13), datetime(2021, 10, 12))
    test.validate()