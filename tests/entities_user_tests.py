from unittest.mock import patch
from nose.tools import ok_, eq_

from moncli import client
from moncli.enums import NotificationTargetType


@patch('moncli.api_v2.get_users')
def test_user_should_get_the_account(get_users):

    # Arrange
    get_users.return_value = [{'id': '1', 'email': 'test.user@foobar.org'}]
    user = client.get_users()[0]
    get_users.return_value = [{'id': '1', 'account': {'id': '1', 'name': 'Account 1', 'first_day_of_the_week': None, 'show_timeline_weekends': None, 'slug': None}}]

    # Act
    account = user.get_account()

    # Assert
    ok_(account != None)
    eq_(account.name, 'Account 1')



@patch('moncli.api_v2.get_users')
def test_user_should_get_teams(get_users):

    # Arrange
    get_users.return_value = [{'id': '1', 'email': 'test.user@foobar.org'}]
    user = client.get_users()[0]
    get_users.return_value = [{'id': '1', 'teams': [{'id': '1', 'name': 'Team 1'}]}]

    # Act
    teams = user.get_teams()

    # Assert
    ok_(teams != None)
    eq_(len(teams), 1)
    eq_(teams[0].name, 'Team 1')



@patch('moncli.api_v2.get_users')
@patch('moncli.api_v2.create_notification')
def test_user_should_send_a_notification(create_notification, get_users):

    # Arrange 
    get_users.return_value = [{'id': '1', 'email': 'test.user@foobar.org'}]
    create_notification.return_value = {'id': '1', 'text': 'Text 1'}
    user = client.get_users()[0]

    # Act 
    notification = user.send_notification('Text 1', '2', NotificationTargetType.Post)

    # Assert
    ok_(notification != None)
    ok_(notification.text, 'Text 1')



@patch('moncli.api_v2.get_teams')
def test_team_should_retrieve_list_of_users(get_teams):

    # Arrange 
    get_teams.return_value = [{'id': '1', 'name': 'Team 1'}]
    team = client.get_teams()[0]
    get_teams.return_value = [{'id': '1', 'users':[{'id': '1', 'email': 'test.user@foobar.org'}]}]

    # Act 
    users = team.get_users()

    # Assert
    ok_(users != None)
    eq_(len(users), 1)
    eq_(users[0].email, 'test.user@foobar.org')



@patch('moncli.api_v2.get_account')
def test_account_should_get_plan_info(get_account):

    # Arrange
    get_account.return_value = {'id': '1', 'name': 'Account 1', 'first_day_of_the_week': None, 'show_timeline_weekends': None, 'slug': None}
    account = client.get_account()

    get_account.return_value = {'id': '1', 'plan': {'max_users': 1}}

    # Act
    plan = account.get_plan()
    
    # Assert
    ok_(plan != None)
    eq_(plan.max_users, 1)