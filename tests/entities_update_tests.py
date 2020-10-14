import json
from unittest.mock import patch
from nose.tools import ok_, eq_

import moncli.entities as e

USERNAME = 'test.user@foobar.org' 
GET_ME_RETURN_VALUE = e.user.User(**{'creds': None, 'id': '1', 'email': USERNAME})

@patch('moncli.api_v2.add_file_to_update')
@patch('moncli.api_v2.get_updates')
@patch.object(e.MondayClient, 'get_me')
def test_should_get_updates(get_me, get_updates, add_file_to_update):

    # Arrange 
    id = '1'
    body = 'Hello, world!'
    get_me.return_value = GET_ME_RETURN_VALUE
    get_updates.return_value = [{'id': id, 'body': body}]
    add_file_to_update.return_value = {'id': '12345', 'name': '33.jpg', 'url': 'https://test.monday.com/12345/33.jpg'}
    client = e.MondayClient(USERNAME, '', '')
    update = client.get_updates()[0]

    # Act
    asset = update.add_file('/Users/test/33.jpg')

    # Assert
    ok_(asset != None)
    eq_(asset.id, '12345')
    eq_(asset.name, '33.jpg')
    eq_(asset.url, 'https://test.monday.com/12345/33.jpg')