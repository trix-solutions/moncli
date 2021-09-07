from unittest.mock import patch
from nose.tools import ok_, eq_, raises

from moncli import client, entities as en
from moncli.enums import BoardKind, NotificationTargetType, WorkspaceKind, SubscriberKind


@patch('moncli.api_v2.create_board')
def test_should_create_a_new_board(create_board):

    # Arrange
    board_name = 'New Board 1'
    board_kind = BoardKind.private
    create_board.return_value = {'id': '1', 'name': board_name, 'board_kind': board_kind.name}

    # Act
    board = client.create_board(board_name, board_kind)

    # Assert 
    ok_(board != None)
    eq_(board.name, board_name)
    eq_(board.board_kind, board_kind.name)


@patch('moncli.api_v2.get_boards')
def test_should_retrieve_a_list_of_boards(get_boards):

    # Arrange
    test_boards = [{'id': '1', 'name': 'Board 1'}]
    get_boards.return_value = test_boards

    # Act
    boards = client.get_boards()

    # Assert
    ok_(boards != None)
    eq_(len(boards), 1)
    eq_(boards[0].id, test_boards[0]['id'])
    eq_(boards[0].name, test_boards[0]['name'])



@raises(en.client.NotEnoughGetBoardParameters)
def test_should_fail_to_retrieve_single_board_due_to_too_few_parameters():

    # Act
    client.get_board()


@raises(en.client.TooManyGetBoardParameters)
def test_should_fail_to_retrieve_single_board_due_to_too_many_parameters():

    # Act
    client.get_board(id='1', name='Test Board 1')


@patch('moncli.api_v2.get_boards')
def test_should_retrieve_a_board_by_id(get_boards):

    # Arrange 
    id = '1'
    name = 'Test Board 1'
    get_boards.return_value = [{'id': id, 'name': name}]
    
    # Act
    board = client.get_board(id=id)

    # Assert
    ok_(board != None)
    eq_(board.id, id)
    eq_(board.name, name)


@patch.object(en.MondayClient, 'get_board_by_id')
@patch('moncli.api_v2.get_boards')
def test_should_retrieve_a_board_by_name(get_boards, get_board_by_id):

    # Arrange 
    id = '2'
    name = 'Test Board 2'
    get_boards.return_value = [{'id': '1', 'name': 'Test Board 1'}, {'id': id, 'name': name}]
    get_board_by_id.return_value = en.Board(id=id, name=name)
    
    # Act 
    board = client.get_board(name=name)

    # Assert
    ok_(board != None)
    eq_(board.id, id)
    eq_(board.name, name)


@patch('moncli.api_v2.archive_board')
def test_should_archive_a_board(archive_board):

    # Arrange 
    id = '1'
    archive_board.return_value = {'id': id}

    # Act 
    board = client.archive_board(id)

    # Assert
    ok_(board != None)
    eq_(board.id, id)


@raises(en.client.AssetIdsRequired)
def test_should_fail_to_retrieve_assets_with_no_ids():

    # Act
    client.get_assets([])


@patch('moncli.api_v2.get_assets')
def test_should_retrieve_assets(get_assets):

    # Arrange
    asset_id = '12345'
    name = '33.jpg'
    url = 'http://test.monday.com/files/33.jpg' 
    get_assets.return_value = [{'id': asset_id, 'name': name, 'url': url}]
    
    # Act
    assets = client.get_assets([12345])

    # Assert
    ok_(assets)
    eq_(assets[0].id, asset_id)
    eq_(assets[0].name, name)
    eq_(assets[0].url, url)


@patch('moncli.api_v2.get_items')
def test_should_get_items(get_items):

    # Arrange 
    get_items.return_value = [{'id': '1', 'name': 'Test Item 1'}]
    
    # Act 
    items = client.get_items()

    # Assert
    ok_(items != None)
    ok_(len(items), 1)


@patch('moncli.api_v2.get_updates')
def test_should_get_updates(get_updates):

    # Arrange 
    id = '1'
    body = 'Hello, world!'
    get_updates.return_value = [{'id': id, 'body': body}]

    # Act 
    updates = client.get_updates()

    # Assert
    ok_(updates != None)
    ok_(len(updates), 1)
    eq_(updates[0].id, id)
    eq_(updates[0].body, body)


@patch('moncli.api_v2.clear_item_updates')
def test_should_clear_item_updates(clear_item_updates):

    # Arrange 
    id = '1'
    name = 'Hello, world!'
    clear_item_updates.return_value = {'id': id, 'name': name}

    # Act 
    item = client.clear_item_updates(id)

    # Assert
    ok_(item)
    eq_(item.id, id)
    eq_(item.name, name)


@patch('moncli.api_v2.delete_update')
def test_should_delete_update(delete_update):

    # Arrange 
    id = '1'
    item_id = '12'
    creator_id = '123'
    delete_update.return_value = {'id': id, 'item_id': item_id, 'creator_id': creator_id}
    
    # Act 
    update = client.delete_update(id)

    # Assert
    ok_(update)
    eq_(update.id, id)
    eq_(update.item_id, item_id)
    eq_(update.creator_id, creator_id)


@patch('moncli.api_v2.create_notification')
def test_should_create_a_notification(create_notification):

    # Arrange 
    text = 'Text 1'
    create_notification.return_value = {'id': '1', 'text': text}

    # Act 
    notification = client.create_notification(text, '1', '2', NotificationTargetType.Post)

    # Assert
    ok_(notification != None)
    ok_(notification.text, text)


@patch('moncli.api_v2.create_or_get_tag')
def test_should_create_or_get_a_tag(create_or_get_tag):

    # Arrange 
    name = 'Tag 1'
    create_or_get_tag.return_value = {'id': '1', 'name': name, 'color': 'Black'}

    # Act 
    tag = client.create_or_get_tag(name)

    # Assert
    ok_(tag != None)
    eq_(tag.name, name)


@patch('moncli.api_v2.get_tags')

def test_should_retrieve_list_of_tags(get_tags):

    # Arrange 
    name = 'Tag 1'
    get_tags.return_value = [{'id': '1', 'name': name, 'color': 'Black'}]
    
    # Act 
    tags = client.get_tags()

    # Assert
    ok_(tags != None)
    eq_(len(tags), 1)
    eq_(tags[0].name, name)

@patch('moncli.api_v2.create_workspace')

def test_should_create_workspace(create_workspace):

    # Arrange
    id = '12345'
    name = 'Workspace'
    kind = WorkspaceKind.open
    description = 'This is a test workspace.'
    create_workspace.return_value = {'id': id, 'name': name, 'kind': kind.name, 'description': description}

    # Act
    workspace = client.create_workspace(name, kind, description=description)

    # Assert
    ok_(workspace != None)
    eq_(workspace.id, id)
    eq_(workspace.name, name)
    eq_(workspace.kind, kind.name)
    eq_(workspace.description, description)

@patch('moncli.api_v2.add_users_to_workspace')
def test_should_add_users_to_workspace(add_users_to_workspace):
    
    #Arrange
    id = '12345'
    user_ids = ['1','2','3','4','5']
    kind = SubscriberKind.owner
    add_users_to_workspace.return_value = {'id': id, 'kind': kind.name}

    # Act
    workspace = client.add_users_to_workspace(id ,user_ids, kind)

    # Assert
    ok_(workspace != None)
    eq_(workspace.id, id)
    eq_(workspace.kind , kind.name)

@patch('moncli.api_v2.add_teams_to_workspace')
def test_should_add_teams_to_workspace(add_teams_to_workspace):

    # Arrange
    workspace_id = '12345'
    team_ids =  [105939, 105940, 105941]
    add_teams_to_workspace.return_value = {'id': '12345'}

    # Act
    workspace = client.add_teams_to_workspace(workspace_id, team_ids)

    #Assert
    ok_(workspace != None)
    eq_(workspace.id, workspace_id)



@patch('moncli.api_v2.delete_teams_from_workspace')
def test_should_add_teams_to_workspace(delete_teams_from_workspace):

    # Arrange
    workspace_id = '12345'
    team_ids =  [105939, 105940, 105941]
    delete_teams_from_workspace.return_value = {'id': '12345'}

    # Act
    workspace = client.delete_teams_from_workspace(workspace_id, team_ids)

    #Assert
    ok_(workspace != None)
    eq_(workspace.id, workspace_id)



@patch('moncli.api_v2.get_users')
def test_should_retrieve_list_of_users(get_users):

    # Arrange 
    name = 'User 1'
    email = 'user.one@test.com'
    get_users.return_value = [{'id': '1', 'name': name, 'email': email}]

    # Act 
    users = client.get_users()

    # Assert
    ok_(users != None)
    eq_(len(users), 1)
    eq_(users[0].name, name)
    eq_(users[0].email, email)


@patch('moncli.api_v2.get_teams')
def test_should_retrieve_list_of_teams(get_teams):

    # Arrange 
    name = 'User 1'
    get_teams.return_value = [{'id': '1', 'name': name}]

    # Act 
    teams = client.get_teams()

    # Assert
    ok_(teams != None)
    eq_(len(teams), 1)
    eq_(teams[0].name, name)


@patch('moncli.api_v2.get_me')

def test_should_retrieve_me(get_me):

    # Arrange 
    name = 'User 2'
    username = "test@foo.bar"
    get_me.return_value = {'id': '1', 'name': name, 'email': username}
    
    # Act 
    user = client.get_me()

    # Assert
    ok_(user != None)
    eq_(user.email, username)