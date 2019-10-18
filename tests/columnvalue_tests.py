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
    ok_(column_value != None)
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
    ok_(column_value != None)
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
    ok_(column_value != None)
    eq_(column_value.date, date)
    eq_(column_value.time, time)
    eq_(format, {'date': date, 'time': time})


def test_should_return_empty_dropdown_column_value():

    # Arrange
    id = 'dropdown_1'
    column_type = ColumnType.dropdown
    title = 'Dropdown One'

    # Act
    column_value = create_column_value(id, column_type, title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.label, None)
    eq_(column_value.ids, None)
    eq_(format, {})


def test_should_return_dropdown_column_value_by_ids():

    # Arrange
    id = 'dropdown_2'
    column_type = ColumnType.dropdown
    title = 'Dropdown Two'
    ids = [1,2,3]

    # Act 
    column_value = create_column_value(id, column_type, title, ids=ids)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.ids, [1,2,3])
    eq_(column_value.label, None)
    eq_(format, {'ids': [1,2,3]})


def test_should_return_dropdown_column_value_by_label():

    # Arrange
    id = 'dropdown_3'
    column_type = ColumnType.dropdown
    title = 'Dropdown Three'
    label = 'Status 1'

    # Act
    column_value = create_column_value(id, column_type, title, label=label)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.ids, None)
    eq_(column_value.label, label)
    eq_(format, {'label': label})


def test_should_return_dropdown_column_value_by_label_with_preference():

    # Arrange
    id = 'dropdown_4'
    column_type = ColumnType.dropdown
    title = 'Dropdown Four'
    label = 'Status 2'
    ids = [1,2,3]

    # Act
    column_value = create_column_value(id, column_type, title, label=label, ids=ids)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.ids, None)
    eq_(column_value.label, label)
    eq_(format, {'label': label})
    

def test_should_return_empty_email_column_value():

    # Arrange
    id = 'email_1'
    column_type = ColumnType.email
    title = 'Email One'

    # Act
    column_value = create_column_value(id, column_type, title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.email, None)
    eq_(column_value.text, None)
    eq_(format, {})


def test_should_return_email_column_value_with_email():

    # Arrange
    id = 'email_2'
    column_type = ColumnType.email
    title = 'Email Two'
    email = 'email@test.com'

    # Act
    column_value = create_column_value(id, column_type, title, email=email)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.email, email)
    eq_(column_value.text, None)
    eq_(format, {'email': email, 'text': email})


def test_should_return_email_column_value_with_email_and_text():

    # Arrange
    id = 'email_2'
    column_type = ColumnType.email
    title = 'Email Two'
    email = 'email@test.com'
    text = 'Test Email'

    # Act
    column_value = create_column_value(id, column_type, title, email=email, text=text)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.email, email)
    eq_(column_value.text, text)
    eq_(format, {'email': email, 'text': text})


def test_should_return_empty_hour_column_value():

    # Arrange
    id = 'hour_1'
    column_type = ColumnType.hour
    title = 'Hour One'

    # Act
    column_value = create_column_value(id, column_type, title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.hour, None)
    eq_(column_value.minute, 0)
    eq_(format, {})


def test_should_return_hour_column_value_with_hour_and_minute():

    # Arrange
    id = 'hour_2'
    column_type = ColumnType.hour
    title = 'Hour Two'
    hour = '7'
    minute = '6'

    # Act
    column_value = create_column_value(id, column_type, title, hour=hour, minute=minute)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.hour, hour)
    eq_(column_value.minute, minute)
    eq_(format, {'hour': hour, 'minute': minute})


def test_should_return_empty_link_column_value():

    # Arrange
    id = 'link_1'
    column_type = ColumnType.link
    title = 'Link One'

    # Act
    column_value = create_column_value(id, column_type, title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.url, None)
    eq_(column_value.text, None)
    eq_(format, {})


def test_should_return_link_column_value_with_url():

    # Arrange
    id = 'link_2'
    column_type = ColumnType.link
    title = 'Link Two'
    url = 'https://link.two'

    # Act
    column_value = create_column_value(id, column_type, title, url=url)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.url, url)
    eq_(column_value.text, None)
    eq_(format, {'url': url, 'text': url})


def test_should_return_link_column_value_with_url_and_text():

    # Arrange
    id = 'link_3'
    column_type = ColumnType.link
    title = 'Link Three'
    url = 'https://link.three'
    text = 'Link Three'

    # Act
    column_value = create_column_value(id, column_type, title, url=url, text=text)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.url, url)
    eq_(column_value.text, text)
    eq_(format, {'url': url, 'text': text})


def test_should_return_an_empty_long_text_column_value():

    # Arrange
    id = 'long_text_0'
    column_type = ColumnType.long_text
    title = 'Long Test 0'

    # Act
    column_value = create_column_value(id, column_type, title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.text, None)
    eq_(format, {})


def test_should_return_long_text_column_value_with_text():

    # Arrange
    id = 'long_text_1'
    column_type = ColumnType.long_text
    title = 'Long Test 1'
    text = 'LOOOOOOOOOOOOOOOOOOOOOOOOOOOOONG'

    # Act
    column_value = create_column_value(id, column_type, title, text=text)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.text, text)
    eq_(format, {'text': text})
    

def test_should_return_name_column_value_with_name():

    # Arrange
    id = 'name_1'
    column_type = ColumnType.name
    title = 'Name 1'
    name = 'Name'

    # Act
    column_value = create_column_value(id, column_type, title, name=name)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.name, name)
    eq_(format, name)


def test_should_return_an_empty_number_column_value():

    # Arrange
    id = 'number_0'
    column_type = ColumnType.numbers
    title = 'Number 0'

    # Act
    column_value = create_column_value(id, column_type, title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.number, None)
    eq_(format, '')


def test_should_return_a_number_column_value_with_int():

    # Arrange
    id = 'number_1'
    column_type = ColumnType.numbers
    title = 'Number 1'
    number = 8675309

    # Act
    column_value = create_column_value(id, column_type, title, number=number)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.number, number)
    eq_(format, str(number))


def test_should_return_a_number_column_value_with_float():

    # Arrange
    id = 'number_2'
    column_type = ColumnType.numbers
    title = 'Number 2'
    number = 23.333333333

    # Act
    column_value = create_column_value(id, column_type, title, number=number)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.number, number)
    eq_(format, str(number))


def test_should_return_an_empty_number_column_value_when_input_is_text():

    # Arrange
    id = 'number_x'
    column_type = ColumnType.numbers
    title = 'Number X'
    number = 'x'

    # Act
    column_value = create_column_value(id, column_type, title, number=number)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.number, None)
    eq_(format, '')

