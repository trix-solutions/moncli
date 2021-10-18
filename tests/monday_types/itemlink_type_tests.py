import json
from schematics.exceptions import ConversionError, DataError
from nose.tools import eq_,raises

from moncli import entities as en
from moncli.entities import column_value
from moncli.enums import ColumnType
from moncli.types import ItemLinkType


def test_should_succeed_when_to_native_returns_a_list_when_passed_an_itemlink_value_value_with_api_data_itemlink_type():
    
    # Arrange
    id = "itemlink_1"
    title = 'ItemLink'
    column_type = ColumnType.board_relation
    settings = json.dumps({'allowMultipleBoards': True, 'allowCreateReflectionColumn': False, 'boardIds': [1697598326]})
    value = json.dumps({'linkedPulseIds' : [{'linkedPulseId': 123456789 }]})
    column_value = en.cv.create_column_value(column_type,id=id,title=title,value=value,settings_str=settings)

    # Act
    itemlink_type = ItemLinkType(title='Item Link Column 1')
    value = itemlink_type.to_native(column_value.value)

    # Assert
    eq_(value, [123456789])


def test_should_succeed_when_to_native_returns_none_when_passed_a_none__itemlink_type():

    # Arrange
    itemlink_type = ItemLinkType(title='Item Link Column 2')

    # Act
    value = itemlink_type.to_native(None)

    # Assert
    eq_(value, [])


def test_should_succeed_when_to_native_returns_a_list_of_int_values_when_passed_a_list_of_int_or_str_values_and_multiple_values_is_true_itemlink_type():

    # Arrange
    itemlink_type = ItemLinkType(title='Item Link Column 3')
    value = [12345, '67890']

    # Act
    value = itemlink_type.to_native(value)

    # Assert
    eq_(value, [12345, 67890])


def test_should_succeed_when_to_native_returns_a_single_int_value_when_passed_an_int_or_str_and_multiple_values_is_false_itemlink_type():

    # Arrange
    itemlink_type = ItemLinkType(title='Item Link Column 4',multiple_values=False)
    int_value = 12345
    str_value = '12345'

    # Act
    value_1 = itemlink_type.to_native(int_value)
    value_2 = itemlink_type.to_native(str_value)


    # Assert
    eq_(value_1, 12345)
    eq_(value_2, 12345)

def test_should_succeed_when_to_primitive_returns_none_when_passed_a_none__itemlink_type():

    # Arrange
    itemlink_type = ItemLinkType(title='Item Link Column 2')

    # Act
    value_1 = itemlink_type.to_primitive(None)
    value_2 = itemlink_type.to_primitive([])

    # Assert
    eq_(value_1, {})
    eq_(value_2, {})


def test_should_succeed_when_to_primitive_returns_dict_when_passed__list_of_int_values_to_itemlink_type():

    # Arrange
    itemlink_type = ItemLinkType(title='Item Link Column 3')
    value = [12345, '67890']

    # Act
    value = itemlink_type.to_primitive(value)

    # Assert
    eq_(value['item_ids'], [12345, 67890])

def test_should_succeed_when_to_primitive_returns_dict_when_multiple_values_to_false_passed_list_of_int_values_to_itemlink_type():

    # Arrange
    itemlink_type = ItemLinkType(title='Item Link Column 3',multiple_values=False)
    value = 12345

    # Act
    value = itemlink_type.to_primitive(value)

    # Assert
    eq_(value['item_ids'], [12345])  

@raises(ConversionError)
def test_should_fail_when_passed_invalid_int_or_str_for_to_native_function_for_itemlink_type():

    # Arrange
    itemlink_type = ItemLinkType(title='Item Link Column 3')
    value =[ 'not a value']

    # Act
    itemlink_type.to_native(value)


@raises(ConversionError)
def test_should_fail_when_passed_invalid_int_or_str_for_to_primitve_function_for_itemlink_type():

    # Arrange
    itemlink_type = ItemLinkType(title='Item Link Column 3')
    value =[ 'not a value']

    # Act
    value = itemlink_type.to_primitive(value)
    eq_(value,{})