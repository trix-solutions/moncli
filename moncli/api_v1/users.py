from moncli.api_v1 import constants
from moncli.api_v1.requests import execute_get

def get_users(api_key, page = 1, per_page = 25, offset = 0, order_by_latest = False):

    resource_url = constants.USERS

    params = {
        'page': page,
        'per_page': per_page,
        'offset': offset,
        'order_by_latest': order_by_latest
    }

    return execute_get(api_key, resource_url, params)


def get_user_by_id(api_key, user_id):

    resource_url = constants.USER_BY_ID.format(user_id)

    return execute_get(api_key, resource_url)


def get_user_posts(api_key, user_id, page = 1, per_page = 25, offset = 0):

    resource_url = constants.USER_POSTS.format(user_id)

    params = {
        'page': page,
        'per_page': per_page,
        'offset': offset
    }

    return execute_get(api_key, resource_url, params)


def get_user_newsfeed(api_key, user_id, page = 1, per_page = 25, offset = 0):

    resource_url = constants.USER_NEWSFEED.format(user_id)

    params = {
        'page': page,
        'per_page': per_page,
        'offset': offset
    }

    return execute_get(api_key, resource_url, params)


def get_user_unread_feed(api_key, user_id, page = 1, per_page = 25, offset = 0):

    resource_url = constants.USER_UNREAD_FEED.format(user_id)

    params = {
        'page': page,
        'per_page': per_page,
        'offset': offset
    }

    return execute_get(api_key, resource_url, params)

