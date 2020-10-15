import json

from nose.tools import ok_, eq_, raises

from moncli import entities as en
from moncli.entities import column_value as cv
from moncli.enums import ColumnType, PeopleKind

@raises(cv.ColumnValueIsReadOnly)
def test_should_fail_for_non_writeable_column_type():

    # Arrange
    id = 'test_id'
    column_type = ColumnType.auto_number
    title = 'should fail'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.format()


def test_should_return_an_empty_checkbox_column_value():

    # Arrange
    id = 'checkbox_1'
    column_type = ColumnType.checkbox
    title = 'Checkbox'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
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
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.checked = True
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.checked, True)
    eq_(format, {'checked': 'true'})


def test_should_return_empty_checkbox_column_value_after_setting_value_to_none():

    # Arrange
    id = 'checkbox_3'
    column_type = ColumnType.checkbox
    title = 'Checkbox'
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps({'checked': True}))

    # Act
    column_value.checked = None
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.checked, False)
    eq_(format, {})
    

def test_should_return_an_empty_country_column_value():

    # Arrange
    id = 'country_1'
    column_type = ColumnType.country
    title = 'Country'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.country_code, None)
    eq_(column_value.country_name, None)
    eq_(format, {})


@raises(cv.UnknownCountryCodeError)
def test_should_raise_an_unknown_country_code_error():

    # Arrange
    id = 'country_2'
    column_type = ColumnType.country
    title = 'Country'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.country_code = 'foobar'


@raises(cv.UnknownCountryNameError)
def test_should_raise_an_unknown_country_name_error():

    # Arrange
    id = 'country_3'
    column_type = ColumnType.country
    title = 'Country'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.country_name = 'foobar'


def test_should_return_country_column_value_by_country_code():

    # Arrange
    id = 'country_4'
    column_type = ColumnType.country
    title = 'Checkbox'
    country_code = 'US'
    country_name = 'United States'

    # Act
    column_value = cv.create_column_value(column_type, id=id, title=title)
    column_value.country_code = country_code
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.country_code, country_code)
    eq_(column_value.country_name, country_name)
    eq_(format, {'countryCode': country_code, 'countryName': country_name})


def test_should_return_country_column_value_by_country_name():

    # Arrange
    id = 'country_5'
    column_type = ColumnType.country
    title = 'Checkbox'
    country_code = 'VC'
    country_name = 'Saint Vincent and the Grenadines'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.country_name = country_name
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.country_code, country_code)
    eq_(column_value.country_name, country_name)
    eq_(format, {'countryCode': country_code, 'countryName': country_name})


def test_should_return_empty_country_column_value_when_setting_country_code_to_none():

    # Arrange
    id = 'country_6'
    column_type = ColumnType.country
    title = 'Checkbox'
    country_code = 'VC'
    country_name = 'Saint Vincent and the Grenadines'
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps({'countryCode': country_code, 'countryName': country_name}))

    # Act
    column_value.country_code = None
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.country_code, None)
    eq_(column_value.country_name, None)
    eq_(format, {})


def test_should_return_empty_country_column_value_when_setting_country_name_to_none():

    # Arrange
    id = 'country_7'
    column_type = ColumnType.country
    title = 'Checkbox'
    country_code = 'VC'
    country_name = 'Saint Vincent and the Grenadines'
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps({'countryCode': country_code, 'countryName': country_name}))

    # Act
    column_value.country_name = None
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.country_code, None)
    eq_(column_value.country_name, None)
    eq_(format, {})
    

def test_should_return_an_empty_date_column_value():

    # Arrange
    id = 'date_1'
    column_type = ColumnType.date
    title = 'Date'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.date, None)
    eq_(column_value.time, None)
    eq_(format, {})


@raises(cv.DateFormatError)
def test_should_raise_date_format_error_when_setting_date():

    # Arrange
    id = 'date_2'
    column_type = ColumnType.date
    title = 'Date'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.date = 'foobar'


def test_should_return_date_column_value_with_default_time():

    # Arrange
    id = 'date_3'
    column_type = ColumnType.date
    title = 'Date'
    date = '1990-08-30'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.date = date
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.date, date)
    eq_(column_value.time, None)
    eq_(format, {'date': date})


@raises(cv.TimeFormatError)
def test_should_raise_time_format_error_when_setting_time():

    # Arrange
    id = 'date_4'
    column_type = ColumnType.date
    title = 'Date'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.time = 'foobar'


def test_should_return_date_column_value_with_time():

    # Arrange
    id = 'date_5'
    column_type = ColumnType.date
    title = 'Date'
    date = '1990-08-30'
    time = '04:15:00'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.date = date
    column_value.time = time
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.date, date)
    eq_(column_value.time, time)
    eq_(format, {'date': date, 'time': time})


def test_should_return_empty_date_column_value_if_only_time_is_set():

    # Arrange
    id = 'date_6'
    column_type = ColumnType.date
    title = 'Date'
    time = '04:15:00'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.time = time
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.date, None)
    eq_(column_value.time, time)
    eq_(format, {})


def test_should_return_empty_date_column_value_if_date_and_time_are_set_to_null():

    # Arrange
    id = 'date_7'
    column_type = ColumnType.date
    title = 'Date'
    date = '1990-08-30'
    time = '04:15:00'
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps({'date': date, 'time': time}))

    # Act
    column_value.date = None
    column_value.time = None
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.date, None)
    eq_(column_value.time, None)
    eq_(format, {})


@raises(cv.ColumnValueSettingsError)
def test_should_raise_column_value_settings_error():

    # Arrange
    id = 'dropdown_1'
    column_type = ColumnType.dropdown
    title = 'Dropdown One'
    
    # Act
    cv.create_column_value(column_type, id=id, title=title)


def test_should_return_empty_dropdown_column_value():

    # Arrange
    id = 'dropdown_2'
    column_type = ColumnType.dropdown
    title = 'Dropdown Two'
    column_value = cv.create_column_value(column_type, id=id, title=title, settings=en.objects.DropdownSettings({'labels': []}))

    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.labels, [])
    eq_(format, {})


@raises(cv.DropdownLabelError)
def test_should_raise_dropdown_label_error_when_adding_label():

    # Arrange
    id = 'dropdown_3'
    column_type = ColumnType.dropdown
    title = 'Dropdown Three'
    column_value = cv.create_column_value(column_type, id=id, title=title, settings=en.objects.DropdownSettings({
        'labels': [
            {'id': 1, 'name': 'Label 1'}
        ]
    }))

    # Act 
    column_value.add_label(2)


@raises(cv.DropdownLabelSetError)
def test_should_raise_dropdown_label_set_error():

    # Arrange
    id = 'dropdown_3'
    column_type = ColumnType.dropdown
    title = 'Dropdown Four'
    ids = {'ids': [1]}
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps(ids), settings=en.objects.DropdownSettings({
        'labels': [
            {'id': 1, 'name': 'Label 1'}
        ]
    }))

    # Act 
    column_value.add_label(1)


def test_should_add_label_to_dropdown_column_value():

    # Arrange
    id = 'dropdown_5'
    column_type = ColumnType.dropdown
    title = 'Dropdown Five'
    column_value = cv.create_column_value(column_type, id=id, title=title, settings=en.objects.DropdownSettings({
        'labels': [
            {'id': 1, 'name': 'Label 1'}
        ]
    }))

    # Act 
    column_value.add_label(1)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.labels, [en.objects.DropdownLabel({'id': 1, 'name': 'Label 1'})])
    eq_(format, {'ids': [1]})


@raises(cv.DropdownLabelError)
def test_should_raise_dropdown_label_error_when_removing_label():

    # Arrange
    id = 'dropdown_6'
    column_type = ColumnType.dropdown
    title = 'Dropdown Six'
    column_value = cv.create_column_value(column_type, id=id, title=title, settings=en.objects.DropdownSettings({
        'labels': [
            {'id': 1, 'name': 'Label 1'}
        ]
    }))

    # Act 
    column_value.remove_label(2)


@raises(cv.DropdownLabelNotSetError)
def test_should_raise_dropdown_label_not_set_error():

    # Arrange
    id = 'dropdown_7'
    column_type = ColumnType.dropdown
    title = 'Dropdown Seven'
    column_value = cv.create_column_value(column_type, id=id, title=title, settings=en.objects.DropdownSettings({
        'labels': [
            {'id': 1, 'name': 'Label 1'}
        ]
    }))

    # Act 
    column_value.remove_label(1)


def test_should_remove_label_to_dropdown_column_value():

    # Arrange
    id = 'dropdown_8'
    column_type = ColumnType.dropdown
    title = 'Dropdown Eight'
    ids = {'ids': [1]}
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps(ids), settings=en.objects.DropdownSettings({
        'labels': [
            {'id': 1, 'name': 'Label 1'}
        ]
    }))

    # Act 
    column_value.remove_label(1)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.labels, [])
    eq_(format, {})
    

def test_should_return_empty_email_column_value():

    # Arrange
    id = 'email_1'
    column_type = ColumnType.email
    title = 'Email One'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
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
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.email = email
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.email, email)
    eq_(column_value.email_text, email)
    eq_(format, {'email': email, 'text': email})


def test_should_return_email_column_value_with_email_and_text():

    # Arrange
    id = 'email_3'
    column_type = ColumnType.email
    title = 'Email Three'
    email = 'email@test.com'
    text = 'Test Email'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.email = email
    column_value.email_text = text
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.email, email)
    eq_(column_value.email_text, text)
    eq_(format, {'email': email, 'text': text})


def test_should_return_empty_email_column_value_when_only_text_is_set():

    # Arrange
    id = 'email_4'
    column_type = ColumnType.email
    title = 'Email Four'
    text = 'Test Email'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.email_text = text
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.email, None)
    eq_(column_value.email_text, text)
    eq_(format, {})


def test_should_return_empty_email_column_value_when_email_and_text_are_set_to_null():

    # Arrange
    id = 'email_4'
    column_type = ColumnType.email
    title = 'Email Four'
    email = 'email@test.com'
    text = 'Test Email'
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps({'email': email, 'text': text}))

    # Act
    column_value.email = None
    column_value.email_text = None
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.email, None)
    eq_(column_value.email_text, None)
    eq_(format, {})


def test_should_return_file_column_value():

    # Arrange
    id = 'files'
    title = 'Files'
    text = 'https://test.monday.com/files/33.jpg'
    value = {'files': [{'id': '127540488', 'created_at': None, 'file_extension': None, 'file_size': None, 'name': '33.jpg', 'public_url': None, 'url': 'https://test.monday.com/files/33.jpg', 'url_thumbnail': None}]}

    # Act
    column_value = cv.create_column_value(ColumnType.file, id=id, title=title, text=text, value=json.dumps(value))

    # Assert
    ok_(column_value != None)
    eq_(column_value.files, value['files'])
    eq_(column_value.format(), {'clear_all': True})


def test_should_return_empty_hour_column_value():

    # Arrange
    id = 'hour_1'
    column_type = ColumnType.hour
    title = 'Hour One'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.hour, None)
    eq_(column_value.minute, 0)
    eq_(format, {})


def test_should_return_hour_column_value_with_hour_and_default_minute():

    # Arrange
    id = 'hour_2'
    column_type = ColumnType.hour
    title = 'Hour Two'
    hour = '6'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.hour = hour
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.hour, hour)
    eq_(column_value.minute, 0)
    eq_(format, {'hour': hour, 'minute': 0})


def test_should_return_hour_column_value_with_hour_and_minute():

    # Arrange
    id = 'hour_3'
    column_type = ColumnType.hour
    title = 'Hour Tree'
    hour = '7'
    minute = '6'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.hour = hour
    column_value.minute = minute
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.hour, hour)
    eq_(column_value.minute, minute)
    eq_(format, {'hour': hour, 'minute': minute})


def test_should_return_empty_hour_column_value_with_set_minute():

    # Arrange
    id = 'hour_4'
    column_type = ColumnType.hour
    title = 'Hour Four'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.minute = 25
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.hour, None)
    eq_(column_value.minute, 25)
    eq_(format, {})


def test_should_return_empty_hour_column_value_when_hour_and_minute_set_to_null():

    # Arrange
    id = 'hour_4'
    column_type = ColumnType.hour
    title = 'Hour Four'
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps({'hour': 1, 'minute': 1}))

    # Act
    column_value.hour = None
    column_value.minute = None
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.hour, None)
    eq_(column_value.minute, 0)
    eq_(format, {})


def test_should_return_empty_link_column_value():

    # Arrange
    id = 'link_1'
    column_type = ColumnType.link
    title = 'Link'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.url, None)
    eq_(column_value.url_text, None)
    eq_(format, {})


def test_should_return_link_column_value_with_url():

    # Arrange
    id = 'link_2'
    column_type = ColumnType.link
    title = 'Link'
    url = 'https://link.two'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.url = url
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.url, url)
    eq_(column_value.url_text, url)
    eq_(format, {'url': url, 'text': url})


def test_should_return_link_column_value_with_url_and_text():

    # Arrange
    id = 'link_3'
    column_type = ColumnType.link
    title = 'Link'
    url = 'https://link.three'
    text = 'Link'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.url = url
    column_value.url_text = text
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.url, url)
    eq_(column_value.url_text, text)
    eq_(format, {'url': url, 'text': text})


def test_should_return_empty_link_column_value_with_set_text():

    # Arrange
    id = 'link_4'
    column_type = ColumnType.link
    title = 'Link'
    text = 'Link'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.url_text = text
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.url, None)
    eq_(column_value.url_text, text)
    eq_(format, {})


def test_should_return_empty_link_column_value_when_url_and_text_set_to_null():

    # Arrange
    id = 'link_4'
    column_type = ColumnType.link
    title = 'Link'
    url = 'https://link.two'
    text = 'Link'
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps({'url': url, 'text': text}))

    # Act
    column_value.url = None
    column_value.url_text = None
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.url, None)
    eq_(column_value.url_text, None)
    eq_(format, {})


def test_should_return_an_empty_long_text_column_value():

    # Arrange
    id = 'long_text_0'
    column_type = ColumnType.long_text
    title = 'Long Text'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.long_text, None)
    eq_(format, {})


def test_should_return_long_text_column_value_with_text():

    # Arrange
    id = 'long_text_1'
    column_type = ColumnType.long_text
    title = 'Long Text'
    text = 'LOOOOOOOOOOOOOOOOOOOOOOOOOOOOONG'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.long_text = text
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.long_text, text)
    eq_(format, {'text': text})


def test_should_return_empty_long_text_column_value_when_text_set_to_null():

    # Arrange
    id = 'long_text_1'
    column_type = ColumnType.long_text
    title = 'Long Text'
    text = 'LOOOOOOOOOOOOOOOOOOOOOOOOOOOOONG'
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps({'text': text}))

    # Act
    column_value.long_text = None
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.long_text, None)
    eq_(format, {})


def test_should_return_empty_name_column_value():

    # Arrange
    id = 'name_1'
    column_type = ColumnType.name
    title = 'Name'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.name, '')
    eq_(format, '')


def test_should_return_name_column_value_with_name():

    # Arrange
    id = 'name_2'
    column_type = ColumnType.name
    title = 'Name'
    name = 'Name'

    # Act
    column_value = cv.create_column_value(column_type, id=id, title=title)
    column_value.name = name
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.name, name)
    eq_(format, name)


def test_should_return_empty_name_column_value_when_setting_name_to_null():

    # Arrange
    id = 'name_3'
    column_type = ColumnType.name
    title = 'Name'
    name = 'Name'
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps(name))

    # Act
    column_value.name = None
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.name, '')
    eq_(format, '')


def test_should_return_an_empty_number_column_value():

    # Arrange
    id = 'number_0'
    column_type = ColumnType.numbers
    title = 'Number'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
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
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.number = number
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.number, number)
    eq_(format, str(number))


def test_should_return_a_number_column_value_with_float():

    # Arrange
    id = 'number_2'
    column_type = ColumnType.numbers
    title = 'Number'
    number = 23.333333333

    # Act
    column_value = cv.create_column_value(column_type, id=id, title=title)
    column_value.number = number
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.number, number)
    eq_(format, str(number))


def test_should_return_empty_number_column_value_when_number_set_to_null():

    # Arrange
    id = 'number_3'
    column_type = ColumnType.numbers
    title = 'Number'
    number = 23.333333333
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps(number))

    # Act
    column_value.number = None
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.number, None)
    eq_(format, '')


@raises(cv.NumberValueError)
def test_raise_number_value_error_when_input_is_text():

    # Arrange
    id = 'number_x'
    column_type = ColumnType.numbers
    title = 'Number'
    number = 'x'

    # Act
    column_value = cv.create_column_value(column_type, id=id, title=title)
    column_value.number = number


def test_should_return_an_empty_people_column_value():

    # Arrange
    id = 'people_0'
    column_type = ColumnType.people
    title = 'People 0'

    # Act
    column_value = cv.create_column_value(column_type, id=id, title=title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.persons_and_teams, [])
    eq_(format, {})


def test_should_return_a_people_column_value_with_persons_and_teams():

    # Arrange
    id = 'people_1'
    column_type = ColumnType.people
    title = 'People 1'
    persons_and_teams = {'personsAndTeams': [{'id': 1, 'kind': PeopleKind.person.name}]}
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps(persons_and_teams))

    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.persons_and_teams, persons_and_teams['personsAndTeams'])
    eq_(format, persons_and_teams)


def test_should_return_a_people_column_value_with_added_persons_and_teams():

    # Arrange
    id = 'people_1'
    column_type = ColumnType.people
    title = 'People 1'
    persons_and_teams = {'personsAndTeams': [{'id': 1, 'kind': PeopleKind.person.name}]}
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.add_people(en.User(creds=None, id='1'))
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.persons_and_teams, persons_and_teams['personsAndTeams'])
    eq_(format, persons_and_teams)


def test_should_return_an_empty_people_column_value_after_remove():

    # Arrange
    id = 'people_2'
    column_type = ColumnType.people
    title = 'People 2'
    persons_and_teams = {'personsAndTeams': [{'id': 1, 'kind': PeopleKind.person.name}]}
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps(persons_and_teams))

    # Act
    column_value.remove_people(1)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.persons_and_teams, [])
    eq_(format, {})


def test_should_return_people_column_value_unaffected_when_adding_existent_people():

    # Arrange
    id = 'people_2'
    column_type = ColumnType.people
    title = 'People 2'
    persons_and_teams = {'personsAndTeams': [{'id': 1, 'kind': PeopleKind.person.name}]}
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps(persons_and_teams))

    # Act
    column_value.add_people(en.User(creds=None, id='1'))
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.persons_and_teams, persons_and_teams['personsAndTeams'])
    eq_(format, persons_and_teams)


def test_should_return_people_column_value_unaffected_when_removing_nonexistent_people():

    # Arrange
    id = 'people_2'
    column_type = ColumnType.people
    title = 'People 2'
    persons_and_teams = {'personsAndTeams': [{'id': 1, 'kind': PeopleKind.person.name}]}
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps(persons_and_teams))

    # Act
    column_value.remove_people(2)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.persons_and_teams, persons_and_teams['personsAndTeams'])
    eq_(format, persons_and_teams)


def test_should_return_an_empty_phone_column_value():

    # Arrange
    id = 'phone_0'
    column_type = ColumnType.phone
    title = 'Phone'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.phone, None)
    eq_(column_value.country_short_name, None)
    eq_(format, {'phone': '', 'countryShortName': ''})


def test_should_return_a_phone_column_value_with_data():

    # Arrange
    id = 'phone_2'
    column_type = ColumnType.phone
    title = 'Phone'
    country_short_name = 'US'
    phone = '1234567890'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.phone = phone
    column_value.country_short_name = country_short_name
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.phone, phone)
    eq_(column_value.country_short_name, country_short_name)
    eq_(format, {'phone': phone, 'countryShortName': country_short_name})


def test_should_return_empty_phone_column_value_when_only_phone_set():

    # Arrange
    id = 'phone_3'
    column_type = ColumnType.phone
    title = 'Phone'
    phone = '1234567890'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.phone = phone
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.phone, phone)
    eq_(column_value.country_short_name, None)
    eq_(format, {'phone': '', 'countryShortName': ''})


def test_should_return_empty_phone_column_value_when_only_country_short_name_set():

    # Arrange
    id = 'phone_3'
    column_type = ColumnType.phone
    title = 'Phone'
    country_short_name = 'US'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.country_short_name = country_short_name
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.phone, None)
    eq_(column_value.country_short_name, country_short_name)
    eq_(format, {'phone': '', 'countryShortName': ''})


def test_should_return_empty_rating_column_value():

    # Arrange
    id = 'rating_1'
    column_type = ColumnType.rating
    title = 'Rating One'

    # Act
    column_value = cv.create_column_value(column_type, id=id, title=title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.rating, None)
    eq_(format, {})


def test_should_return_a_rating_column_value_with_rating():

    # Arrange
    id = 'rating_2'
    column_type = ColumnType.rating
    title = 'Rating Two'
    rating = 5

    # Act
    column_value = cv.create_column_value(column_type, id=id, title=title)
    column_value.rating = rating
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.rating, 5)
    eq_(format, {'rating': rating})


def test_should_return_empty_rating_column_value_when_set_to_none():

    # Arrange
    id = 'rating_2'
    column_type = ColumnType.rating
    title = 'Rating Two'
    rating = 5
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps({'rating': rating}))

    # Act
    column_value.rating = None
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.rating, None)
    eq_(format, {})


def test_should_return_empty_status_column_value():

    # Arrange
    id = 'status_1'
    column_type = ColumnType.status
    title = 'Status One'
    column_value = cv.create_column_value(column_type, id=id, title=title, additional_info=json.dumps({}), settings=None)

    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.index, None)
    eq_(column_value.label, None)
    eq_(format, {})


@raises(cv.StatusIndexError)
def test_should_raise_status_index_error_when_setting_index():

    # Arrange
    id = 'status_2'
    column_type = ColumnType.status
    title = 'Status'
    label = 'Status 2'
    column_value = cv.create_column_value(
        column_type, 
        id=id, 
        title=title, 
        additional_info=json.dumps({'label': label}), 
        settings=en.objects.StatusSettings({'labels': {'2': label}}))

    # Act 
    column_value.index = 1


def test_should_return_status_column_value_when_setting_index():

    # Arrange
    id = 'status_2'
    column_type = ColumnType.status
    title = 'Status'
    label = 'Status 2'
    index = 2
    column_value = cv.create_column_value(
        column_type, 
        id=id, 
        title=title, 
        additional_info=json.dumps({'label': label}), 
        settings=en.objects.StatusSettings({'labels': {'2': label}}))

    # Act 
    column_value.index = index
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.index, index)
    eq_(column_value.label, label)
    eq_(format, {'index': index})


@raises(cv.StatusLabelError)
def test_should_raise_status_label_error_when_setting_label():

    # Arrange
    id = 'status_2'
    column_type = ColumnType.status
    title = 'Status'
    label = 'Status 2'
    column_value = cv.create_column_value(
        column_type, 
        id=id, 
        title=title, 
        additional_info=json.dumps({'label': label}), 
        settings=en.objects.StatusSettings({'labels': {'2': label}}))

    # Act 
    column_value.label = 'Status Foobar'


def test_should_return_status_column_value_when_setting_label():

    # Arrange
    id = 'status_2'
    column_type = ColumnType.status
    title = 'Status'
    label = 'Status 2'
    index = 2
    column_value = cv.create_column_value(
        column_type, 
        id=id, 
        title=title, 
        additional_info=json.dumps({'label': label}), 
        settings=en.objects.StatusSettings({'labels': {'2': label}}))

    # Act 
    column_value.label = label
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.index, index)
    eq_(column_value.label, label)
    eq_(format, {'index': index})


def test_should_return_empty_tags_column_value():

    # Arrange
    id = 'tags_1'
    column_type = ColumnType.tags
    title = 'Tags 1'
    column_value = cv.create_column_value(column_type, id=id, title=title)
    
    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.tag_ids, [])
    eq_(format, {'tag_ids': []})


def test_should_return_tags_column_value_with_tag_ids():

    # Arrange
    id = 'tags_2'
    column_type = ColumnType.tags
    title = 'Tags 2'
    tag_ids = [1,2,3]
    
    # Act
    column_value = cv.create_column_value(column_type, id=id, title=title)
    for id in tag_ids:
        column_value.add(id)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.tag_ids, tag_ids)
    eq_(format, {'tag_ids': tag_ids})


def test_should_remove_tag_ids_and_return_tags_column_value_with_remaining_tag_ids():

    # Arrange
    id = 'tags_2'
    column_type = ColumnType.tags
    title = 'Tags 2'
    tag_ids = [1,2,3]
    column_value = cv.create_column_value(column_type, id=id, title=title)
    for id in tag_ids:
        column_value.add(id)
    
    # Act
    column_value.remove(2)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.tag_ids, [1,3])
    eq_(format, {'tag_ids': [1,3]})


def test_should_ignore_adding_existent_tag_id():

    # Arrange
    id = 'tags_2'
    column_type = ColumnType.tags
    title = 'Tags 2'
    tag_ids = [1,2]
    column_value = cv.create_column_value(column_type, id=id, title=title)
    for id in tag_ids:
        column_value.add(id)
    
    # Act
    column_value.add(2)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.tag_ids, [1,2])
    eq_(format, {'tag_ids': [1,2]})


def test_should_ignore_removing_nonexistent_tag_id():

    # Arrange
    id = 'tags_2'
    column_type = ColumnType.tags
    title = 'Tags 2'
    tag_ids = [1,2]
    column_value = cv.create_column_value(column_type, id=id, title=title)
    for id in tag_ids:
        column_value.add(id)
    
    # Act
    column_value.remove(3)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.tag_ids, [1,2])
    eq_(format, {'tag_ids': [1,2]})


def test_should_return_empty_tag_column_value_when_all_ids_are_removed():

    # Arrange
    id = 'tags_2'
    column_type = ColumnType.tags
    title = 'Tags 2'
    tag_ids = [1]
    column_value = cv.create_column_value(column_type, id=id, title=title)
    for id in tag_ids:
        column_value.add(id)
    
    # Act
    column_value.remove(1)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.tag_ids, [])
    eq_(format, {'tag_ids': []})


def test_should_return_empty_team_column_value():

    # Arrange
    id = 'team_1'
    column_type = ColumnType.team
    title = 'Team'
    column_value = cv.create_column_value(column_type, id=id, title=title)
    
    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.team_id, None)
    eq_(format, {})


def test_should_return_team_column_value_with_team_id():

    # Arrange
    id = 'team_2'
    column_type = ColumnType.team
    title = 'Team'
    team_id = 12345
    column_value = cv.create_column_value(column_type, id=id, title=title)
    
    # Act
    column_value.team_id = team_id
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.team_id, team_id)
    eq_(format, {'team_id': team_id})


def test_should_return_empty_team_column_value_when_team_id_set_to_none():

    # Arrange
    id = 'team_2'
    column_type = ColumnType.team
    title = 'Team'
    team_id = 12345
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps({'team_id': team_id}))
    
    # Act
    column_value.team_id = None
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.team_id, None)
    eq_(format, {})


def test_should_return_empty_text_column_value():

    # Arrange
    id = 'text_1'
    column_type = ColumnType.text
    title = 'Text 1'
    column_value = cv.create_column_value(column_type, id=id, title=title)
    
    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.text, None)
    eq_(format, '')


def test_should_return_text_column_value_with_text():

    # Arrange
    id = 'text_2'
    column_type = ColumnType.text
    title = 'Text 2'
    text = 'Hello, Grandma!'
    column_value = cv.create_column_value(column_type, id=id, title=title)
    
    # Act
    column_value.text_value = text
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.text_value, text)
    eq_(format, text)


def test_should_return_empty_text_column_value_when_text_set_to_null():

    # Arrange
    id = 'text_2'
    column_type = ColumnType.text
    title = 'Text 2'
    text = 'Hello, Grandma!'
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps(text))
    
    # Act
    column_value.text_value = None
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.text_value, None)
    eq_(format, '')


def test_should_return_an_empty_timeline_column_value():

    # Arrange
    id = 'timeline_1'
    column_type = ColumnType.timeline
    title = 'Timeline'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.from_date, None)
    eq_(column_value.to_date, None)
    eq_(format, {})


@raises(cv.DateFormatError)
def test_should_raise_date_format_error_when_setting_from_date():

    # Arrange
    id = 'timeline_1'
    column_type = ColumnType.timeline
    title = 'Timeline'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.from_date = 'Foobar'


@raises(cv.DateFormatError)
def test_should_raise_date_format_error_when_setting_to_date():

    # Arrange
    id = 'timeline_1'
    column_type = ColumnType.timeline
    title = 'Timeline'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.to_date = 'Foobar'


def test_should_return_a_timeline_column_value_with_data():

    # Arrange
    id = 'timeline_2'
    column_type = ColumnType.timeline
    title = 'Timeline Two'
    from_date = '1990-08-30'
    to_date = '2013-08-23'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.from_date = from_date
    column_value.to_date = to_date
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.from_date, from_date)
    eq_(column_value.to_date, to_date)
    eq_(format, {'from': from_date, 'to': to_date})


def test_should_return_empty_timeline_column_value_with_to_date_set_to_none():

    # Arrange
    id = 'timeline_2'
    column_type = ColumnType.timeline
    title = 'Timeline Two'
    from_date = '1990-08-30'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.from_date = from_date
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.from_date, from_date)
    eq_(column_value.to_date, None)
    eq_(format, {})


def test_should_return_empty_timeline_column_value_with_from_date_set_to_none():

    # Arrange
    id = 'timeline_2'
    column_type = ColumnType.timeline
    title = 'Timeline Two'
    to_date = '2013-08-23'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.to_date = to_date
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.from_date, None)
    eq_(column_value.to_date, to_date)
    eq_(format, {})


def test_should_return_empty_timezone_column_value():

    # Arrange
    id = 'timezone_1'
    column_type = ColumnType.world_clock
    title = 'Time zone 1'
    column_value = cv.create_column_value(column_type, id=id, title=title)
    
    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.timezone, None)
    eq_(format, {})


@raises(cv.UnknownTimeZoneError)
def test_should_raise_unknown_timezone_error_when_timezone_set():

    # Arrange
    id = 'timezone_2'
    column_type = ColumnType.world_clock
    title = 'Timezone 2'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.timezone = 'Foo/Bar'


def test_should_return_timezone_column_value_with_text():

    # Arrange
    id = 'timezone_2'
    column_type = ColumnType.world_clock
    title = 'Timezone 2'
    timezone = 'America/Phoenix'
    column_value = cv.create_column_value(column_type, id=id, title=title)
    
    # Act
    column_value.timezone = timezone
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.timezone, timezone)
    eq_(format, {'timezone': timezone})


def test_should_return_empty_timezone_column_value_when_set_to_none():

    # Arrange
    id = 'timezone_2'
    column_type = ColumnType.world_clock
    title = 'Timezone 2'
    timezone = 'America/Phoenix'
    column_value = cv.create_column_value(column_type, id=id, title=title, value=json.dumps({'timezone': timezone}))
    
    # Act
    column_value.timezone = None
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.timezone, None)
    eq_(format, {})


def test_should_return_empty_week_column_value():

    # Arrange
    id = 'week_1'
    column_type = ColumnType.week
    title = 'Week'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.start_date, None)
    eq_(column_value.end_date, None)
    eq_(format, {'week': ''})


@raises(cv.DateFormatError)
def test_should_raise_date_format_error_on_setting_start_date():

    # Arrange
    id = 'week_2'
    column_type = ColumnType.week
    title = 'Week'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.start_date = 'poop'


@raises(cv.DateFormatError)
def test_should_raise_date_format_error_on_setting_end_date():

    # Arrange
    id = 'week_3'
    column_type = ColumnType.week
    title = 'Week'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.end_date = 'poop'


def test_should_return_week_column_value_with_data():

    # Arrange
    id = 'week_4'
    column_type = ColumnType.week
    title = 'Week'
    start_date = '2019-10-21'
    end_date = '2019-10-27'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.start_date = start_date
    column_value.end_date = end_date
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.start_date, start_date)
    eq_(column_value.end_date, end_date)
    eq_(format, {'week': {'startDate': start_date, 'endDate': end_date}})


def test_should_return_empty_week_column_value_when_only_start_date_set():

    # Arrange
    id = 'week_5'
    column_type = ColumnType.week
    title = 'Week'
    start_date = '2019-10-21'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.start_date = start_date
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.start_date, start_date)
    eq_(column_value.end_date, None)
    eq_(format, cv.WeekValue.null_value)


def test_should_return_empty_week_column_value_when_only_end_date_set():

    # Arrange
    id = 'week_6'
    column_type = ColumnType.week
    title = 'Week'
    end_date = '2019-10-27'
    column_value = cv.create_column_value(column_type, id=id, title=title)

    # Act
    column_value.end_date = end_date
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.start_date, None)
    eq_(column_value.end_date, end_date)
    eq_(format, cv.WeekValue.null_value)