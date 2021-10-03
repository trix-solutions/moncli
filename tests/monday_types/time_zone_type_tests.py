from schematics.exceptions import ValidationError
from nose.tools import eq_,raises

from moncli import entities as en
from moncli.enums import ColumnType
from moncli.types import TimeZoneType


def test_should_succeed_when_to_native_returns_a_str_when_passed_a_timezonevalue_value_with_api_data_to_world_clock_type():

    # Arrange
    id = "timezone"
    title = 'Time Zone Column 1'
    column_type = ColumnType.world_clock
    column_value = en.cv.create_column_value(column_type,id=id,title=title)
    column_value.value = 'America/New_York'

    # Act
    timezone_type = TimeZoneType(title=title)
    value = timezone_type.to_native(column_value)

    # Assert
    eq_(value,'America/New_York')

def test_should_succeed_when_to_native_returns_a_none_when_passed_a_none_to_world_clock_type():

    # Arrange
    timezone_type = TimeZoneType(title='Time Zone Column 1')

    # Act
    timezone_value = timezone_type.to_native(None)

    # Assert
    eq_(timezone_value,None)


def test_should_succeed_when_to_primitive_returns_an_empty_dict_when_passed_a_none_to_world_clock_type():

    # Arrange
    timezone_type = TimeZoneType(title='Time Zone Column 1')

    # Act
    timezone_value = timezone_type.to_primitive(None)

    # Assert
    eq_(timezone_value,{})

def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_in_a_str_timezone_value_to_world_clock_type():

    # Arrange
    id = "timezone"
    title = 'Time Zone Column 1'
    column_type = ColumnType.world_clock
    column_value = en.cv.create_column_value(column_type,id=id,title=title)
    column_value.value = 'America/New_York'

    # Act
    timezone_type = TimeZoneType(title=title)
    value = timezone_type.to_primitive(column_value)

    # Assert
    eq_(value['timezone'],'America/New_York')

@raises(ValidationError)
def test_timezone_type_should_raise_validation_error_when_validate_timezone_receives_invalid_timezone_str():

    # Arrange
    timezone_type = TimeZoneType(id='timezone_type_1')

    # Act
    timezone_type.validate_timezone(value='Invalid/Timezone')
