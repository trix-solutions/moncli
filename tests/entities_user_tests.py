from unittest.mock import patch
from nose.tools import ok_, eq_, raises

import moncli.entities as e

USERNAME = 'test.user@foobar.org' 
GET_ME_RETURN_VALUE = e.user.User(**{'creds': None, 'id': '1', 'email': USERNAME})


@patch.object(e.client.MondayClient, 'get_me')
@patch('moncli.api_v2.get_users')
def test_should_get_the_account(get_users, get_me):

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
def test_should_get_teams(get_teams, get_users, get_me):

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
