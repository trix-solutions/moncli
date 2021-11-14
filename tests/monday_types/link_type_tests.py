import json
from schematics.exceptions import DataError
from nose.tools import eq_,raises

from moncli import column_value as cv
from moncli.enums import ColumnType
from moncli.models import MondayModel
from moncli.types import LinkType


def test_should_succeed_when_to_native_returns_a_link_when_passed_a_link_value_value_with_api_data_to_link_type():
    
    # Arrange
    id = "link"
    title = 'link 1'
    column_type = ColumnType.link
    value = json.dumps({'url': 'https://www.google.com', 'text': 'Google'})
    column_value = cv.create_column_value(column_type,id=id,title=title,value=value)

    # Act
    link_type = LinkType(title=title)
    value = link_type.to_native(column_value)

    # Assert
    eq_(value.url, 'https://www.google.com',)
    eq_(value.text, 'Google')


def test_should_succeed_when_to_native_returns_a_link_when_passed_a_dict_value_to_link_type():

    # Arrange
    link_type = LinkType(title='link 1')
    
    # Act
    value = link_type.to_native({'url': 'https://www.google.com', 'text': 'Google'})

    # Assert
    eq_(value.url, 'https://www.google.com',)
    eq_(value.text, 'Google')


def test_should_succeed_when_to_native_returns_a_none_when_passed_a_none_to_link_type():
    
    # Arrange
    link_type = LinkType(title='link 1')
    
    # Act
    value = link_type.to_native(None)

    # Assert
    eq_(value,None)


def test_should_succeed_when_to_primitive_returns_an_empty_dict_when_passed_in_a_none_to_link_type():
    
    # Arrange
    link_type = LinkType(title='link 1')
    
    # Act
    value = link_type.to_primitive(None)

    # Assert
    eq_(value,{})


def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_in_a_link_value_to_link_type():
    
    # Arrange
    link_type = LinkType(title='link 1')
    
    # Act
    value = link_type.to_primitive(cv.Link(url='https://www.google.com', text= 'Google'))

    # Assert
    eq_(value['url'], 'https://www.google.com',)
    eq_(value['text'], 'Google')


def test_should_succeed_when_to_primitive_returns_an_empty_dict_when_passed_a_link_with_no_url_value_to_link_type():
    
    # Arrange
    link_type = LinkType(title='link 1')
    
    # Act
    value = link_type.to_primitive(cv.Link(text= 'Google'))

    # Assert
    eq_(value,{})


@raises(DataError)
def test_should_succeed_when_validate_link_raises_a_validationerror_when_passed_a_link_with_an_invalid_url_value_to_link_type():
    
    # Arrange
    class TestModel(MondayModel):
        value = LinkType(id='link')
    test = TestModel(id='item_id', name='Item Name')

    # Act
    test.value = cv.Link(url='not a valid url')
    test.validate()