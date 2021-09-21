import json

from nose.tools import ok_, eq_, raises

from moncli import entities as en, error as e
from moncli.enums import *

def test_should_return_empty_text_column_value():

    # Arrange
    id = 'text_1'
    column_type = ColumnType.text
    title = 'Text 1'
    column_value = en.cv.create_column_value(column_type, id=id, title=title)
    
    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.value, None)
    eq_(format, '')


def test_should_return_text_column_value_with_loaded_text():

    # Arrange
    id = 'text_2'
    column_type = ColumnType.text
    title = 'Text 2'
    text = 'Hello, Grandma!'
    column_value = en.cv.create_column_value(column_type, id=id, title=title, value=json.dumps(text))
    
    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.value, text)
    eq_(format, text)


def test_should_return_empty_text_column_value_when_value_is_set_to_native_default():

    # Arrange
    id = 'text_3'
    column_type = ColumnType.text
    title = 'Text 3'
    text = 'Hello, Grandma!'
    column_value = en.cv.create_column_value(column_type, id=id, title=title, value=json.dumps(text))
    
    # Act
    column_value.value = None

    # Assert
    eq_(column_value.value, None)


def test_should_return_text_column_with_value_when_setting_an_int_value():

    # Arrange
    id = 'text_4'
    column_type = ColumnType.text
    title = 'Text 4'
    text = 12345
    column_value = en.cv.create_column_value(column_type, id=id, title=title)
    
    # Act
    column_value.value = text

    # Assert
    eq_(column_value.value, str(text))


def test_should_return_text_column_with_value_when_setting_an_float_value():

    # Arrange
    id = 'text_5'
    column_type = ColumnType.text
    title = 'Text 5'
    text = 123.45
    column_value = en.cv.create_column_value(column_type, id=id, title=title)
    
    # Act
    column_value.value = text
    # Assert
    eq_(column_value.value, str(text))

@raises(e.ColumnValueError)
def test_should_throw_exception_when_setting_an_invalid_value():

    # Arrange
    id = 'text_5'
    column_type = ColumnType.text
    title = 'Text 5'
    text = {'value': 123.45}
    column_value = en.cv.create_column_value(column_type, id=id, title=title)
    
    # Act
    column_value.value = text

    # Assert
    eq_(column_value.value, str(text))


def test_should_create_a_people_column_value_with_no_api_input_data():

    # Arrange

    id = 'people_1'
    column_type = ColumnType.people
    title = 'people 1'
    value = None
    
    column_value = en.cv.create_column_value(column_type, id=id, title=title,value=value)
    
    # Act
    format = column_value.format()

    # Assert

    eq_(format, {})


def test_should_create_a_people_column_value_with_no_api_input_data():

    # Arrange

    id = 'people_1'
    column_type = ColumnType.people
    title = 'people 1'
    value_dict ={'personsAndTeams': [{'id':134 , 'kind':'person'},{'id':11234 , 'kind':'person'}]}
    value = json.dumps(value_dict)
    column_value = en.cv.create_column_value(column_type, id=id, title=title,value=value)
    
    # Act
    person_value = column_value.format()['personsAndTeams']
    format = person_value[0]

    # Assert

    eq_(format['id'],134)

def test_should_set_people_column_value_to_none():
     # Arrange

    id = 'people_1'
    column_type = ColumnType.people
    title = 'people 1'
    column_value = en.cv.create_column_value(column_type, id=id, title=title)
    
    # Act

    column_value.value = None

    # Assert

    eq_(column_value.value,[])

@raises(e.ColumnValueError)
def test_should_throw_an_exception_when_setting_an_invalid_value_to_people_column_value():

    id = 'people_1'
    column_type = ColumnType.people
    title = 'people 1'
    value_dict ={'personsAndTeams': [{'id':123 , 'kind':'not person'},{'id':11234 , 'kind':'person'}]}
    value = json.dumps(value_dict)
    column_value = en.cv.create_column_value(column_type, id=id, title=title)
    
    # Act
    column_value.value = value

def test_should_create_a_number_column_value_with_no_api_input_data():

    # Arrange
    id = 'value_1'
    title = "value"
    column_type = ColumnType.numbers
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    format = column_value.format()

    #Assert
    eq_(format, "")

def test_should_create_a_number_column_value_with_api_input_data():

    id = 'value_1'
    title = "value"
    column_type = ColumnType.numbers
    value = "123"
    column_value = en.cv.create_column_value(column_type, id=id, title=title,value=value)

    # Act
    format = column_value.format()

    #Assert
    eq_(format, value)

def test_should_set_number_column_value_to_none_to_value():

    # Arrange
    id = 'value_1'
    title = "value"
    column_type = ColumnType.numbers
    value=None
    column_value = en.cv.create_column_value(column_type, id=id, title=title)


    # Act
    column_value.value = value

    #Assert
    eq_(column_value.value, None)

def test_should_set_number_column_value_to_int_or_float_to_value():
    id = 'value_1'
    title = "value"
    column_type = ColumnType.numbers
    value = 123.32
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = value

    #Assert
    eq_(column_value.value,value)

@raises(e.ColumnValueError)
def test_should_set_number_column_value_to_an_improper_string_and_error():
    id = 'value_1'
    title = "value"
    column_type = ColumnType.numbers
    value = "just a number"
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = value
    

def test_should_set_number_column_value_to__a_valid_string_value():
    id = 'value_1'
    title = "value"
    column_type = ColumnType.numbers
    value = "123.32"
    column_value = en.cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.value = value

    #Assert
    eq_(column_value.value, float(value))
