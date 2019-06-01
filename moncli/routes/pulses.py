from moncli.routes import constants
from .requests import execute_get, execute_post, execute_put, execute_delete

def get_pulses(
        api_key, 
        page = 1,
        per_page = 25, 
        offset = 0,
        order_by_latest = False,
        since = None,
        until = None):
    
    resource_url = constants.PULSES

    params = {
        'page': page,
        'per_page': per_page,
        'offset': offset,
        'order_by_latest': order_by_latest
    }

    if since != None:
        params['since'] = since

    if until != None:
        params['until'] = until

    return execute_get(api_key, resource_url, params)


def get_pulse_by_id(api_key, pulse_id):

    resource_url = constants.PULSE_BY_ID.format(pulse_id)

    return execute_get(api_key, resource_url)


def put_pulse_by_id(api_key, pulse_id, name):

    resource_url = constants.PULSE_BY_ID.format(pulse_id)

    body = {
        'name': name
    }

    return execute_put(api_key, resource_url, body)


def delete_pulse_by_id(api_key, pulse_id, archive = False):

    resource_url = constants.PULSE_BY_ID.format(pulse_id)

    params = {
        'archive': archive
    }

    return execute_delete(api_key, resource_url, params)


def get_pulse_subscribers(api_key, pulse_id, page = 1, per_page = 25, offset = 0):

    resource_url = constants.PULSE_SUBSCRIBERS.format(pulse_id)

    params = {
        'page': page,
        'per_page': per_page,
        'offset': offset
    }

    return execute_get(api_key, resource_url, params)


def put_pulse_subscriber(api_key, pulse_id, user_id, as_admin = False):

    resource_url = constants.PULSE_SUBSCRIBERS.format(pulse_id)

    body = {
        'user_id': user_id,
        'as_admin': as_admin
    }

    return execute_put(api_key, resource_url, body)


def delete_pulse_subscriber(api_key, pulse_id, user_id):

    resource_url = constants.PULSE_SUBSCRIBERS_BY_USER_ID.format(pulse_id, user_id)

    return execute_delete(api_key, resource_url)


def get_pulse_notes(api_key, pulse_id):

    resource_url = constants.PULSE_NOTES.format(pulse_id)

    return execute_get(api_key, resource_url)


def post_pulse_notes(api_key, 
        pulse_id, 
        title, 
        content, 
        owners_only = True, 
        user_id = None, 
        create_update = None):

    resource_url = constants.PULSE_NOTES.format(pulse_id)

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

    resource_url = constants.PULSE_NOTE_BY_ID.format(pulse_id, note_id)

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

    resource_url = constants.PULSE_NOTE_BY_ID.format(pulse_id, note_id)

    return execute_delete(api_key, resource_url)


def get_pulse_updates(api_key, pulse_id, page = 1, limit = 25):

    resource_url = constants.PULSE_UPDATES.format(pulse_id)

    params = {
        'page': page,
        'limit': limit
    }

    return execute_get(api_key, resource_url, params)
