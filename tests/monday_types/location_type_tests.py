import json
from nose.tools import eq_,raises
from unittest.mock import patch
from schematics.exceptions import ConversionError, DataError

from moncli import *
from moncli import entities as en
from moncli.enums import ColumnType
from moncli.models import MondayModel
from moncli import types as t


def test_should_succeed_when_to_native_returns_a_location_when_passed_a_locationvalue_value_with_api_data():
    
    # Arrange
    id = 'location_1'
    title = 'Location'
    column_type = ColumnType.location
    value=json.dumps({'lat': 26.930101, 'lng': -80.790198, 'address': "Home address"})
    column_value =  cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    location_type = t.LocationType(title='Location')
    value = location_type.to_native(column_value)

    # Assert
    eq_(value.lat,26.930101)
    eq_(value.lng,-80.790198)


def test_should_succeed_when_to_native_returns_a_location_when_passed_an_import_dict_value():
    
    # Arrange
    location_type = t.LocationType(title='Location')

    # Act
    value = location_type.to_native({'lat': 26.930101, 'lng': -80.790198, 'address': "Home address"})

    # Assert
    eq_(value.lat,26.930101)
    eq_(value.lng,-80.790198)
    

@raises(ConversionError)
def test_should_succeed_when_to_native_raises_a_conversionerror_when_passed_an_invalid_import_dict():
    
    # Arrange
    location_type = t.LocationType(title='Location')

    # Act
    location_type.to_native({'latitude': 26.930101, 'longitude': -80.790198, 'address': "Home address"})


def test_should_succeed_when_to_native_returns_none_when_passed_a_none():
    
    # Arrange
    location_type = t.LocationType(title='Location')

    # Act
    value = location_type.to_native(None)

    # Assert
    eq_(value,None)


def test_should_succeed_when_to_primitive_returns_empty_dict_when_passed_a_none():

    # Arrange
    location_type = t.LocationType(title='Location')

    # Act
    value = location_type.to_primitive(None)

    # Assert
    eq_(value,{})


def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_a_location_value_():
    
    # Arrange
    location_type = t.LocationType(title='Location')

    # Act
    value = location_type.to_primitive(cv.Location(lat = 26.930101, lng= -80.790198, address = "Home address"))

    # Assert
    eq_(value['lat'],26.930101)
    eq_(value['lng'],-80.790198)


def test_should_succeed_when_to_primitive_returns_empty_dict_when_passed_a_location_value_with_a_lat_or_lng_as_none():
    
    # Arrange
    location_type = t.LocationType(title='Location')

    # Act
    value = location_type.to_primitive(cv.Location(lat = 26.930101))

    # Assert
    eq_(value,{})

@raises(DataError)
def test_should_succeed_when_validate_location_raises_a_validation_error_when_passed_a_location_value_with_an_invalid_lat():
    
    # Arrange    
    class TestModel(MondayModel):
        value = t.LocationType(id='location_1')
    test = TestModel(id='item_id', name='Item Name')

    # Act
    test.value = cv.Location(lat=-99,lng=123.234)
    test.validate()

@raises(DataError)
def test_should_succeed_when_validate_location_raises_a_validationerror_when_passed_a_location_value_with_an_invalid_lng():
   
   # Arrange
    class TestModel(MondayModel):
        value = t.LocationType(id='location_1')
    test = TestModel(id='item_id', name='Item Name')

    # Act
    test.value = cv.Location(lat=-23,lng=223.234)
    test.validate()