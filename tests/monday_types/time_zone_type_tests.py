import json
import pytz
from pytz.exceptions import UnknownTimeZoneError
from schematics.exceptions import ValidationError,DataError
from nose.tools import eq_,raises
from unittest.mock import patch

from moncli import entities as en
from moncli import types as t
from moncli import client
from moncli.enums import ColumnType
from moncli.models import MondayModel


@patch.object(en.Item,'get_column_values')
@patch('moncli.api_v2.get_items')
def test_should_succeed_when_to_native_returns_a_str_when_passed_a_timezonevalue_value_with_api_data_to_world_clock_type(get_items,get_column_values):

    # Arrange
    id = "timezone"
    title = 'Time Zone Column 1'
    column_type = ColumnType.world_clock
    column_value = en.cv.create_column_value(column_type,id=id,title=title)
    column_value.value = 'America/New_York'
    get_items.return_value = [{'id': '1697598380', 'name': 'edited item'}]
    get_column_values.return_value = [column_value]
    item = client.get_items()[0]
    column_value = item.get_column_values()[0]

    # Act
    timezone_type = t.TimeZoneType(title=title)
    value = timezone_type.to_native(column_value)

    # Assert
    eq_(value,'America/New_York')

def test_should_succeed_when_to_native_returns_a_none_when_passed_a_none_to_world_clock_type():

    # Arrange
    timezone_type = t.TimeZoneType(title='Time Zone Column 1')

    # Act
    timezone_value = timezone_type.to_native(None)

    # Assert
    eq_(timezone_value,None)


def test_should_succeed_when_to_primitive_returns_an_empty_dict_when_passed_a_none_to_world_clock_type():

    # Arrange
    timezone_type = t.TimeZoneType(title='Time Zone Column 1')

    # Act
    timezone_value = timezone_type.to_primitive(None)

    # Assert
    eq_(timezone_value,{})

@patch.object(en.Item,'get_column_values')
@patch('moncli.api_v2.get_items')
def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_in_a_str_timezone_value_to_world_clock_type(get_items,get_column_values):

    # Arrange
    id = "timezone"
    title = 'Time Zone Column 1'
    column_type = ColumnType.world_clock
    column_value = en.cv.create_column_value(column_type,id=id,title=title)
    column_value.value = 'America/New_York'
    get_items.return_value = [{'id': '1697598380', 'name': 'edited item'}]
    get_column_values.return_value = [column_value]
    item = client.get_items()[0]
    column_value = item.get_column_values()[0]

    # Act
    timezone_type = t.TimeZoneType(title=title)
    value = timezone_type.to_primitive(column_value)

    # Assert
    eq_(value['timezone'],'America/New_York')

@patch.object(en.Item,'get_column_values')
@patch('moncli.api_v2.get_items')
@raises(DataError)
def test_should_fail_when_to_primitive_raises_a_validation_error_when_passed_a_str_timezone_that_is_invalid_to_world_clock_type(get_items,get_column_values):

    # Arrange
    id = "timezone"
    title = 'Time Zone Column 1'
    column_type = ColumnType.world_clock
    column_value = en.cv.create_column_value(column_type,id=id,title=title)
    column_value.value = 'Invalid/Timezone'
    get_items.return_value = [{'id': '1697598380', 'name': 'edited item'}]
    get_column_values.return_value = [column_value]
    item = client.get_items()[0]
    column_value = item.get_column_values()[0]

    # Act
    tz = TimeZoneModel(item)
    tz.timezone = column_value.value
    tz.validate()

class TimeZoneModel(MondayModel):
    timezone = t.TimeZoneType(title='Time Zone Column 1')
    def validate_timezone(self, value):
        try:
            pytz.timezone(value)
        except (UnknownTimeZoneError):
            raise ValidationError('Unknown time zone "{}".'.format(value))
