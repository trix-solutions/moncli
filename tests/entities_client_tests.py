from unittest.mock import patch
from nose.tools import ok_, eq_, raises

from moncli.api_v2 import constants
from moncli.entities import client as c, user as u, exceptions as ex
from moncli.enums import BoardKind, NotificationTargetType

USERNAME = 'test.user@foobar.org' 
GET_ME_RETURN_VALUE = u.User(**{'creds': None, 'id': '1', 'email': USERNAME})

@patch.object(c.MondayClient, 'get_me')
@raises(ex.AuthorizationError)
def test_should_fail_monday_client_authorization(get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE

    # Act
    c.MondayClient('not.my.username@whatever.gov', '', '')


@patch.object(c.MondayClient, 'get_me')
def test_should_create_monday_client(get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE

    # Act
    client = c.MondayClient(USERNAME, '', '')

    # Assert
    ok_(client != None)


@patch('moncli.api_v2.create_board')
@patch.object(c.MondayClient, 'get_me')
def test_should_create_a_new_board(get_me, create_board):

    # Arrange
    board_name = 'New Board 1'
    board_kind = BoardKind.private
    get_me.return_value = GET_ME_RETURN_VALUE
    create_board.return_value = {'id': '1', 'name': board_name, 'board_kind': board_kind.name}
    client = c.MondayClient(USERNAME, '', '')

    # Act
    board = client.create_board(board_name, board_kind=board_kind)

    # Assert 
    ok_(board != None)
    eq_(board.name, board_name)
    eq_(board.board_kind, board_kind.name)


@patch('moncli.api_v2.get_boards')
@patch.object(c.MondayClient, 'get_me')
def test_should_retrieve_a_list_of_boards(get_me, get_boards):

    # Arrange
    test_boards = [{'id': '1', 'name': 'Board 1'}]
    get_me.return_value = GET_ME_RETURN_VALUE
    get_boards.return_value = test_boards
    client = c.MondayClient(USERNAME, '', '')

    # Act
    boards = client.get_boards()

    # Assert
    ok_(boards != None)
    eq_(len(boards), 1)
    eq_(boards[0].id, test_boards[0]['id'])
    eq_(boards[0].name, test_boards[0]['name'])


@patch.object(c.MondayClient, 'get_me')
@raises(ex.NotEnoughGetBoardParameters)
def test_should_fail_to_retrieve_single_board_due_to_too_few_parameters(get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    client = c.MondayClient(USERNAME, '', '')

    # Act
    client.get_board()


@patch.object(c.MondayClient, 'get_me')
@raises(ex.TooManyGetBoardParameters)
def test_should_fail_to_retrieve_single_board_due_to_too_many_parameters(get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    client = c.MondayClient(USERNAME, '', '')

    # Act
    client.get_board(id='1', name='Test Board 1')


@patch('moncli.api_v2.get_boards')
@patch.object(c.MondayClient, 'get_me')
def test_should_retrieve_a_board_by_id(get_me, get_boards):

    # Arrange 
    id = '1'
    name = 'Test Board 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_boards.return_value = [{'id': id, 'name': name}]
    client = c.MondayClient(USERNAME, '', '')
    
    # Act
    board = client.get_board(id=id)

    # Assert
    ok_(board != None)
    eq_(board.id, id)
    eq_(board.name, name)


@patch('moncli.api_v2.get_boards')
@patch.object(c.MondayClient, 'get_me')
def test_should_retrieve_a_board_by_name(get_me, get_boards):

    # Arrange 
    id = '2'
    name = 'Test Board 2'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_boards.return_value = [{'id': '1', 'name': 'Test Board 1'}, {'id': id, 'name': name}]
    client = c.MondayClient(USERNAME, '', '')

    # Act 
    board = client.get_board(name=name)

    # Assert
    ok_(board != None)
    eq_(board.id, id)
    eq_(board.name, name)


@patch('moncli.api_v2.archive_board')
@patch.object(c.MondayClient, 'get_me')
def test_should_archive_a_board(get_me, archive_board):

    # Arrange 
    id = '1'
    get_me.return_value = GET_ME_RETURN_VALUE
    archive_board.return_value = {'id': id}
    client = c.MondayClient(USERNAME, '', '')

    # Act 
    board = client.archive_board(id)

    # Assert
    ok_(board != None)
    eq_(board.id, id)


@patch('moncli.api_v2.get_items')
@patch.object(c.MondayClient, 'get_me')
def test_should_get_items(get_me, get_items):

    # Arrange 
    get_me.return_value = GET_ME_RETURN_VALUE
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1', 'board': {'id': '1'}}]
    client = c.MondayClient(USERNAME, '', '')

    # Act 
    items = client.get_items()

    # Assert
    ok_(items != None)
    ok_(len(items), 1)


@patch('moncli.api_v2.get_updates')
@patch.object(c.MondayClient, 'get_me')
def test_should_get_updates(get_me, get_updates):

    # Arrange 
    id = '1'
    body = 'Hello, world!'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_updates.return_value = [{'id': id, 'body': body}]
    client = c.MondayClient(USERNAME, '', '')

    # Act 
    items = client.get_updates()

    # Assert
    ok_(items != None)
    ok_(len(items), 1)
    eq_(items[0].id, id)
    eq_(items[0].body, body)


@patch('moncli.api_v2.create_notification')
@patch.object(c.MondayClient, 'get_me')
def test_should_create_a_notification(get_me, create_notification):

    # Arrange 
    text = 'Text 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    create_notification.return_value = {'id': '1', 'text': text}
    client = c.MondayClient(USERNAME, '', '')

    # Act 
    notification = client.create_notification(text, '1', '2', NotificationTargetType.Post)

    # Assert
    ok_(notification != None)
    ok_(notification.text, text)


@patch('moncli.api_v2.create_or_get_tag')
@patch.object(c.MondayClient, 'get_me')
def test_should_create_or_get_a_tag(get_me, create_or_get_tag):

    # Arrange 
    name = 'Tag 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    create_or_get_tag.return_value = {'id': '1', 'name': name, 'color': 'Black'}
    client = c.MondayClient(USERNAME, '', '')

    # Act 
    tag = client.create_or_get_tag(name)

    # Assert
    ok_(tag != None)
    eq_(tag.name, name)


@patch('moncli.api_v2.get_tags')
@patch.object(c.MondayClient, 'get_me')
def test_should_retrieve_list_of_tags(get_me, get_tags):

    # Arrange 
    name = 'Tag 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_tags.return_value = [{'id': '1', 'name': name, 'color': 'Black'}]
    client = c.MondayClient(USERNAME, '', '')

    # Act 
    tags = client.get_tags()

    # Assert
    ok_(tags != None)
    eq_(len(tags), 1)
    eq_(tags[0].name, name)


@patch('moncli.api_v2.get_users')
@patch.object(c.MondayClient, 'get_me')
def test_should_retrieve_list_of_users(get_me, get_users):

    # Arrange 
    name = 'User 1'
    email = 'user.one@test.com'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_users.return_value = [{'id': '1', 'name': name, 'email': email}]
    client = c.MondayClient(USERNAME, '', '')

    # Act 
    users = client.get_users()

    # Assert
    ok_(users != None)
    eq_(len(users), 1)
    eq_(users[0].name, name)
    eq_(users[0].email, email)


@patch('moncli.api_v2.get_teams')
@patch.object(c.MondayClient, 'get_me')
def test_should_retrieve_list_of_teams(get_me, get_teams):

    # Arrange 
    name = 'User 1'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_teams.return_value = [{'id': '1', 'name': name}]
    client = c.MondayClient(USERNAME, '', '')

    # Act 
    teams = client.get_teams()

    # Assert
    ok_(teams != None)
    eq_(len(teams), 1)
    eq_(teams[0].name, name)


@patch('moncli.api_v2.get_me')
@patch.object(c.MondayClient, 'get_me')
def test_should_retrieve_me(get_me, get_me_client):

    # Arrange 
    name = 'User 2'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_me_client.return_value = {'id': '1', 'name': name, 'email': USERNAME}
    client = c.MondayClient(USERNAME, '', '')

    # Act 
    user = client.get_me()

    # Assert
    ok_(user != None)
    eq_(user.email, USERNAME)