from nose.tools import eq_,raises
from unittest.mock import patch
from schematics.exceptions import ConversionError

from moncli import *
from moncli import entities as en
from moncli.enums import ColumnType
from moncli import types as t


@patch.object(en.Item,'get_column_values')
@patch('moncli.api_v2.get_items')
def test_should_succeed_when_to_native_returns_an_int_when_passed_a_rating_value_value_with_api_data_to_rating_type(get_items,get_column_values):

    # Arrange
    id = "rating"
    title = 'Rating 1'
    column_type = ColumnType.rating
    column_value = en.cv.create_column_value(column_type,id=id,title=title)
    column_value.value = 1
    get_items.return_value = [{'id': '1697598380', 'name': 'edited item'}]
    get_column_values.return_value = [column_value]
    item = client.get_items()[0]
    column_value = item.get_column_values()[0]

    # Act
    rating_type = t.RatingType(title=title)
    value = rating_type.to_native(column_value)

    # Assert
    eq_(value,1)


def test_should_succeed_when_to_native_returns_an_int_when_passed_a_str_value_to_rating_type():


    rating_value = en.cv.create_column_value(ColumnType.text,id="text1",title="text")
    rating_value.value = "1"
    rating_type = t.RatingType(id=1)

    # Act
    value = rating_type.to_native(rating_value.value)

    # Assert
    eq_(value,1)



def test_should_succeed_when_to_native_returns_a_none_when_passed_a_none_to_rating_type():
    
    rating_value = en.cv.create_column_value(ColumnType.text,id="text1",title="text")
    rating_value.value = None
    rating_type = t.RatingType(id=1)

    # Act
    value = rating_type.to_native(rating_value.value)

    # Assert
    eq_(value,rating_value.value)


@raises(ConversionError)
def test_should_succeed_when_to_native_raises_a_conversion_error_when_passed_an_invalid_str_to_rating_type():
    rating_value = en.cv.create_column_value(ColumnType.text,id="text1",title="text")
    rating_value.value = "string type"
    rating_type = t.RatingType(id=1)

    # Act
    rating_type.to_native(rating_value.value)

    



def test_should_succeed_when_to_primitive_returns_an_empty_dict_when_passed_in_a_none_to_rating_type():
    rating_value = en.cv.create_column_value(ColumnType.text,id="text1",title="text")
    rating_value.value = None
    rating_type = t.RatingType(id=1)

    # Act
    value = rating_type.to_primitive(rating_value.value)

    # Assert
    eq_(value,{})


def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_in_an_int_value_to_rating_type():
    rating_value = en.cv.create_column_value(ColumnType.text,id="text1",title="text")
    rating_value.value = 1
    rating_type = t.RatingType(id=1)

    # Act
    value = rating_type.to_primitive(rating_value.value)

    # Assert
    eq_(value['rating'],1)