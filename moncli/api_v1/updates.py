from moncli.routes import constants
from moncli.routes.requests import execute_get, execute_post, execute_delete

def get_updates(
        api_key, 
        page = 1, 
        per_page = 25, 
        offset = 0, 
        since = None, 
        until = None, 
        updated_since = None, 
        updated_until = None):

    resource_url = constants.UPDATES

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

    resource_url = constants.BOARDS

    body = {
        'user_id': user_id,
        'pulse_id': pulse_id,
        'update_text': update_text
    }

    return execute_post(api_key, resource_url, body)


def get_update_by_id(api_key, update_id):

    resource_url = constants.UPDATES_BY_ID.format(update_id)

    return execute_get(api_key, resource_url)


def delete_update_by_id(api_key, update_id):

    resource_url = constants.UPDATES_BY_ID.format(update_id)

    return execute_delete(api_key, resource_url)


def post_like_to_update(api_key, update_id, user_id):

    resource_url = constants.UPDATE_LIKE.format(update_id)

    body = {
        'user': user_id
    }

    return execute_post(api_key, resource_url, body)


def post_unlike_to_update(api_key, update_id, user_id):

    resource_url = constants.UPDATE_UNLIKE.format(update_id)

    body = {
        'user': user_id
    }

    return execute_post(api_key, resource_url, body)
