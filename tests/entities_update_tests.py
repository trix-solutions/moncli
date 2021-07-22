from unittest.mock import patch
from nose.tools import ok_, eq_

from moncli import client, entities as en

TEST_USER = en.User(**{'creds': None, 'id': '1', 'email': 'foo.bar@test.com'})


@patch('moncli.api_v2.get_updates')
def test_update_should_return_list_of_replies(get_updates):

    # Arrange
    get_updates.return_value = [{'id': '1', 'creator_id': '1', 'item_id': '1', 'replies': [{'id': '2', 'creator_id': '1'}]}]
    
    # Act
    updates = client.get_updates()
    
    # Assert
    ok_(updates != None)
    eq_(len(updates), 1)
    eq_(len(updates[0].replies), 1)


@patch('moncli.api_v2.get_updates')
@patch('moncli.api_v2.get_users')
def test_update_should_return_creator(get_users, get_updates):

    # Arrange  
    get_updates.return_value = [{'id': '1', 'creator_id': '1', 'item_id': '1'}]
    get_users.return_value = [TEST_USER.to_primitive()]
    update = client.get_updates()[0]

    # Assert
    ok_(update != None)
    eq_(update.creator.to_primitive(), TEST_USER.to_primitive())



@patch('moncli.api_v2.get_updates')
@patch('moncli.api_v2.get_users')
def test_update_should_return_creator_of_update_reply(get_users, get_updates):

    # Arrange
    get_updates.return_value = [{'id': '1', 'creator_id': '1', 'item_id': '1', 'replies': [{'id': '2', 'creator_id': '1'}]}]
    get_users.return_value = [TEST_USER.to_primitive()]
    reply = client.get_updates()[0].replies[0]

    # Assert
    ok_(reply != None)
    eq_(reply.creator.to_primitive(), TEST_USER.to_primitive())



@patch('moncli.api_v2.get_updates')
def test_should_return_list_of_replies_for_an_update(get_updates):

    # Arrange
    reply_id = '12345'
    reply_body = 'Reply text'
    get_updates.return_value = [{'id': '1', 'creator_id': '1', 'item_id': '1'}]
    update = client.get_updates()[0]
    get_updates.return_value = [{'id': '1', 'creator_id': '1', 'item_id': '1', 'replies': [{'id': reply_id, 'body': reply_body}]}]

    # Act 
    replies = update.get_replies()

    # Assert
    ok_(replies)
    eq_(replies[0].id, reply_id)
    eq_(replies[0].body, reply_body)



@patch('moncli.api_v2.get_updates')
@patch('moncli.api_v2.add_file_to_update')
def test_should_add_file_to_update(add_file_to_update, get_updates):

    # Arrange 
    id = '12345'
    name = '33.jpg'
    url = 'https://test.monday.com/12345/33.jpg'
    get_updates.return_value = [{'id': '1', 'item_id': '1', 'creator_id': TEST_USER.id}]
    add_file_to_update.return_value = {'id': '12345', 'name': name, 'url': url}
    update = client.get_updates()[0]

    # Act
    asset = update.add_file('/Users/test/33.jpg')

    # Assert
    ok_(asset != None)
    eq_(asset.id, id)
    eq_(asset.name, name)
    eq_(asset.url, url)



@patch('moncli.api_v2.get_updates')
def test_should_get_files_from_update(get_updates):

    # Arrange 
    id = '12345'
    name = '33.jpg'
    url = 'https://test.monday.com/12345/33.jpg'
    get_updates.return_value = [{'id': '1', 'item_id': '1', 'creator_id': '1'}]   
    update = client.get_updates()[0]
    get_updates.return_value = [{'id': '1', 'item_id': '1', 'creator_id': '1', 'assets': [{'id': id, 'name': name, 'url': url}]}]

    # Act
    assets = update.get_files()

    # Assert
    ok_(assets)
    eq_(assets[0].id, id)
    eq_(assets[0].name, name)
    eq_(assets[0].url, url)



@patch('moncli.api_v2.get_updates')
@patch('moncli.api_v2.delete_update')
def test_should_should_update(delete_update, get_updates):

    # Arrange 
    id = '1'
    item_id = '1'
    creator_id = '1'
    get_updates.return_value = [{'id': id, 'item_id': item_id, 'creator_id': creator_id}]
    delete_update.return_value = {'id': id, 'item_id': item_id, 'creator_id': creator_id}
    update = client.get_updates()[0]

    # Act
    update = update.delete()

    # Assert
    ok_(update)
    eq_(update.id, id)
    eq_(update.item_id, item_id)
    eq_(update.creator_id, creator_id)