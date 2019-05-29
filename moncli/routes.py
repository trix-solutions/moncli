import requests, json

BASE_URL = 'https://api.monday.com'
PORT = '443'
API_VERSION = 'v1'

# User route signatures
USERS = 'users.json'
USER_BY_ID = 'users/{}.json'
USER_POSTS = 'users/{}/posts.json'
USER_NEWSFEED = 'users/{}/newsfeed.json'
USER_UNREAD_FEED = 'users/{}/unread_feed'

# Updates route signatures
UPDATES = 'updates.json'
UPDATES_BY_ID = 'updates/{}.json'
UPDATE_LIKE = 'updates/{}/like.json'
UPDATE_UNLIKE = 'updates/{}/unlike.json'

# Pulses route signatures
PULSES = 'pulses.json'
PULSE_BY_ID = 'pulses/{}.json'
PULSE_SUBSCRIBERS = 'pulses/{}/subscribers.json'
PULSE_SUBSCRIBERS_BY_USER_ID = 'pulses/{}/subscribers/{}.json'
PULSE_NOTES = 'pulses/{}/notes.json'
PULSE_NOTE_BY_ID = 'pulses/{}/notes/{}.json'
PULSE_UPDATES = 'pulses/{}/updates.json'

# Boards route signatures
BOARDS = 'boards.json'
BOARD_BY_ID = 'boards/{}.json'
BOARD_GROUPS = 'boards/{}/groups.json'
BOARD_MOVE_GROUP = 'boards/{}/groups/{}/move.json'
BOARD_GROUP_BY_ID = 'boards/{}/groups/{}.json'
BOARD_COLUMNS = 'boards/{}/columns.json'
BOARD_COLUMN_BY_ID = 'boards/{}/columns/{}.json'
BOARD_VALUE_COLUMN = 'boards/{}/columns/{}/value.json'
BOARD_TEXT_COLUMN = 'boards/{}/columns/{}/text.json'
BOARD_PERSON_COLUMN = 'boards/{}/columns/{}/person.json'
BOARD_STATUS_COLUMN = 'boards/{}/columns/{}/status.json'
BOARD_DATE_COLUMN = 'boards/{}/columns/{}/date.json'
BOARD_NUMERIC_COLUMN = 'boards/{}/columns/{}/numeric.json'
BOARD_TAGS_COLUMN = 'boards/{}/columns/{}/tags.json'
BOARD_TIMELINE_COLUMN = 'boards/{}/columns/{}/timeline.json'
BOARD_PULSES = 'boards/{}/pulses.json'
BOARD_DUPLICATE_PULSE = 'boards/{}/pulses/{}/duplicate.json'
BOARD_MOVE_PULSES = 'boards/{}/pulses/move.json'
BOARD_SUBSCRIBERS = 'boards/{}/subscribers.json'
BOARD_SUBSCRIBERS_BY_ID = 'boards/{}/subscribers/{}.json'

# Tags route signatures
TAGS_BY_ID = 'tags/{}.json'

def get_users(api_key, page = 1, per_page = 25, offset = 0, order_by_latest = False):

    resource_url = USERS

    params = {
        'page': page,
        'per_page': per_page,
        'offset': offset,
        'order_by_latest': order_by_latest
    }

    return execute_get(api_key, resource_url, params)


def get_user_by_id(api_key, user_id):

    resource_url = USER_BY_ID.format(user_id)

    return execute_get(api_key, resource_url)


def get_user_posts(api_key, user_id, page = 1, per_page = 25, offset = 0):

    resource_url = USER_POSTS.format(user_id)

    params = {
        'page': page,
        'per_page': per_page,
        'offset': offset
    }

    return execute_get(api_key, resource_url, params)


def get_user_newsfeed(api_key, user_id, page = 1, per_page = 25, offset = 0):

    resource_url = USER_NEWSFEED.format(user_id)

    params = {
        'page': page,
        'per_page': per_page,
        'offset': offset
    }

    return execute_get(api_key, resource_url, params)


def get_user_unread_feed(api_key, user_id, page = 1, per_page = 25, offset = 0):

    resource_url = USER_UNREAD_FEED.format(user_id)

    params = {
        'page': page,
        'per_page': per_page,
        'offset': offset
    }

    return execute_get(api_key, resource_url, params)


def get_updates(
        api_key, 
        page = 1, 
        per_page = 25, 
        offset = 0, 
        since = None, 
        until = None, 
        updated_since = None, 
        updated_until = None):

    resource_url = UPDATES

    params = {
        'page': page,
        'per_page': per_page,
        'offset': offset
    }

    if since != None:
        params['since'] = since

    if since != None:
        params['until'] = until

    if since != None:
        params['updated_since'] = updated_since

    if since != None:
        params['updated_until'] = updated_until

    return execute_get(api_key, resource_url, params)


def post_update(api_key, user_id, pulse_id, update_text):

    resource_url = BOARDS

    body = {
        'user_id': user_id,
        'pulse_id': pulse_id,
        'update_text': update_text
    }

    return execute_post(api_key, resource_url, body)


def get_update_by_id(api_key, update_id):

    resource_url = UPDATES_BY_ID.format(update_id)

    return execute_get(api_key, resource_url)


def delete_update_by_id(api_key, update_id):

    resource_url = UPDATES_BY_ID.format(update_id)

    return execute_delete(api_key, resource_url)


def post_like_to_update(api_key, update_id, user_id):

    resource_url = UPDATE_LIKE.format(update_id)

    body = {
        'user': user_id
    }

    return execute_post(api_key, resource_url, body)


def post_unlike_to_update(api_key, update_id, user_id):

    resource_url = UPDATE_UNLIKE.format(update_id)

    body = {
        'user': user_id
    }

    return execute_post(api_key, resource_url, body)


def get_pulses(
        api_key, 
        page = 1,
        per_page = 25, 
        offset = 0,
        order_by_latest = False,
        since = None,
        until = None):
    
    resource_url = PULSES

    params = {
        'page': page,
        'per_page': per_page,
        'offset': offset,
        'order_by_latest': order_by_latest
    }

    if since != None:
        params['since'] = since

    if since != None:
        params['until'] = until

    return execute_get(api_key, resource_url, params)


def get_pulse_by_id(api_key, pulse_id):

    resource_url = PULSE_BY_ID.format(pulse_id)

    return execute_get(api_key, resource_url)


def put_pulse_by_id(api_key, pulse_id, name):

    resource_url = PULSE_BY_ID.format(pulse_id)

    body = {
        'name': name
    }

    return execute_put(api_key, resource_url, body)


def delete_pulse_by_id(api_key, pulse_id, archive = False):

    resource_url = PULSE_BY_ID.format(pulse_id)

    params = {
        'archive': archive
    }

    return execute_delete(api_key, resource_url, params)


def get_pulse_subscribers(api_key, pulse_id, page = 1, per_page = 25, offset = 0):

    resource_url = PULSE_SUBSCRIBERS.format(pulse_id)

    params = {
        'page': page,
        'per_page': per_page,
        'offset': offset
    }

    return execute_get(api_key, resource_url, params)


def put_pulse_subscriber(api_key, pulse_id, user_id, as_admin = False):

    resource_url = PULSE_SUBSCRIBERS.format(pulse_id)

    body = {
        'user_id': user_id,
        'as_admin': as_admin
    }

    return execute_put(api_key, resource_url, body)


def delete_pulse_subscriber(api_key, pulse_id, user_id):

    resource_url = PULSE_SUBSCRIBERS_BY_USER_ID.format(pulse_id, user_id)

    return execute_delete(api_key, resource_url)


def get_pulse_notes(api_key, pulse_id):

    resource_url = PULSE_NOTES.format(pulse_id)

    return execute_get(api_key, resource_url)


def post_pulse_notes(api_key, 
        pulse_id, 
        title, 
        content, 
        owners_only = True, 
        user_id = None, 
        create_update = None):

    resource_url = PULSE_NOTES.format(pulse_id)

    body = {
        'title': title,
        'content': content,
        'owners_only': owners_only
    }

    if user_id != None:
        body['user_id'] = user_id

        if create_update != None:
            body['create_update'] = create_update

    return execute_post(api_key, resource_url, body)


def put_pulse_note_by_id(
        api_key, 
        pulse_id,
        note_id,
        title,
        content,
        user_id = None,
        create_update = None):

    resource_url = PULSE_NOTE_BY_ID.format(pulse_id, note_id)

    body = {
        'title': title,
        'content': content
    }

    if user_id != None:
        body['user_id'] = user_id

        if create_update != None:
            body['create_update'] = create_update

    return execute_put(api_key, resource_url, body)


def delete_pulse_note_by_id(api_key, pulse_id, note_id):

    resource_url = PULSE_NOTE_BY_ID.format(pulse_id, note_id)

    return execute_delete(api_key, resource_url)


def get_pulse_updates(api_key, pulse_id, page = 1, limit = 25):

    resource_url = PULSE_UPDATES.format(pulse_id)

    params = {
        'page': page,
        'limit': limit
    }

    return execute_get(api_key, resource_url, params)
    

def get_boards(api_key, per_page = 25, only_globals = False, order_by_latest = False):

    resource_url = BOARDS

    params = {
        'per_page': per_page,
        'only_globals': only_globals,
        'order_by_latest': order_by_latest
    }

    return execute_get(api_key, resource_url, params)


def get_board_by_id(api_key, board_id):

    resource_url = BOARD_BY_ID.format(board_id)

    return execute_get(api_key, resource_url)

    
def format_url(resource_url):

    return "{}:{}/{}/{}".format(
        BASE_URL, 
        PORT, 
        API_VERSION,
        resource_url)


def raise_mondayapi_error(method, resource_url, resp):
    
    raise MondayApiError(
        method, 
        format_url(resource_url), 
        resp.status_code,
         resp.text)


def execute_get(api_key, resource_url, params = None):

    monday_params = MondayQueryParameters(api_key)

    if params != None:
        monday_params.add_params(params)

    resp = requests.get(
        format_url(resource_url), 
        params=monday_params.to_dict())

    if resp.status_code == 200:
        return resp.json()

    raise_mondayapi_error('GET', resource_url, resp)


def execute_post(api_key, resource_url, body):

    monday_params = MondayQueryParameters(api_key)

    data = json.dumps(body)

    resp = requests.post(
        format_url(resource_url),
        data,
        params=monday_params.to_dict())

    if resp.status_code == 200 or resp.status_code == 201:
        return resp.json()

    raise_mondayapi_error('POST', resource_url, resp)


def execute_put(api_key, resource_url, body):

    monday_params = MondayQueryParameters(api_key)

    data = json.dumps(body)

    resp = requests.post(
        format_url(resource_url),
        data,
        params=monday_params.to_dict())

    if resp.status_code == 200:
        return resp.json()

    raise_mondayapi_error('PUT', resource_url, resp)


def execute_delete(api_key, resource_url, params = None):

    monday_params = MondayQueryParameters(api_key)

    if params != None:
        monday_params.add_params(params)

    resp = requests.delete(
        format_url(resource_url), 
        params=monday_params.to_dict())

    if resp.status_code == 200:
        return resp.json()

    raise_mondayapi_error('GET', resource_url, resp)


class MondayApiError(Exception):

    def __init__(self, method, error_url, error_code, message):
        self.method = method
        self.error_url = error_url
        self.error_code = error_code
        self.message = message


class MondayQueryParameters():

    def __init__(self, api_key):

        self.__dict = { 'api_key': api_key}


    def add_param(self, name, value):

        self.__dict[name] = value

    
    def add_params(self, params_dict):

        for key in params_dict:
            self.add_param(key, params_dict[key])

    
    def to_dict(self):

        return self.__dict