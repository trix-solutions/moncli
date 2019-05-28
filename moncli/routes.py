import requests

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

def get_users(api_key, page = 0, per_page = 25, offset = 0, order_by_latest = False):

    resource_url = '{}/users.json'.format(format_url())

    params = {
        'api_key': api_key,
        'page': page,
        'per_page': per_page,
        'offset': offset,
        'order_by_latest': order_by_latest
    }

    resp = requests.get(resource_url, params=params)

    if resp.status_code == 200:
        return resp.json()

    raise_mondayapi_error('GET', 'users.json', resp)


def get_user_by_id(api_key, user_id):

    resource_url = '{}/users/{}.json'.format(
        format_url(),
        user_id)

    params = {
        'api_key': api_key,
        'id': user_id
    }



def get_boards(api_key, per_page = 25, only_globals = False, order_by_latest = False):

    resource_url = '{}/boards.json'.format(format_url())

    params = {
        'api_key': api_key,
        'per_page': per_page,
        'only_globals': only_globals,
        'order_by_latest': order_by_latest
    }

    resp = requests.get(resource_url, params=params)

    if resp.status_code == 200:
        return resp.json()

    raise_mondayapi_error('GET', 'boards.json', resp)


def get_board_by_id(api_key, board_id):

    resource_url = "{}/boards/{}.json".format(
        format_url(),
        board_id)

    params = {
        'api_key': api_key
    }

    resp = requests.get(resource_url, params=params)

    if resp.status_code == 200:
        return resp.json()

    raise_mondayapi_error('GET', 'boards/{}.json'.format(board_id), resp)

    
def format_url():

    return "{}:{}/{}".format(
        BASE_URL, 
        PORT, 
        API_VERSION)


def raise_mondayapi_error(method, resource_url, resp):

    error_url = "{}:{}/{}/{}".format(
        BASE_URL, 
        PORT, 
        API_VERSION, 
        resource_url)
    
    raise MondayApiError(
        method, 
        error_url, 
        resp.status_code,
         resp.text)


class MondayApiError(Exception):

    def __init__(self, method, error_url, error_code, message):
        self.method = method
        self.error_url = error_url
        self.error_code = error_code
        self.message = message