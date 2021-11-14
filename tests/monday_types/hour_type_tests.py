from schematics.exceptions import ConversionError, DataError, ValidationError
from nose.tools import eq_,raises

from moncli import column_value as cv
from moncli.enums import ColumnType
from moncli.models import MondayModel
from moncli.types import HourType


def test_should_succeed_when_to_native_returns_an_hour_when_passed_a_hourvalue_value_with_api_data_to_hour_type():
    # Arrange
    id = "hour"
    title = 'hour 1'
    column_type = ColumnType.hour
    column_value = cv.create_column_value(column_type,id=id,title=title)
    column_value.value = {'hour': 12, 'minute': 0}

    # Act
    hour_type = HourType(title=title)
    value = hour_type.to_native(column_value)

    # Assert
    eq_(value.hour,12)
    eq_(value.minute,0)


def test_should_succeed_when_to_native_returns_an_hour_when_passed_a_dict_value_to_hour_type():

    # Arrange

    hour_type = HourType(title='hour 1')

    # Act

    value = hour_type.to_native({'hour': 12, 'minute': 0})

    # Assert

    eq_(value.hour,12)
    eq_(value.minute,0)

@raises(ConversionError)
def test_should_succeed_when_to_native_raises_a_conversionerror_when_passed_an_invalid_dict_to_hour_type():
    
    # Arrange

    hour_type = HourType(title='hour 1')

    # Act

    value = hour_type.to_native({'hrs':12})


def test_should_succeed_when_to_native_returns_none_when_passed_none_to_hour_type():
    
    # Arrange

    hour_type = HourType(title='hour 1')

    #Act

    value = hour_type.to_native(None)

    # Assert

    eq_(value,None)


def test_should_succeed_when_to_primitive_returns_empty_dict_when_passed_a_none_to_hour_type():

    # Arrange

    hour_type = HourType(title='hour 1')

    #Act

    value = hour_type.to_primitive(None)

    # Assert
    
    eq_(value,{})


def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_an_hour_value_to_hour_type():

    # Arrange
    hour_type = HourType(title='hour 1')

    # Act

    value = hour_type.to_primitive(cv.Hour(12,0))
    
    # Assert

    eq_(value['hour'],12)
    eq_(value['minute'],0)

@raises(DataError)
def test_should_succeed_when_validate_hour_raises_a_validation_exception_when_passed_an_hour_with_hour_less_than_0_or_hour_greater_than_23_to_hour_type():
    
    class TestModel(MondayModel):
        value = HourType(id='hour 1')
    model = TestModel(id='item_id', name='Item Name')

    # Act
    model.value = cv.Hour(12,0)
    model.value.hour = 99

    model.validate()

@raises(DataError)
def test_should_succeed_when_validate_hour_raises_a_validation_exception_when_passed_an_hour_with_minute_less_than_0_or_minute_greater_than_59_to_hour_type():
    # Arrange
    class TestModel(MondayModel):
        value = HourType(id='hour 1')
    model = TestModel(id='item_id', name='Item Name')

    # Act
    model.value = cv.Hour(12,0)
    model.value.minute = 99

    model.validate()