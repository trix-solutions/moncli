from schematics.exceptions import ConversionError
from nose.tools import eq_,raises

from moncli import column_value as cv
from moncli.enums import ColumnType
from moncli import types as t

def test_should_succeed_when_to_native_returns_a_list_when_passing_in_a_tagsvalue_value_with_api_data_to_tags_type():
    # Arrange
    id = "tag_id"
    title = 'Tag IDs'
    column_type = ColumnType.tags
    column_value = cv.create_column_value(column_type,id=id,title=title)
    column_value.value = ['12345','12346']

    # Act
    timezone_type = t.TagsType(title=title)
    value = timezone_type.to_native(column_value.value)

    # Assert
    eq_(value,[12345,12346])

def test_should_succeed_when_to_native_returns_empty_list_when_passed_none_to_tags_type():
    # Arrange
    tags_type = t.TagsType(title='tags')

    # Act
    tags_value = tags_type.to_native(None)

    # Assert
    eq_(tags_value,[])

@raises(ConversionError)
def test_should_raise_conversion_error_when_invalid_tags_value_passed_to_tags_type():
    # Arrange
    tags_type = t.TagsType(title='tags')

    # Act
    tags_type.to_native(["invalid string"])

    

def test_should_succeed_when_to_primitive_returns_an_empty_dict_when_passed_in_a_none_to_tags_type():
    # Arrange
    tags_type = t.TagsType(title='tags')

    # Act
    tags_value = tags_type.to_primitive(None)

    # Assert
    eq_(tags_value,{})

def test_should_succeed_when_to_primitive_returns_export_dict_when_passed_in_a_list_value_to_tags_type():
    # Arrange
    tags_type = t.TagsType(title='tags')

    # Act
    tags_value = tags_type.to_primitive([12345,12346])

    # Assert
    eq_(tags_value['tag_ids'],[12345,12346])

