from nose.tools import ok_, eq_, raises

from moncli import columnvalue
from moncli.columnvalue import create_column_value
from moncli.enums import ColumnType, PeopleKind

@raises(columnvalue.ColumnValueIsReadOnly)
def test_should_fail_for_non_writeable_column_type():

    # Arrange
    id = 'test_id'
    column_type = ColumnType.auto_number
    title = 'should fail'

    # Act
    column_value = create_column_value(id, column_type, title)
    column_value.format()


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
    column_value = create_column_value(id, column_type, title, country_name=country_name, country_code=country_code)
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
    eq_(column_value.text, email)
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
    eq_(column_value.minute, None)
    eq_(format, {})


def test_should_return_hour_column_value_with_hour_and_default_minute():

    # Arrange
    id = 'hour_2'
    column_type = ColumnType.hour
    title = 'Hour Two'
    hour = '6'

    # Act
    column_value = create_column_value(id, column_type, title, hour=hour)
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
    eq_(column_value.text, url)
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
    column_value = create_column_value(id, column_type, title, value=name)
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
    column_value = create_column_value(id, column_type, title, value=number)
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
    column_value = create_column_value(id, column_type, title, value=number)
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
    column_value = create_column_value(id, column_type, title, value=number)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.number, None)
    eq_(format, '')


def test_should_return_an_empty_people_column_value():

    # Arrange
    id = 'people_0'
    column_type = ColumnType.people
    title = 'People 0'

    # Act
    column_value = create_column_value(id, column_type, title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.persons_and_teams, None)
    eq_(format, {})


def test_should_return_a_people_column_value_with_persons_and_teams():

    # Arrange
    id = 'people_1'
    column_type = ColumnType.people
    title = 'People 1'
    persons_and_teams = [{'id': 1, 'kind': PeopleKind.person}]

    # Act
    column_value = create_column_value(id, column_type, title, persons_and_teams=persons_and_teams)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.persons_and_teams, persons_and_teams)
    eq_(format, {'personsAndTeams': persons_and_teams})


def test_should_return_an_empty_people_column_value_after_remove():

    # Arrange
    id = 'people_2'
    column_type = ColumnType.people
    title = 'People 2'
    persons_and_teams = [{'id': 1, 'kind': PeopleKind.person}]

    # Act
    column_value = create_column_value(id, column_type, title, persons_and_teams=persons_and_teams)
    column_value.remove_people(1)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.persons_and_teams, None)
    eq_(format, {})


def test_should_return_a_people_column_value_with_added_persons_and_teams():

    # Arrange
    id = 'people_1'
    column_type = ColumnType.people
    title = 'People 1'
    persons_and_teams = [{'id': 1, 'kind': PeopleKind.person.name}]

    # Act
    column_value = create_column_value(id, column_type, title)
    column_value.add_people(1, PeopleKind.person)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.persons_and_teams, persons_and_teams)
    eq_(format, {'personsAndTeams': persons_and_teams})


def test_should_return_an_empty_phone_column_value():

    # Arrange
    id = 'phone_0'
    column_type = ColumnType.phone
    title = 'Phone Zero'

    # Act
    column_value = create_column_value(id, column_type, title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.phone, None)
    eq_(column_value.country_short_name, None)
    eq_(format, {'phone': '', 'countryShortName': ''})


def test_should_return_a_phone_column_value_with_data():

    # Arrange
    id = 'phone_1'
    column_type = ColumnType.phone
    title = 'Phone One'
    country_short_name = 'US'
    phone = '1234567890'

    # Act
    column_value = create_column_value(id, column_type, title, phone=phone, country_short_name=country_short_name)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.phone, phone)
    eq_(column_value.country_short_name, country_short_name)
    eq_(format, {'phone': phone, 'countryShortName': country_short_name})


def test_should_return_empty_rating_column_value():

    # Arrange
    id = 'rating_1'
    column_type = ColumnType.rating
    title = 'Rating One'

    # Act
    column_value = create_column_value(id, column_type, title)
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
    column_value = create_column_value(id, column_type, title, rating=rating)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.rating, 5)
    eq_(format, {'rating': rating})


def test_should_return_empty_status_column_value():

    # Arrange
    id = 'status_1'
    column_type = ColumnType.status
    title = 'Status One'

    # Act
    column_value = create_column_value(id, column_type, title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.index, None)
    eq_(column_value.label, None)
    eq_(format, {'label': ''})


def test_should_return_status_column_value_by_index():

    # Arrange
    id = 'status_2'
    column_type = ColumnType.status
    title = 'Status Two'
    index = 1

    # Act 
    column_value = create_column_value(id, column_type, title, index=index)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.index, index)
    eq_(column_value.label, None)
    eq_(format, {'index': index})


def test_should_return_status_column_value_by_label():

    # Arrange
    id = 'status_3'
    column_type = ColumnType.status
    title = 'Status Three'
    label = 'Status 3'

    # Act
    column_value = create_column_value(id, column_type, title, label=label)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.index, None)
    eq_(column_value.label, label)
    eq_(format, {'label': label})


def test_should_return_status_column_value_by_label_with_preference():

    # Arrange
    id = 'status_4'
    column_type = ColumnType.status
    title = 'Status Four'
    label = 'Status 2'
    index = 4

    # Act
    column_value = create_column_value(id, column_type, title, label=label, index=index)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.index, None)
    eq_(column_value.label, label)
    eq_(format, {'label': label})


def test_should_return_empty_tags_column_value():

    # Arrange
    id = 'tags_1'
    column_type = ColumnType.tags
    title = 'Tags 1'
    
    # Act
    column_value = create_column_value(id, column_type, title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.tag_ids, None)
    eq_(format, {'tag_ids': []})


def test_should_return_tags_column_value_with_tag_ids():

    # Arrange
    id = 'tags_2'
    column_type = ColumnType.tags
    title = 'Tags 2'
    tag_ids = [1,2,3]
    
    # Act
    column_value = create_column_value(id, column_type, title, tag_ids=tag_ids)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.tag_ids, tag_ids)
    eq_(format, {'tag_ids': tag_ids})


def test_should_return_empty_team_column_value():

    # Arrange
    id = 'team_1'
    column_type = ColumnType.team
    title = 'Team 1'
    
    # Act
    column_value = create_column_value(id, column_type, title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.team_id, None)
    eq_(format, {})


def test_should_return_team_column_value_with_team_id():

    # Arrange
    id = 'team_2'
    column_type = ColumnType.team
    title = 'Team 2'
    team_id = 12345
    
    # Act
    column_value = create_column_value(id, column_type, title, team_id=team_id)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.team_id, team_id)
    eq_(format, {'team_id': team_id})


def test_should_return_empty_text_column_value():

    # Arrange
    id = 'text_1'
    column_type = ColumnType.text
    title = 'Text 1'
    
    # Act
    column_value = create_column_value(id, column_type, title)
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
    
    # Act
    column_value = create_column_value(id, column_type, title, value=text)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.text, text)
    eq_(format, text)


def test_should_return_an_empty_timeline_column_value():

    # Arrange
    id = 'timeline_1'
    column_type = ColumnType.timeline
    title = 'Timeline 1'

    # Act
    column_value = create_column_value(id, column_type, title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.from_date, None)
    eq_(column_value.to_date, None)
    eq_(format, {})


def test_should_return_a_timeline_column_value_with_data():

    # Arrange
    id = 'timeline_2'
    column_type = ColumnType.timeline
    title = 'Timeline Two'
    from_date = '1990-08-30'
    to_date = '2013-08-23'

    # Act
    column_value = create_column_value(id, column_type, title, from_date=from_date, to_date=to_date)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.from_date, from_date)
    eq_(column_value.to_date, to_date)
    eq_(format, {'from': from_date, 'to': to_date})


def test_should_return_empty_timezone_column_value():

    # Arrange
    id = 'timezone_1'
    column_type = ColumnType.world_clock
    title = 'Time zone 1'
    
    # Act
    column_value = create_column_value(id, column_type, title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.timezone, None)
    eq_(format, {})


def test_should_return_timezone_column_value_with_text():

    # Arrange
    id = 'timezone_2'
    column_type = ColumnType.world_clock
    title = 'Timezone 2'
    timezone = 'America/Phoenix'
    
    # Act
    column_value = create_column_value(id, column_type, title, timezone=timezone)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.timezone, timezone)
    eq_(format, {'timezone': timezone})


def test_should_return_empty_week_column_value():

    # Arrange
    id = 'week_1'
    column_type = ColumnType.week
    title = 'Week 1'

    # Act
    column_value = create_column_value(id, column_type, title)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.start_date, None)
    eq_(column_value.end_date, None)
    eq_(format, {})


def test_should_return_week_column_value_with_data():

    # Arrange
    id = 'week_1'
    column_type = ColumnType.week
    title = 'Week 1'
    start_date = '2019-10-21'
    end_date = '2019-10-27'

    # Act
    column_value = create_column_value(id, column_type, title, start_date=start_date, end_date=end_date)
    format = column_value.format()

    # Assert
    ok_(column_value != None)
    eq_(column_value.start_date, start_date)
    eq_(column_value.end_date, end_date)
    eq_(format, {'week': {'startDate': start_date, 'endDate': end_date}})