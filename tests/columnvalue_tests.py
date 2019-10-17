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
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.checked, False)
    eq_(format, {})


def test_should_return_checked_checkbox_column_value():

    # Arrange
    id = 'checkbox_2'
    column_type = ColumnType.checkbox
    title = 'Checkbox'

    # Act
    column_value = create_column_value(id, column_type, title, checked='true')
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.checked, True)
    eq_(format, {'checked': 'true'})
    

def test_should_return_an_empty_country_column_value():

    # Arrange
    id = 'country_1'
    column_type = ColumnType.country
    title = 'Country'

    # Act
    column_value = create_column_value(id, column_type, title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.country_code, None)
    eq_(column_value.country_name, None)
    eq_(format, {})


def test_should_return_country_column_value():

    # Arrange
    id = 'country_2'
    column_type = ColumnType.country
    title = 'Checkbox'
    country_code = 'US'
    country_name = 'United States'

    # Act
    column_value = create_column_value(id, column_type, title, countryCode=country_code, countryName=country_name)
    format = column_value.format()

    # Assert
    ok_(columnvalue != None)
    eq_(column_value.country_code, country_code)
    eq_(column_value.country_name, country_name)
    eq_(format, {'countryCode': country_code, 'countryName': country_name})
    

def test_should_return_an_empty_date_column_value():

    # Arrange
    id = 'date_1'
    column_type = ColumnType.date
    title = 'Date'

    # Act
    column_value = create_column_value(id, column_type, title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.date, None)
    eq_(column_value.time, None)
    eq_(format, {})


def test_should_return_date_column_value_with_default_time():

    # Arrange
    id = 'date_2'
    column_type = ColumnType.date
    title = 'Date'
    date = '1990-08-30'

    # Act
    column_value = create_column_value(id, column_type, title, date=date)
    format = column_value.format()

    # Assert
    ok_(columnvalue != None)
    eq_(column_value.date, date)
    eq_(column_value.time, None)
    eq_(format, {'date': date})


def test_should_return_date_column_value_with_time():

    # Arrange
    id = 'date_2'
    column_type = ColumnType.date
    title = 'Date'
    date = '1990-08-30'
    time = '04:15'

    # Act
    column_value = create_column_value(id, column_type, title, date=date, time=time)
    format = column_value.format()

    # Assert
    ok_(columnvalue != None)
    eq_(column_value.date, date)
    eq_(column_value.time, time)
    eq_(format, {'date': date, 'time': time})
    
