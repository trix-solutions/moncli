import json
from nose.tools import eq_,raises
from schematics.exceptions import ConversionError, DataError

from moncli import *
from moncli import entities as en
from moncli.enums import ColumnType
from moncli.models import MondayModel
from moncli import types as t

def test_should_succeed_when_to_native_returns_a_country_when_passing_in_a_country_value_value_with_api_data_to_country_type():
    
    # Arrange
    id = 'country_1'
    title = 'Country'
    column_type = ColumnType.country
    value = json.dumps({'countryName': 'India', 'countryCode': 'IN'})
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    country_type = t.CountryType(title='Country')
    format  = country_type.to_native(column_value)

    # Assert
    eq_(format.name,'India')
    eq_(format.code,'IN')


def test_should_succeed_when_to_native_returns_none_when_passed_a_none_to_country_type():
    
    # Arrange
    country_type = t.CountryType(title='Country')

    # Act
    format  = country_type.to_native(None)

    # Assert
    eq_(format,None)


def test_should_succeed_when_to_native_returns_a_country_when_passed_a_valid_import_dict_value_to_country_type():

    # Arrange
    country_type = t.CountryType(title='Country')

    # Act
    format  = country_type.to_native({'country': 'India', 'code': 'IN'})

    # Assert
    eq_(format.name, "India")
    eq_(format.code,'IN')


@raises(ConversionError)
def test_should_succeed_when_to_native_raises_a_conversionerror_when_passed_an_invalid_import_dict_to_country_type():

    # Arrange
    country_type = t.CountryType(title='Country')

    # Act
    country_type.to_native({'invalid': 'India', 'name': 'IN'})


def test_should_succeed_when_to_primitive_returns_an_empty_dict_when_passed_in_a_none_to_country_type():

    # Arrange
    country_type = t.CountryType(title='Country')

    # Act
    format  = country_type.to_primitive(None)

    # Assert
    eq_(format,{})


def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_a_country_value_to_country_type():

    # Arrange
    country_type = t.CountryType(title='Country')

    # Act
    format = country_type.to_primitive(cv.Country('India', 'IN'))

    # Assert
    eq_(format['countryName'],'India')
    eq_(format['countryCode'],'IN')


def test_should_succeed_when_to_primitive_returns_empty_dict_when_passed_a_country_value_with_a_name_or_code_as_none_to_country_type():

    # Arrange
    country_type = t.CountryType(title='Country')

    # Act
    format = country_type.to_primitive(cv.Country(name=None, code='IN'))

    # Assert
    eq_(format,{})


@raises(DataError)
def test_should_succeed_when_validate_country_raises_a_validationerror_when_passed_a_country_with_an_invalid_name_to_country_type():
    
    # Arrange
    test.country_value= cv.Country('IINDA','IN')
    test.country_value.name = ''

    # Act
    test.validate()


@raises(DataError)
def test_should_succeed_when_validate_country_raises_a_validationerror_when_passed_a_country_with_an_invalid_code_to_country_type():

    # Arrange
    test.country_value= cv.Country('INDIA','INDYA')

    # Act
    test.validate()


class TestModel(MondayModel):
        country_value = t.CountryType(id='phone')
test = TestModel(id='item_id', name='Item Name')