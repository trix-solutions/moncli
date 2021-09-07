from unittest.mock import patch
from nose.tools import ok_, eq_

from moncli.api_v2 import handlers, constants
from moncli.enums import BoardKind, ColumnType, State, NotificationTargetType, WebhookEventType, WorkspaceKind, SubscriberKind

EXECUTE_QUERY_PATCH = 'moncli.api_v2.handlers.execute_query'
UPLOAD_FILE_PATCH = 'moncli.api_v2.handlers.upload_file'

def setup():
    print('SETUP')


def teardown():
    print('TEARDOWN')

@patch(EXECUTE_QUERY_PATCH)
def test_create_board(execute_query):

    # Arrange
    execute_query.return_value = {'id': '1', 'name': 'Test', 'board_kind': 'public'}

    # Act
    board = handlers.create_board('Test', BoardKind.public, 'id', 'name', 'board_kind')
    
    # Assert
    ok_(board != None)
    ok_(type(board) is dict)
    ok_(board['name'] == 'Test')
    ok_(board['board_kind'] == 'public')


@patch(EXECUTE_QUERY_PATCH)
def test_get_board(execute_query):

    # Arrange
    execute_query.return_value = [{'id': '1'}, {'id': '2'}, {'id': '3'}, {'id': '4'}, {'id': '5'}]

    # Act
    boards = handlers.get_boards('id', limit=5)
    
    # Assert
    ok_(boards != None)
    ok_(type(boards) is list)
    ok_(len(boards) == 5)


@patch(EXECUTE_QUERY_PATCH)
def test_archive_board(execute_query):

    # Arrange
    execute_query.return_value = {'id': '1', 'state': 'archived'}

    # Act
    archived_board = handlers.archive_board('1', 'id', 'state')
    
    # Assert
    ok_(archived_board != None)
    ok_(type(archived_board) is dict)
    ok_(archived_board['state'] == 'archived')


@patch(EXECUTE_QUERY_PATCH)
def test_add_subscribers_to_board(execute_query):

    # Arrange
    user_id = '1'
    name = 'name'
    execute_query.return_value = {'id': user_id, 'name': name}

    # Act
    subscriber = handlers.add_subscribers_to_board('1', ['1'])

    # Assert
    ok_(subscriber)
    eq_(subscriber['id'], user_id)
    eq_(subscriber['name'], name)


@patch(EXECUTE_QUERY_PATCH)
def test_remove_subscribers_from_board(execute_query):

    # Arrange
    user_id = '1'
    name = 'name'
    execute_query.return_value = [{'id': user_id, 'name': name}]

    print(execute_query)
    # Act
    subscribers = handlers.delete_subscribers_from_board('1', ['1'])

    # Assert
    ok_(subscribers)
    eq_(subscribers[0]['id'], user_id)
    eq_(subscribers[0]['name'], name)


@patch(EXECUTE_QUERY_PATCH)
def test_create_column(execute_query):

    # Arrange
    title = 'Text Column One'
    execute_query.return_value = {'id': 'text_column_1', 'title': title, 'type': 'text'}

    # Act
    new_column = handlers.create_column('1', title, ColumnType.text, 'id', 'title', 'type')
    
    # Assert
    ok_(new_column != None)
    ok_(type(new_column) is dict)
    ok_(new_column['title'] == title)
    ok_(new_column['type'] == ColumnType.text.name)


@patch(EXECUTE_QUERY_PATCH)
def test_change_column_value(execute_query):

    # Arrange
    execute_query.return_value = {'id': '1'}

    # Act
    updated_item = handlers.change_column_value('1', 'text_column_1', '1', 'Hello, world!', 'id')
    
    # Assert
    ok_(updated_item != None)
    ok_(type(updated_item) is dict)
    ok_(updated_item['id'] == '1')


@patch(EXECUTE_QUERY_PATCH)
def test_change_multiple_column_value(execute_query):

    # Arrange
    column_values = {'text_column_1': 'Let\'s eat, Grandma!', 'numbers_column_1': 8675309}
    execute_query.return_value = {'id': '1'}

    # Act
    updated_item = handlers.change_multiple_column_value('1', '1', column_values, 'id')
    
    # Assert
    ok_(updated_item != None)
    ok_(type(updated_item) is dict)
    ok_(updated_item['id'] == '1')


@patch(EXECUTE_QUERY_PATCH)
def test_duplicate_group(execute_query):

    # Arrange
    group_id = 'group_2'
    execute_query.return_value = {'id': group_id}

    # Act
    duplicated_group = handlers.duplicate_group('1', 'group_1', 'id')
    
    # Assert
    ok_(duplicated_group != None)
    ok_(duplicated_group['id'] == 'group_2')


@patch(EXECUTE_QUERY_PATCH)
def test_create_group(execute_query):

    # Arrange
    group_id = 'group_1'
    group_name = 'New Group One'
    execute_query.return_value = {'id': group_id, 'title': group_name}

    # Act
    new_group = handlers.create_group('1', group_name, 'id', 'title')
    
    # Assert
    ok_(new_group != None)
    ok_(type(new_group) is dict)
    ok_(new_group['id'] == group_id)
    ok_(new_group['title'] == group_name)


@patch(EXECUTE_QUERY_PATCH)
def test_archive_group(execute_query):

    # Arrange
    execute_query.return_value = {'id': 'group_1', 'archived': True}

    # Act
    archived_group = handlers.archive_group('1', 'group_1', 'archived')
    
    # Assert
    ok_(archived_group != None)
    ok_(type(archived_group) is dict)
    ok_(archived_group.__contains__('id'))
    ok_(archived_group['archived'] == True)


@patch(EXECUTE_QUERY_PATCH)
def test_delete_group(execute_query):

    # Arrange
    execute_query.return_value = {'id': 'group_1', 'deleted': True}

    # Act
    deleted_group = handlers.delete_group('1', 'group_1', 'deleted')
    
    # Assert
    ok_(deleted_group != None)
    ok_(type(deleted_group) is dict)
    ok_(deleted_group.__contains__('id'))
    ok_(deleted_group['deleted'] == True)


@patch(EXECUTE_QUERY_PATCH)
def test_create_item(execute_query):

    # Arrange
    item_name = 'Item One'
    execute_query.return_value = {'id': '1', 'name': item_name}

    # Act
    new_item = handlers.create_item(item_name, '1', 'id', 'name')
    
    # Assert
    ok_(new_item != None)
    ok_(type(new_item) is dict)
    ok_(new_item.__contains__('id'))
    ok_(new_item['name'] == item_name)


@patch(EXECUTE_QUERY_PATCH)
def test_create_subitem(execute_query):

    # Arrange
    id = '2'
    item_name = 'Item One'
    execute_query.return_value = {'id': id, 'name': item_name}

    # Act
    subitem = handlers.create_subitem('1', item_name)
    
    # Assert
    ok_(subitem != None)
    ok_(type(subitem) is dict)
    eq_(subitem['id'], id)
    eq_(subitem['name'], item_name)


@patch(EXECUTE_QUERY_PATCH)
def test_clear_item_updates(execute_query):

    # Arrange
    id = '1'
    item_name = 'Item One'
    execute_query.return_value = {'id': id, 'name': item_name}

    # Act
    item = handlers.clear_item_updates(id)
    
    # Assert
    ok_(item)
    ok_(type(item) is dict)
    eq_(item['id'], id)
    eq_(item['name'], item_name)


@patch(EXECUTE_QUERY_PATCH)
def test_get_items(execute_query):

    # Arrange
    execute_query.return_value = [{'id': '1', 'name': 'Item One'}, {'id': '2', 'name': 'Item Two'}]

    # Act
    items = handlers.get_items(page=1, limit=2)
    
    # Assert
    ok_(items != None)
    ok_(type(items) is list)
    ok_(len(items) == 2)


@patch(EXECUTE_QUERY_PATCH)
def test_get_items_by_column_values(execute_query):

    # Arrange
    execute_query.return_value = [{'id': '1', 'name': 'Item One'}]

    # Act
    items = handlers.get_items_by_column_values('1', 'name', 'Item One', 'id', 'name')
    
    # Assert
    ok_(items != None)
    ok_(type(items) is list)
    ok_(len(items) == 1)


@patch(EXECUTE_QUERY_PATCH)
def test_archive_item(execute_query):

    # Arrange
    execute_query.return_value = {'id': '1', 'state': 'archived'}

    # Act
    archived_item = handlers.archive_item('1', 'id', 'state')
    
    # Assert
    ok_(archived_item != None)
    ok_(type(archived_item) is dict)
    ok_(archived_item['state'] == State.archived.name)


@patch(EXECUTE_QUERY_PATCH)
def test_delete_item(execute_query):

    # Arrange
    execute_query.return_value = {'id': '1', 'state': 'deleted'}

    # Act
    deleted_item = handlers.delete_item('1', 'id', 'state')
    
    # Assert
    ok_(deleted_item != None)
    ok_(type(deleted_item) is dict)
    ok_(deleted_item['state'] == State.deleted.name)


@patch(EXECUTE_QUERY_PATCH)
def test_duplicate_item(execute_query):

    # Arrange
    id = '1'
    name = 'dupe'
    execute_query.return_value = {'id': id, 'name': name}

    # Act
    duplicate_item = handlers.duplicate_item('1', '1')
    
    # Assert
    ok_(duplicate_item)
    eq_(duplicate_item['id'], id)
    eq_(duplicate_item['name'], name)


@patch(EXECUTE_QUERY_PATCH)
def test_create_update(execute_query):

    # Arrange
    body = 'Hello, world! Let\'s eat, Grandma!'
    item_id = '1'
    execute_query.return_value = {'id': '1', 'body': body, 'item_id': item_id}

    # Act
    new_update = handlers.create_update(body, item_id, 'id', 'body', 'item_id')
    
    # Assert
    ok_(new_update != None)
    ok_(type(new_update) is dict)
    ok_(new_update['body'] == body)
    ok_(new_update['item_id'] == item_id)


@patch(EXECUTE_QUERY_PATCH)
def test_get_updates(execute_query):

    # Arrange
    execute_query.return_value = [{'id': '1'}, {'id': '2'}, {'id': '3'}, {'id': '4'}, {'id': '5'}]

    # Act
    updates = handlers.get_updates('id', limit=5)
    
    # Assert
    ok_(updates != None)
    ok_(type(updates) is list)
    ok_(len(updates) == 5)


@patch(EXECUTE_QUERY_PATCH)
def test_delete_update(execute_query):

    # Arrange
    id = '1'
    item_id = '1'
    creator_id = '1'
    execute_query.return_value = {'id': id, 'item_id': item_id, 'creator_id': creator_id}

    # Act
    update = handlers.delete_update('1')
    
    # Assert
    ok_(update)
    ok_(type(update) is dict)
    eq_(update['id'], id)
    eq_(update['item_id'], item_id)
    eq_(update['creator_id'], creator_id)


@patch(EXECUTE_QUERY_PATCH)
def test_create_notification(execute_query):

    # Arrange
    text = 'Did you eat, Grandma?'
    execute_query.return_value = {'text': text}
    
    # Act
    notification = handlers.create_notification(text, '1', '2', NotificationTargetType.Project, 'text')
    
    # Assert
    ok_(notification != None)
    ok_(type(notification) is dict)
    ok_(notification['text'] == text)


@patch(EXECUTE_QUERY_PATCH)
def test_create_or_get_tag(execute_query):

    # Arrange
    name = 'Tag One'
    execute_query.return_value = {'id': '1', 'name': 'Tag One'}
    
    # Act
    tag = handlers.create_or_get_tag(name, 'id', 'name')
    
    # Assert
    ok_(tag != None)
    ok_(type(tag) is dict)
    ok_(tag['name'] == name)


@patch(EXECUTE_QUERY_PATCH)
def test_get_tags(execute_query):

    # Arrange
    execute_query.return_value = [{'id': '1'}, {'id': '2'}, {'id': '3'}]

    # Act
    tags = handlers.get_tags('id')
    
    # Assert
    ok_(tags != None)
    ok_(type(tags) is list)
    ok_(len(tags) == 3)


@patch(EXECUTE_QUERY_PATCH)
def test_get_users(execute_query):

    # Arrange
    execute_query.return_value = [{'id': '1', 'name': 'Grandma'}, {'id': '2', 'name': 'Osamu Dazai'}]

    # Act
    users = handlers.get_users('id', 'name')
    
    # Assert
    ok_(users != None)
    ok_(type(users) is list)
    ok_(len(users) == 2)


@patch(EXECUTE_QUERY_PATCH)
def test_get_teams(execute_query):

    # Arrange
    team_name = 'Grandma\'s House'
    execute_query.return_value = [{'id': '1', 'name': team_name}]

    # Act
    teams = handlers.get_teams('id', 'name')
    
    # Assert
    ok_(teams != None)
    ok_(type(teams) is list)
    ok_(len(teams) == 1)
    

@patch(EXECUTE_QUERY_PATCH)
def test_get_me(execute_query):

    # Arrange
    name = 'Meeeeeeeeee!'
    execute_query.return_value = {'id': '1', 'name': name}

    # Act
    me = handlers.get_me('')
    
    # Assert
    ok_(me != None)
    ok_(type(me) is dict)
    ok_(me['name'] == name)


@patch(EXECUTE_QUERY_PATCH)
def test_create_webhook(execute_query):

    # Arrange
    board_id = '12345'
    url = 'http://test.webhook.com/webhook/test'
    event = WebhookEventType.create_item
    webhook_id = '12345678'
    execute_query.return_value = {'id': webhook_id, 'board_id': int(board_id)}

    # Act
    webhook = handlers.create_webhook(board_id, url, event)

    # Assert
    ok_(webhook != None)
    ok_(type(webhook) is dict)
    ok_(webhook['id'] == webhook_id)
    ok_(webhook['board_id'] == int(board_id))


@patch(EXECUTE_QUERY_PATCH)
def test_delete_webhook(execute_query):

    # Arrange
    board_id = '12345'
    webhook_id = '12345678'
    execute_query.return_value = {'id': webhook_id, 'board_id': int(board_id)}

    # Act
    webhook = handlers.delete_webhook(webhook_id)

    # Assert
    ok_(webhook != None)
    ok_(type(webhook) is dict)
    ok_(webhook['id'] == webhook_id)
    ok_(webhook['board_id'] == int(board_id))


@patch(UPLOAD_FILE_PATCH)
def test_add_file_to_update(upload_file):

    # Arrange
    name = '33.jpg'
    url = 'https://test.monday.com/12345/{}'.format(name)
    upload_file.return_value = {'id': '12345', 'name': name, 'url': url}

    # Act
    asset = handlers.add_file_to_update('12345', '/Users/test/{}'.format(name))
    
    # Assert
    ok_(asset != None)
    ok_(type(asset) is dict)
    ok_(asset['name'] == name)
    ok_(asset['url'] == url)


@patch(UPLOAD_FILE_PATCH)
def test_add_file_to_column(upload_file):

    # Arrange
    name = '33.jpg'
    url = 'https://test.monday.com/12345/{}'.format(name)
    upload_file.return_value = {'id': '12345', 'name': name, 'url': url}

    # Act
    asset = handlers.add_file_to_column('12345', 'files', '/Users/test/{}'.format(name))
    
    # Assert
    ok_(asset != None)
    ok_(type(asset) is dict)
    ok_(asset['name'] == name)
    ok_(asset['url'] == url)


@patch(EXECUTE_QUERY_PATCH)
def test_create_workspace(execute_query):

    # Arrange
    id = '12345'
    name = 'Workspace'
    kind = WorkspaceKind.open
    description = 'This is a test workspace'
    execute_query.return_value = {'id': id, 'name': name, 'kind': kind.name, 'description': description}

    # Act
    workspace = handlers.create_workspace(name, kind, description=description)

    # Assert
    ok_(workspace != None)
    ok_(type(workspace) is dict)
    ok_(workspace['id'] == id)
    ok_(workspace['name'] == name)
    ok_(workspace['kind'] == kind.name)
    ok_(workspace['description'] == description)

    
@patch(EXECUTE_QUERY_PATCH)
def test_add_users_to_workspace(execute_query):

    # Arrange
    id = '12345'
    user_ids = ['1','2','3','4','5']
    kind = SubscriberKind.subscriber
    execute_query.return_value = {'id': '12345',  'kind': kind.name }
    # Act
    workspace = handlers.add_users_to_workspace(id,user_ids, kind)

    # Assert
    ok_(workspace != None)
    ok_(type(workspace) is dict)
    ok_(workspace['id'] == id)
    ok_(workspace['kind'] == kind.name)

    
@patch(EXECUTE_QUERY_PATCH)
def test_remove_users_from_workspace(execute_query):

    #Arrange
    workspace_id = '12345'
    user_ids=['1','2','3','4','5']
    execute_query.return_value = {'id': '12345'}

    #Act
    workspace = handlers.delete_users_from_workspace(workspace_id,user_ids)

    #Assert
    ok_(workspace != None)
    ok_(workspace['id'] == workspace_id)


@patch(EXECUTE_QUERY_PATCH)
def test_add_teams_to_workspace(execute_query):

    #Arrange
    workspace_id = '12345'
    team_ids =  ['105939', '105940', '105941']
    execute_query.return_value = [{'id': '105939'}, {'id': '105940'}, {'id': '105940'}]

    # Act
    teams = handlers.add_teams_to_workspace(workspace_id, team_ids)

    # Assert
    ok_(teams != None)
    ok_(type(teams is list))
    eq_(len(teams), 3)

    
@patch(EXECUTE_QUERY_PATCH)
def test_remove_teams_from_workspace(execute_query):

    #Arrange
    workspace_id = '12345'
    team_ids =  ['105939', '105940', '105941']
    execute_query.return_value = [{'id': '105939'}, {'id': '105940'}, {'id': '105940'}]

    # Act
    teams = handlers.delete_teams_from_workspace(workspace_id, team_ids)

    # Assert
    ok_(teams != None)
    ok_(type(teams is list))
    eq_(len(teams), 3)
