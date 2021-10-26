import json
from datetime import datetime
from schematics.exceptions import ConversionError
from nose.tools import eq_,raises

from moncli import entities as en
from moncli.enums import ColumnType
from moncli.types import WeekType


def test_should_succeed_when_to_native_returns_a_week_when_passing_in_a_weekvalue_value_with_api_data_to_week_value():
    
    # Arrange
    id = "week"
    title = 'week 1'
    column_type = ColumnType.week
    value = json.dumps({ 
        'week': {
            'startDate': '2021-09-20',
            'endDate': '2021-09-26'
        }
    })
    column_value = en.cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    week_type = WeekType(title=title)
    value = week_type.to_native(column_value)

    # Assert
    eq_(value.start, datetime(2021, 9, 20, 0, 0))
    eq_(value.end, datetime(2021, 9, 26, 0, 0))


def test_should_succeed_when_to_native_returns_a_week_when_passed_an_import_dict_value_to_week_value():
    
    # Arrange
    week_type = WeekType(title='week 1')
   
    # Act
    value = week_type.to_native({'start': datetime(2021, 9, 20, 0, 0),
                                'end': datetime(2021, 9, 26, 0, 0)})

    # Assert
    eq_(value.start, datetime(2021, 9, 20, 0, 0))
    eq_(value.end, datetime(2021, 9, 26, 0, 0))


@raises(ConversionError)
def test_should_succeed_when_to_native_raises_a_conversion_error_when_passed_an_invalid_import_dict_to_week_value():
   
    # Arrange
    week_type = WeekType(title='week 1')

    # Act
    week_type.to_native({'invalid':'dict'})


def test_should_succeed_when_to_native_returns_none_when_passed_a_none_to_week_value():
    
    # Arrange
    week_type = WeekType(title='week 1')

   # Act
    value = week_type.to_native(None)

     # Assert
    eq_(value, None)


def test_should_succeed_when_to_primitive_returns_empty_dict_when_passed_in_a_none_to_week_value():
    
    # Arrange
    week_type = WeekType(title='week 1')

   # Act
    value = week_type.to_primitive(None)

     # Assert
    eq_(value, {})


def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_in_a_week_value_to_week_value():
    
    # Arrange
    week_type = WeekType(title='week 1')
    week = en.cv.Week(
        start = datetime(2021, 9, 20, 0, 0),
        end = datetime(2021, 9, 26, 0, 0))

    # Act
    value = week_type.to_primitive(week)['week']
                                        
    # Assert
    eq_(value['startDate'], '2021-09-20'),
    eq_(value['endDate'], '2021-09-26')


def test_should_succeed_when_to_primitive_returns_empty_dict_when_passed_a_week_value_with_a_none_start_or_end_to_week_value():
     # Arrange

    week_type = WeekType(title='week 1')

   # Act
    value = week_type.to_primitive(en.cv.Week(start = None,end = datetime(2021, 9, 26, 0, 0)))

     # Assert
    eq_(value, {})