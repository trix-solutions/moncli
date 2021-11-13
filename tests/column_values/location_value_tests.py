import json

from nose.tools import eq_, raises

from moncli import column_value as cv, error as e
from moncli.enums import *

def test_should_create_a_location_column_with_no_api_input_data():

    # Arrange
    id = 'location_1'
    title = 'Location'
    column_type = ColumnType.location
    value = None
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    location = column_value.format()

    # Assert
    eq_(location, cv.COMPLEX_NULL_VALUE)


def test_should_create_a_location_column_with_api_input_data():

    # Arrange
    id = 'location_1'
    title = 'Location'
    column_type = ColumnType.location
    value = json.dumps({
            'lat': 0.0,
            'lng': 0.0,
            'address': 'Origin of Earth'
            })
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    location = column_value.format()

    # Assert
    eq_(location['lat'],0.0)
    eq_(location['lng'],0.0)
    eq_(location['address'],'Origin of Earth')


def test_should_return_none_when_location_value_set_to_none():

    # Arrange
    id = 'location_1'
    title = 'Location'
    column_type = ColumnType.location
    value = None
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    column_value.value = None

    # Assert
    eq_(column_value.value, None)


def test_should_return_location_value_when_location_column_value_set_to_location_value():

    # Arrange
    id = 'location_1'
    title = 'Location'
    column_type = ColumnType.location
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value = cv.Location(50.0,50.0,'Some place')
    location_value = cv.Location(50.0,50.0,'Some place')

    # Assert
    eq_(column_value.value.lat, location_value.lat )
    eq_(column_value.value.lng, location_value.lng )
    eq_(column_value.value.address, location_value.address )


def test_should_return_location_value_when_location_value_set_to_dict_value():

    # Arrange

    id = 'location_1'
    title = 'Location'
    column_type = ColumnType.location
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act

    column_value.value = {'lat': 50.0, 'lng': 50.0, 'address': 'Some place'}
    location_value = cv.Location(50.0,50.0,'Some place')

    # Assert
    eq_(column_value.value.lat, location_value.lat )
    eq_(column_value.value.lng, location_value.lng )
    eq_(column_value.value.address, location_value.address )


@raises(e.ColumnValueError)
def test_should_fail_to_set_location_column_value_when_invalid_dict_is_passed():

    # Arrange
    id = 'location_1'
    title = 'Location'
    column_type = ColumnType.location
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value = {'latitude': 50.0, 'longitude': 50.0}

@raises(e.ColumnValueError)
def test_should_fail_to_set_location_column_value_when_invalid_str_is_passed_with_no_lat_or_lng_value():

    # Arrange
    id = 'location_1'
    title = 'Location'
    column_type = ColumnType.location
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value = "50.0"

@raises(e.ColumnValueError)
def test_should_fail_to_set_location_column_value_when_str_is_passed_with_invalid_lat_or_lng_value():

    # Arrange
    id = 'location_1'
    title = 'Location'
    column_type = ColumnType.location
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value = "this is not a location column value"

def test_should_return_location_value_when_valid_str_set_to_location_column_value():

    # Arrange

    id = 'location_1'
    title = 'Location'
    column_type = ColumnType.location
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act

    column_value.value = '50.0 50.0 Some place'
    location_value ='50.0 50.0 Some place'.split(" ",3)

    # Assert
    eq_(column_value.value.lat, 50.0)
    eq_(column_value.value.lng, 50.0 )
    eq_(column_value.value.address, "Some place")

def test_should_return_null_value_when_none_is_set_to_location_value():

    # Arrange
    id = 'location_1'
    title = 'Location'
    column_type = ColumnType.location
    value = json.dumps({
            'lat': 0.0,
            'lng': 0.0,
            'address': 'Origin of Earth'
            })
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    column_value.value = None
    location = column_value.format()

    # Assert
    eq_(location, cv.COMPLEX_NULL_VALUE)


def test_should_return_dict_value_when_location_value_is_set_to_location_column_value():

    # Arrange
    id = 'location_1'
    title = 'Location'
    column_type = ColumnType.location
    value = {
            'lat': 0.0,
            'lng': 0.0,
            'address': 'Origin of Earth'
            }
    column_value = cv.create_column_value(column_type,id=id,title=title)

    # Act
    column_value.value = value
    location = column_value.format()

    # Assert
    eq_(location['lat'],0.0)
    eq_(location['lng'],0.0)
    eq_(location['address'],'Origin of Earth') 