from . import constants
from .requests import execute_get, execute_post, execute_put, execute_delete

def get_boards(api_key, per_page = 25, only_globals = False, order_by_latest = False):

    resource_url = constants.BOARDS

    params = {
        'per_page': per_page,
        'only_globals': only_globals,
        'order_by_latest': order_by_latest
    }

    return execute_get(api_key, resource_url, params)


def post_board(api_key, user_id, name, description, board_kind):

    resource_url = constants.BOARDS

    body = {
        'user_id': user_id,
        'name': name,
        'description': description,
        'board_kind': board_kind
    }

    return execute_post(api_key, resource_url, body)


def get_board_by_id(api_key, board_id):

    resource_url = constants.BOARD_BY_ID.format(board_id)

    return execute_get(api_key, resource_url)


def delete_board_by_id(api_key, board_id):

    resource_url = constants.BOARD_BY_ID.format(board_id)

    return execute_delete(api_key, resource_url)


def get_board_groups(api_key, board_id, show_archived = False, show_deleted = False):

    resource_url = constants.BOARD_GROUPS.format(board_id)

    params = {
        'show_archived': show_archived,
        'show_deleted': show_deleted
    }

    return execute_get(api_key, resource_url, params)


def put_board_group(api_key, board_id, group_id, title, color):

    resource_url = constants.BOARD_GROUPS.format(board_id)

    body = {
        'group_id': group_id,
        'title': title,
        'color': color
    }

    return execute_put(api_key, resource_url, body)


def post_board_group(api_key, board_id, title):

    resource_url = constants.BOARD_GROUPS.format(board_id)

    body = {
        'title': title
    }

    return execute_post(api_key, resource_url, body)


def post_move_board_group(api_key, board_id, group_id, user_id, dest_board_id):

    resource_url = constants.BOARD_MOVE_GROUP.format(board_id, group_id)

    body = {
        'user_id': user_id,
        'dest_board_id': dest_board_id
    }

    return execute_post(api_key, resource_url, body)


def delete_board_group(api_key, board_id, group_id):

    resource_url = constants.BOARD_GROUP_BY_ID.format(board_id, group_id)

    return execute_delete(api_key, resource_url)


def get_board_columns(api_key, board_id, all_columns = False):

    resource_url = constants.BOARD_COLUMNS.format(board_id)

    params = {
        'all_columns': all_columns
    }

    return execute_get(api_key, resource_url, params)


def post_board_column(api_key, board_id, title, column_type, labels = None):

    resource_url = constants.BOARD_COLUMNS.format(board_id)

    body = {
        'title': title,
        'type': column_type
    }

    if column_type == 'status' and labels != None:
        body['labesl'] = labels

    return execute_post(api_key, resource_url, body)


def put_board_column(api_key, board_id, column_id, title = None, status = None, labels = None):

    resource_url = constants.BOARD_COLUMN_BY_ID.format(board_id, column_id)

    body = {}

    if title != None:
        body['title'] = title

    if status != None:
        body['status'] = status

    if labels != None:
        body['labels'] = labels

    return execute_put(api_key, resource_url, body)\


def delete_board_column(api_key, board_id, column_id):

    resource_url = constants.BOARD_COLUMN_BY_ID.format(board_id, column_id)

    return execute_delete(api_key, resource_url)


def get_board_column_value(api_key, board_id, column_id, pulse_id, return_as_array = False):

    resource_url = constants.BOARD_COLUMN_VALUE.format(board_id, column_id)

    params = {
        'pulse_id': pulse_id,
        'return_as_array': return_as_array
    }

    return execute_get(api_key, resource_url, params)


def put_board_text_column(api_key, board_id, column_id, pulse_id, text):

    resource_url = constants.BOARD_TEXT_COLUMN.format(board_id, column_id)

    body = {
        'pulse_id': pulse_id,
        'text': text,
    }

    return execute_put(api_key, resource_url, body)


def put_board_person_column(api_key, board_id, column_id, pulse_id, user_id):

    resource_url = constants.BOARD_PERSON_COLUMN.format(board_id, column_id)

    body = {
        'pulse_id': pulse_id,
        'user_id': user_id,
    }

    return execute_put(api_key, resource_url, body)


def put_board_status_column(api_key, board_id, column_id, pulse_id, color_index, update_id = None):

    resource_url = constants.BOARD_STATUS_COLUMN.format(board_id, column_id)

    body = {
        'pulse_id': pulse_id,
        'color_index': color_index,
    }

    if update_id != None:
        body['update_id'] = update_id

    return execute_put(api_key, resource_url, body)


def put_board_date_column(api_key, board_id, column_id, pulse_id, date_str):

    resource_url = constants.BOARD_DATE_COLUMN.format(board_id, column_id)

    body = {
        'pulse_id': pulse_id,
        'date_str': str(date_str)
    }

    return execute_put(api_key, resource_url, body)


def put_board_numeric_column(api_key, board_id, column_id, pulse_id, value):

    resource_url = constants.BOARD_NUMERIC_COLUMN.format(board_id, column_id)

    body = {
        'pulse_id': pulse_id,
        'value': str(value)
    }

    return execute_put(api_key, resource_url, body)


def put_board_tags_column(api_key, board_id, column_id, pulse_id, tags):

    resource_url = constants.BOARD_TAGS_COLUMN.format(board_id, column_id)

    body = {
        'pulse_id': pulse_id,
        'tags': ', '.join(tags)
    }

    return execute_put(api_key, resource_url, body)


def put_board_timeline_column(api_key, board_id, column_id, pulse_id, from_time, to_time):

    resource_url = constants.BOARD_TIMELINE_COLUMN.format(board_id, column_id)

    body = {
        'pulse_id': pulse_id,
        'from': from_time,
        'to': to_time
    }

    return execute_put(api_key, resource_url, body)


def get_board_pulses(api_key, board_id, page = 1, per_page = 25, order_by = None):

    resource_url = constants.BOARD_PULSES.format(board_id)

    params = {
        'page': page,
        'per_page': per_page
    }

    if order_by != None:
        params['order_by'] = order_by

    return execute_get(api_key, resource_url, params)


def post_board_pulse(
        api_key, 
        board_id, 
        user_id, 
        group_id, 
        name, 
        photo_from_url = None, 
        update_text = None, 
        add_to_bottom = False):

    resource_url = constants.BOARD_PULSES.format(board_id)

    body = {
        'user_id': user_id,
        'group_id': group_id,
        'pulse[name]': name,
        'add_to_bottom': add_to_bottom
    }

    if photo_from_url != None:
        body['photo_from_url'] = photo_from_url

    if update_text != None:
        body['update[text]'] = update_text

    return execute_post(api_key, resource_url, body)


def post_board_pulse_duplicate(api_key, board_id, pulse_id, group_id, owner_id):

    resource_url = constants.BOARD_DUPLICATE_PULSE.format(board_id, pulse_id)

    body = {
        'group_id': group_id,
        'owner_id': owner_id
    }

    return execute_post(api_key, resource_url, body)


def post_board_pulses_to_new_board(api_key, board_id, user_id, group_id, pulse_ids, dest_board_id = None, force_move_to_board = False):

    resource_url = constants.BOARD_MOVE_GROUP.format(board_id)

    body = {
        'user_id': user_id,
        'group_id': group_id,
        'pulse_ids': pulse_ids
    }

    if (dest_board_id != None):
        body['dest_board_id'] = dest_board_id
        body['force_move_to_board'] = force_move_to_board

    return execute_post(api_key, resource_url, body)


def get_board_subscribers(api_key, board_id, page = 1, per_page = 25, offset = 0):

    resource_url = constants.BOARD_SUBSCRIBERS.format(board_id)

    params = {
        'page': page,
        'per_page': per_page,
        'offset': offset
    }

    return execute_get(api_key, resource_url, params)


def put_board_subscriber(api_key, board_id, user_id, as_admin = False):

    resource_url = constants.BOARD_SUBSCRIBERS.format(board_id)

    body = {
        'as_admin': as_admin
    }

    return execute_put(api_key, resource_url, body)


def delete_board_subscriber_by_id(api_key, board_id, user_id):

    resource_url = constants.BOARD_SUBSCRIBERS_BY_ID.format(board_id, user_id)

    execute_delete(api_key, resource_url)