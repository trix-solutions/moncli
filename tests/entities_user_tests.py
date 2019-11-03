from unittest.mock import patch
from nose.tools import ok_, eq_, raises

import moncli.entities as e
import moncli.enums as en

USERNAME = 'test.user@foobar.org' 
GET_ME_RETURN_VALUE = e.user.User(**{'creds': None, 'id': '1', 'email': USERNAME})


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_users')
def test_user_should_get_the_account(get_users, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_users.return_value = [{'id': '1', 'email': 'test.user@foobar.org', 'teams': [{'id': '1'}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    user = client.get_users()[0]

    get_users.return_value = [{'id': '1', 'account': {'id': '1', 'name': 'Account 1', 'first_day_of_the_week': None, 'show_timeline_weekends': None, 'slug': None}}]

    # Act
    account = user.get_account()

    # Assert
    ok_(account != None)
    eq_(account.name, 'Account 1')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_users')
@patch('moncli.api_v2.get_teams')
def test_user_should_get_teams(get_teams, get_users, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_users.return_value = [{'id': '1', 'email': 'test.user@foobar.org', 'teams': [{'id': '1'}]}]
    get_teams.return_value = [{'id': '1', 'name': 'Team 1', 'users': [{'id': '1'}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    user = client.get_users()[0]

    # Act
    teams = user.get_teams()

    # Assert
    ok_(teams != None)
    eq_(len(teams), 1)
    eq_(teams[0].name, 'Team 1')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_users')
@patch('moncli.api_v2.create_notification')
def test_user_should_send_a_notification(create_notification, get_users, get_me):

    # Arrange 
    get_me.return_value = GET_ME_RETURN_VALUE
    get_users.return_value = [{'id': '1', 'email': 'test.user@foobar.org', 'teams': [{'id': '1'}]}]
    create_notification.return_value = {'id': '1', 'text': 'Text 1'}
    client = e.client.MondayClient(USERNAME, '', '')
    user = client.get_users()[0]

    # Act 
    notification = user.send_notification('Text 1', '2', en.NotificationTargetType.Post)

    # Assert
    ok_(notification != None)
    ok_(notification.text, 'Text 1')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_teams')
@patch('moncli.api_v2.get_users')
def test_team_should_retrieve_list_of_users(get_users, get_teams, get_me):

    # Arrange 
    get_me.return_value = GET_ME_RETURN_VALUE
    get_teams.return_value = [{'id': '1', 'name': 'Team 1', 'users': [{'id': '1'}]}]
    get_users.return_value = [{'id': '1', 'email': 'test.user@foobar.org', 'teams': [{'id': '1'}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    team = client.get_teams()[0]

    # Act 
    users = team.get_users()

    # Assert
    ok_(users != None)
    eq_(len(users), 1)
    eq_(users[0].email, 'test.user@foobar.org')


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_users')
def test_account_should_get_plan_info(get_users, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_users.return_value = [{'id': '1', 'email': 'test.user@foobar.org', 'teams': [{'id': '1'}]}]
    client = e.client.MondayClient(USERNAME, '', '')
    user = client.get_users()[0]

    get_users.return_value = [{'id': '1', 'account': {'id': '1', 'name': 'Account 1', 'first_day_of_the_week': None, 'show_timeline_weekends': None, 'slug': None}}]
    account = user.get_account()

    get_users.return_value = [{'id': '1', 'account': {'plan': {'max_users': 1}}}]

    # Act
    plan = account.get_plan()
    

    # Assert
    ok_(plan != None)
    eq_(plan.max_users, 1)
