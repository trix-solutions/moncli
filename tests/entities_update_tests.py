from unittest.mock import patch
from nose.tools import ok_, eq_, raises

from moncli import MondayClient, entities as en

USERNAME = 'test.user@foobar.org' 
GET_ME_RETURN_VALUE = en.User(**{'creds': None, 'id': '1', 'email': USERNAME})

@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_updates')
def test_update_should_return_list_of_replies(get_updates, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_updates.return_value = [{'id': '1', 'creator_id': '1', 'item_id': '1', 'replies': [{'id': '2', 'creator_id': '1'}]}]
    client = MondayClient(USERNAME, '', '')
    
    # Act
    updates = client.get_updates()
    
    # Assert
    ok_(updates != None)
    eq_(len(updates), 1)
    eq_(len(updates[0].replies), 1)

@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_updates')
@patch('moncli.api_v2.get_users')
def test_update_should_return_creator(get_users, get_updates, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_updates.return_value = [{'id': '1', 'creator_id': '1', 'item_id': '1'}]
    get_users.return_value = [GET_ME_RETURN_VALUE.to_primitive()]
    client = MondayClient(USERNAME, '', '')
    update = client.get_updates()[0]

    # Assert
    ok_(update != None)
    eq_(update.creator.to_primitive(), GET_ME_RETURN_VALUE.to_primitive())


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_updates')
@patch('moncli.api_v2.get_users')
def test_update_should_return_creator_of_update_reply(get_users, get_updates, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_updates.return_value = [{'id': '1', 'creator_id': '1', 'item_id': '1', 'replies': [{'id': '2', 'creator_id': '1'}]}]
    get_users.return_value = [GET_ME_RETURN_VALUE.to_primitive()]
    client = MondayClient(USERNAME, '', '')
    reply = client.get_updates()[0].replies[0]

    # Assert
    ok_(reply != None)
    eq_(reply.creator.to_primitive(), GET_ME_RETURN_VALUE.to_primitive())


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_updates')
def test_should_return_list_of_replies_for_an_update(get_updates, get_me):

    # Arrange
    reply_id = '12345'
    reply_body = 'Reply text'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_updates.return_value = [{'id': '1', 'creator_id': '1', 'item_id': '1'}]
    client = MondayClient(USERNAME, '', '')
    update = client.get_updates()[0]
    get_updates.return_value = [{'id': '1', 'creator_id': '1', 'item_id': '1', 'replies': [{'id': reply_id, 'body': reply_body}]}]

    # Act 
    replies = update.get_replies()

    # Assert
    ok_(replies)
    eq_(replies[0].id, reply_id)
    eq_(replies[0].body, reply_body)


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_updates')
@patch('moncli.api_v2.add_file_to_update')
def test_should_add_file_to_update(add_file_to_update, get_updates, get_me):

    # Arrange 
    id = '12345'
    name = '33.jpg'
    url = 'https://test.monday.com/12345/33.jpg'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_updates.return_value = [{'id': '1', 'item_id': '1', 'creator_id': GET_ME_RETURN_VALUE.id}]
    add_file_to_update.return_value = {'id': '12345', 'name': name, 'url': url}
    client = MondayClient(USERNAME, '', '')
    update = client.get_updates()[0]

    # Act
    asset = update.add_file('/Users/test/33.jpg')

    # Assert
    ok_(asset != None)
    eq_(asset.id, id)
    eq_(asset.name, name)
    eq_(asset.url, url)


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_updates')
def test_should_get_files_from_update(get_updates, get_me):

    # Arrange 
    id = '12345'
    name = '33.jpg'
    url = 'https://test.monday.com/12345/33.jpg'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_updates.return_value = [{'id': '1', 'item_id': '1', 'creator_id': '1'}]
    client = MondayClient(USERNAME, '', '')
    update = client.get_updates()[0]
    get_updates.return_value = [{'id': '1', 'item_id': '1', 'creator_id': '1', 'assets': [{'id': id, 'name': name, 'url': url}]}]

    # Act
    assets = update.get_files()

    # Assert
    ok_(assets)
    eq_(assets[0].id, id)
    eq_(assets[0].name, name)
    eq_(assets[0].url, url)


@patch.object(MondayClient, 'get_me')
@patch('moncli.api_v2.get_updates')
@patch('moncli.api_v2.delete_update')
def test_should_should_update(delete_update, get_updates, get_me):

    # Arrange 
    id = '1'
    item_id = '1'
    creator_id = '1'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_updates.return_value = [{'id': id, 'item_id': item_id, 'creator_id': creator_id}]
    delete_update.return_value = {'id': id, 'item_id': item_id, 'creator_id': creator_id}
    client = MondayClient(USERNAME, '', '')
    update = client.get_updates()[0]

    # Act
    update = update.delete()

    # Assert
    ok_(update)
    eq_(update.id, id)
    eq_(update.item_id, item_id)
    eq_(update.creator_id, creator_id)