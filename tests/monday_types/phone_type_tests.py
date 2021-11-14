import json
from nose.tools import eq_,raises
from unittest.mock import patch
from schematics.exceptions import ConversionError, DataError

from moncli import *
from moncli import entities as en
from moncli.enums import ColumnType
from moncli.models import MondayModel
from moncli import types as t


def test_should_succeed_when_to_native_returns_a_phone_when_passed_a_phonevalue_value_with_api_data_to_phone_type():
    
    # Arrange
    id = "phone"
    title = 'phone 1'
    column_type = ColumnType.phone
    value = json.dumps({'phone': '+15083658469', 'countryShortName': 'US'})
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    phone_type = t.PhoneType(title=title)
    value = phone_type.to_native(column_value)

    # Assert
    eq_(value.phone,'+15083658469')
    eq_(value.code, 'US')


def test_should_succeed_when_to_native_returns_a_phone_when_passed_a_valid_import_dict_value_to_phone_type():
    
    # Arrange
    phone_type = t.PhoneType(title='phone 1')
    
    # Act
    value = phone_type.to_native({'phone': '+15083658469', 'code': 'US'})

    # Assert
    eq_(value.phone,'+15083658469')
    eq_(value.code, 'US')


def test_should_succeed_when_to_native_returns_a_none_when_passed_a_none_to_phone_type():
    
    # Arrange
    phone_type = t.PhoneType(title='phone 1')
    
    # Act
    value = phone_type.to_native(None)

    # Assert
    eq_(value,None)


@raises(ConversionError)
def test_should_succeed_when_to_native_raises_a_conversionerror_when_passed_an_invalid_import_dict_value_to_phone_type():

   # Arrange
    phone_type = t.PhoneType(title='phone 1')
    
    # Act
    phone_type.to_native({'invalid': 'phone'})

def test_should_return_phone_value_when_passed_simple_string_for_to_native_to_phone_type():

    # Arrange
    phone_type = t.PhoneType(title='phone 1')
    
    # Act
    value = phone_type.to_native('+15083658469 US')

    # Assert
    eq_(value.phone,'+15083658469')
    eq_(value.code, 'US')

def test_should_succeed_when_to_primitive_returns_empty_dict_when_passed_a_none_to_phone_type():

    # Arrange
    phone_type = t.PhoneType(title='phone 1')
    
    # Act
    value = phone_type.to_primitive(None)

    # Assert
    eq_(value,{})


def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_a_phone_value__to_phone_type():
    
    # Arrange
    phone_type = t.PhoneType(title='phone 1')
    
    # Act
    value = phone_type.to_primitive(cv.Phone(phone = '+15083658469', code= 'US'))

    # Assert
    eq_(value['phone'],'+15083658469')
    eq_(value['countryShortName'], 'US')


def test_should_succeed_when_to_primitive_returns_empty_dict_when_passed_a_phone_with_phone_or_code_as_none_to_phone_type():
    
    # Arrange
    phone_type = t.PhoneType(title='phone 1')
    
    # Act
    value = phone_type.to_primitive(cv.Phone(phone = '+15083658469', code= None))

    # Assert
    eq_(value,{})


@raises(DataError)
def test_should_succeed_when_validate_country_code_raises_a_validation_error_when_passed_an_invalid_phonecode_value_to_phone_type():
    
    # Arrange
    class TestModel(MondayModel):
        value = t.PhoneType(id='phone')
    test = TestModel(id='item_id', name='Item Name')

    # Act
    test.value = '1234 zz'
    test.validate()