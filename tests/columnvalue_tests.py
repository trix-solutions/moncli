from nose.tools import ok_, eq_, raises

from moncli import columnvalue
from moncli.columnvalue import create_column_value
from moncli.enums import ColumnType

@raises(columnvalue.InvalidColumnValueType)
def test_should_fail_for_non_writeable_column_type():

    # Arrange
    id = 'test_id'
    column_type = ColumnType.auto_number
    title = 'should fail'

    # Act
    create_column_value(id, column_type, title)


def test_should_return_an_empty_checkbox_column_value():

    # Arrange
    id = 'checkbox_1'
    column_type = ColumnType.checkbox
    title = 'Checkbox'

    # Act
    column_value = create_column_value(id, column_type, title)

    # Assert
    ok_(column_value != None)
    eq_(column_value.checked, False)


def test_should_return_checked_checkbox_column_value():

    # Arrange
    id = 'checkbox_2'
    column_type = ColumnType.checkbox
    title = 'Checkbox'

    # Act
    column_value = create_column_value(id, column_type, title, checked='true')

    # Assert
    ok_(column_value != None)
    eq_(column_value.checked, True)
    

def test_should_return_an_empty_country_column_value():

    # Arrange
    id = 'country_1'
    column_type = ColumnType.country
    title = 'Country'

    # Act
    column_value = create_column_value(id, column_type, title)

    # Assert
    ok_(column_value != None)
    eq_(column_value.country_code, None)
    eq_(column_value.country_name, None)


def test_should_return_country_column_value():

    # Arrange
    id = 'country_2'
    column_type = ColumnType.country
    title = 'Checkbox'
    country_code = 'US'
    country_name = 'United States'

    # Act
    column_value = create_column_value(id, column_type, title, countryCode=country_code, countryName=country_name)

    # Assert
    ok_(columnvalue != None)
    eq_(column_value.country_code, country_code)
    eq_(column_value.country_name, country_name)
    
