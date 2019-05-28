import requests

BASE_URL = 'https://api.monday.com'
PORT = '443'
API_VERSION = 'v1'

def get_users(api_key, page = 0, per_page = 25, offset = 0, order_by_latest = false):

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