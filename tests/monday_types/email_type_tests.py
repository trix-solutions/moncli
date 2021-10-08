from schematics.exceptions import ConversionError, DataError, ValidationError
from nose.tools import eq_,raises

from moncli import entities as en
from moncli.enums import ColumnType
from moncli.models import MondayModel
from moncli.types import EmailType
from moncli.entities.column_value import Email


def test_should_succeed_when_to_native_returns_a_email_when_passing_in_a_emailvalue_value_with_api_data_to_email_type():
    # Arrange
    id = "email"
    title = 'email 1'
    column_type = ColumnType.email
    column_value = en.cv.create_column_value(column_type,id=id,title=title)
    column_value.value = {'email': 'info@example.com', 'text': 'example email'}

    # Act
    email_type = EmailType(title=title)
    value = email_type.to_native(column_value)

    # Assert
    eq_(value.email,'info@example.com')
    eq_(value.text, 'example email')


def test_should_succeed_when_to_native_returns_a_email_when_passed_a_valid_import_dict_to_email_type():
    
    # Arrange

    email_type = EmailType(title='email 1')

    # Act

    value = email_type.to_native({'email': 'info@example.com', 'text': 'example email'})

    # Assert
    eq_(value.email,'info@example.com')
    eq_(value.text, 'example email')

@raises(ConversionError)
def test_should_succeed_when_to_native_raises_a_conversionerror_when_passed_an_invalid_import_dict_to_email_type():

    # Arrange

    email_type = EmailType(title='email 1')

    # Act

    email_type.to_native({'invalid': 'dict'})


def test_should_succeed_when_to_primitive_returns_empty_dict_when_passed_a_none_to_email_type():

    # Arrange

    email_type = EmailType(title='email 1')

    # Act

    value = email_type.to_primitive(None)

    # Assert
    eq_(value,{})


def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_a_email_value_to_email_type():
    # Arrange

    email_type = EmailType(title='email 1')

    # Act
    email = Email(email='someone@me.com', text='That is me!')
    value = email_type.to_primitive(email)

    # Assert

    eq_(value['email'],'someone@me.com')
    eq_(value['text'], 'That is me!')

@raises(DataError)
def test_should_succeed_when_validate_email_raises_a_validation_error_when_passed_an_invalid_email_value_to_email_type():

   # Arrange
    class TestModel(MondayModel):
        value = EmailType(id='email 1')
    test = TestModel(id='item_id', name='Item Name')

    # Act
    test.value = Email(email='this.isnot.an.email...',text='not a valid email')
    test.validate()