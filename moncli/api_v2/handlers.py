from typing import List, Dict, Any

from ..enums import BoardKind, ColumnType, NotificationTargetType, WebhookEventType, WorkspaceKind
from . import graphql as util, requests, constants
from .exceptions import MondayApiError


def create_board(api_key: str, board_name: str, board_kind: BoardKind, *args, **kwargs):
    args = get_field_list(constants.DEFAULT_BOARD_QUERY_FIELDS)
    kwargs = get_method_arguments(constants.CREATE_BOARD_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_name'] = util.StringValue(board_name)
    kwargs['board_kind'] = util.EnumValue(board_kind)
    return execute_mutation(api_key, constants.CREATE_BOARD, *args,  **kwargs)


def get_boards(api_key: str, *args, **kwargs) -> List[Dict[str, Any]]:
    args = get_field_list(constants.DEFAULT_BOARD_QUERY_FIELDS)
    kwargs = get_method_arguments(constants.BOARDS_OPTIONAL_PARAMS, **kwargs)
    operation = util.create_query(constants.BOARDS, *args, **kwargs)
    return requests.execute_query(api_key, operation=operation)[constants.BOARDS]   


def archive_board(api_key: str, board_id: str, *args, **kwargs):
    args = get_field_list(constants.DEFAULT_BOARD_QUERY_FIELDS)
    kwargs = get_method_arguments(constants.ARCHIVE_BOARD_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    return execute_mutation(api_key, constants.ARCHIVE_BOARD, *args, **kwargs)

    
def create_column(api_key: str, board_id: str, title: str, column_type: ColumnType, *args, **kwargs):
    args = get_field_list(constants.DEFAULT_COLUMN_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CREATE_COLUMN_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['title'] = util.StringValue(title)
    kwargs['column_type'] = util.EnumValue(column_type)
    return execute_mutation(api_key, constants.CREATE_COLUMN, *args, **kwargs)


def change_column_value(api_key: str, item_id: str, column_id: str, board_id: str, value: str, *args, **kwargs):
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CHANGE_COLUMN_VALUE_OPTIONAL_PARAMS)
    kwargs['item_id'] = util.IntValue(item_id)
    kwargs['column_id'] = util.StringValue(column_id)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['value'] = util.JsonValue(value)
    return execute_mutation(api_key, constants.CHANGE_COLUMN_VALUE, *args, **kwargs)


def change_multiple_column_value(api_key: str, item_id: str, board_id: str, column_values: dict, *args, **kwargs):
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CHANGE_MULTIPLE_COLUMN_VALUES_OPTIONAL_PARAMS, **kwargs)
    kwargs['item_id'] = util.IntValue(item_id)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['column_values'] = util.JsonValue(column_values)
    return execute_mutation(api_key, constants.CHANGE_MULTIPLE_COLUMN_VALUES, *args, **kwargs)


def get_assets(api_key: str, ids: list, *args, **kwargs):
    args = get_field_list(constants.DEFAULT_ASSET_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.ASSETS_OPTIONAL_PARAMS, **kwargs)
    ids = [util.IntValue(id).value for id in ids]
    kwargs['ids'] = util.ListValue(ids)
    return execute_query(api_key, constants.ASSETS, *args, **kwargs)


def duplicate_group(api_key: str, board_id: str, group_id: str, *args, **kwargs):
    kwargs = get_method_arguments(constants.DUPLICATE_GROUP_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['group_id'] = util.StringValue(group_id)
    return execute_mutation(api_key, constants.DUPLICATE_GROUP, *args, **kwargs)


def create_group(api_key: str, board_id: str, group_name: str, *args, **kwargs):
    kwargs = get_method_arguments(constants.CREATE_GROUP_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['group_name'] = util.StringValue(group_name)
    return execute_mutation(api_key, constants.CREATE_GROUP, *args, **kwargs)


def archive_group(api_key: str, board_id: str, group_id: str, *args, **kwargs):
    kwargs = get_method_arguments(constants.ARCHIVE_GROUP_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['group_id'] = util.StringValue(group_id)    
    return execute_mutation(api_key, constants.ARCHIVE_GROUP, *args, **kwargs)


def delete_group(api_key: str, board_id: str, group_id: str, *args, **kwargs):
    kwargs = get_method_arguments(constants.DELETE_GROUP_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['group_id'] = util.StringValue(group_id)       
    return execute_mutation(api_key, constants.DELETE_GROUP, *args, **kwargs)


def create_item(api_key: str, item_name: str, board_id: str, *args, **kwargs):
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CREATE_ITEM_OPTIONAL_PARAMS, **kwargs)
    kwargs['item_name'] = util.StringValue(item_name)
    kwargs['board_id'] = util.IntValue(board_id)    
    return execute_mutation(api_key, constants.CREATE_ITEM, *args, **kwargs)


def get_items(api_key: str, *args, **kwargs):
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.ITEMS_OPTIONAL_PARAMS, **kwargs) 
    return execute_query(api_key, constants.ITEMS, *args, **kwargs)


def get_items_by_column_values(api_key: str, board_id: str, column_id: str, column_value: str, *args, **kwargs):
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.ITEMS_BY_COLUMN_VALUES_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['column_id'] = util.StringValue(column_id)
    kwargs['column_value'] = util.StringValue(column_value)
    return execute_query(api_key, constants.ITEMS_BY_COLUMN_VALUES, *args, **kwargs)


def move_item_to_group(api_key: str, item_id: str, group_id: str, *args, **kwargs):
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.MOVE_ITEM_TO_GROUP_OPTIONAL_PARAMS, **kwargs)
    kwargs['item_id'] = util.IntValue(item_id)
    kwargs['group_id'] = util.StringValue(group_id)
    return execute_mutation(api_key, constants.MOVE_ITEM_TO_GROUP, *args, **kwargs)


def archive_item(api_key: str, item_id: str, *args, **kwargs):
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.ARCHIVE_ITEM_OPTIONAL_PARAMS, **kwargs)
    kwargs['item_id'] = util.IntValue(item_id)
    return execute_mutation(api_key, constants.ARCHIVE_ITEM, *args, **kwargs)


def delete_item(api_key: str, item_id: str, *args, **kwargs):
    args = get_field_list(constants.DEFAULT_ITEM_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.DELETE_ITEM_OPTIONAL_PARAMS, **kwargs)
    kwargs['item_id'] = util.IntValue(item_id)
    return execute_mutation(api_key, constants.DELETE_ITEM, *args, **kwargs)


def create_update(api_key: str, body: str, item_id: str, *args, **kwargs):
    args = get_field_list(constants.DEFAULT_UPDATE_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CREATE_UPDATE_OPTIONAL_PARAMS, **kwargs)
    kwargs['body'] = util.StringValue(body)
    kwargs['item_id'] = util.IntValue(item_id)
    return execute_mutation(api_key, constants.CREATE_UPDATE, *args, **kwargs)


def get_updates(api_key: str, *args, **kwargs):
    args = get_field_list(constants.DEFAULT_UPDATE_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.UPDATES_OPTIONAL_PARAMS, **kwargs)
    return execute_query(api_key, constants.UPDATES, *args, **kwargs)


def create_notification(api_key: str, text: str, user_id: str, target_id: str, target_type: NotificationTargetType, *args, **kwargs):
    kwargs = get_method_arguments(constants.CREATE_NOTIFICATION_OPTIONAL_PARAMS, **kwargs)
    kwargs['text'] = util.StringValue(text)
    kwargs['user_id'] = util.IntValue(user_id)
    kwargs['target_id'] = util.IntValue(target_id)
    kwargs['target_type'] = util.EnumValue(target_type)    
    return execute_mutation(api_key, constants.CREATE_NOTIFICATION, *args, **kwargs)


def create_or_get_tag(api_key: str, tag_name: str, *args, **kwargs):
    kwargs = get_method_arguments(constants.CREATE_OR_GET_TAG_OPTIONAL_PARAMS, **kwargs)
    kwargs['tag_name'] = util.StringValue(tag_name)
    return execute_mutation(api_key, constants.CREATE_OR_GET_TAG, *args, **kwargs)


def get_tags(api_key: str, *args, **kwargs):
    kwargs = get_method_arguments(constants.TAGS_OPTIONAL_PARAMS, **kwargs)
    return execute_query(api_key, constants.TAGS, *args, **kwargs)


def add_file_to_update(api_key: str, update_id: str, file_path: str, *args, **kwargs):
    name = constants.ADD_FILE_TO_UPDATE
    args = get_field_list(constants.DEFAULT_ASSET_QUERY_FIELDS, *args)
    kwargs['file'] = util.FileValue('$file')
    kwargs['update_id'] = util.IntValue(update_id)
    operation = util.create_mutation(name, *args, **kwargs)
    operation.add_query_variable('file', 'File!')
    result = requests.upload_file(api_key, file_path, operation=operation)
    return result[name]


def add_file_to_column(api_key: str, item_id: str, column_id: str, file_path: str, *args, **kwargs):
    name = constants.ADD_FILE_TO_COLUMN
    args = get_field_list(constants.DEFAULT_ASSET_QUERY_FIELDS)
    kwargs['file'] = util.FileValue('$file')
    kwargs['item_id'] = util.IntValue(item_id)
    kwargs['column_id'] = util.StringValue(column_id)
    operation = util.create_mutation(name, *args, **kwargs)
    operation.add_query_variable('file', 'File!')
    result = requests.upload_file(api_key, file_path, operation=operation)
    return result[name]


def get_users(api_key: str, *args, **kwargs):
    kwargs = get_method_arguments(constants.USERS_OPTIONAL_PARAMS, **kwargs)
    return execute_query(api_key, constants.USERS, *args, **kwargs)


def get_teams(api_key: str, *args, **kwargs):
    kwargs = get_method_arguments(constants.TEAMS_OPTIONAL_PARAMS, **kwargs)
    return execute_query(api_key, constants.TEAMS, *args, **kwargs)


def get_me(api_key: str, *args, **kwargs):
    return execute_query(api_key, constants.ME, *args, **kwargs)


def get_account(api_key: str, *args, **kwargs):
    return execute_query(api_key, constants.ACCOUNT, *args, **kwargs)


def create_webhook(api_key: str, board_id: str, url: str, event: WebhookEventType, *args, **kwargs):
    kwargs = get_method_arguments(constants.CREATE_WEBHOOK_OPTIONAL_PARAMS, **kwargs)
    kwargs['board_id'] = util.IntValue(board_id)
    kwargs['url'] = util.StringValue(url)
    kwargs['event'] = util.EnumValue(event)
    return execute_mutation(api_key, constants.CREATE_WEBHOOK, *args, **kwargs)


def delete_webhook(api_key: str, webhook_id: str, *args, **kwargs):
    kwargs['id'] = util.IntValue(webhook_id)
    return execute_mutation(api_key, constants.DELETE_WEBHOOK, *args, **kwargs)


def create_workspace(api_key: str, name: str, kind: WorkspaceKind, *args, **kwargs):
    args = get_field_list(constants.DEFAULT_WORKSPACE_QUERY_FIELDS, *args)
    kwargs = get_method_arguments(constants.CREATE_WORKSPACE_OPTIONAL_PARAMS, **kwargs)
    kwargs['name'] = util.StringValue(name)
    kwargs['kind'] = util.EnumValue(kind)
    return execute_mutation(api_key, constants.CREATE_WORKSPACE, *args, **kwargs)


def execute_query(api_key:str, query_name: str, *args, **kwargs):
    operation = util.create_query(query_name, *args, **kwargs)
    result = requests.execute_query(api_key, operation=operation)
    return result[query_name]


def execute_mutation(api_key: str, query_name: str, *args, **kwargs):

    if kwargs.__contains__('include_complexity'):
        raise MondayApiError(query_name, 400, '', ['Query complexity cannot be retrieved for mutation requests.'])

    if 'id' not in args:
        args += ('id',)

    operation = util.create_mutation(query_name, *args, **kwargs)
    result = requests.execute_query(api_key, operation=operation)
    return result[query_name]


def get_field_list(fields: list, *args):
    if not args:
        return fields
    return args

def get_method_arguments(mappings: dict, **kwargs):
    result = {}
    for key, value in mappings.items():   
        try:
            if isinstance(value, util.ArgumentValueKind):
                result[key] = util.create_value(kwargs[key], value)
            elif type(value) is tuple:
                data = [util.create_value(item, value[1]).format() for item in kwargs[key]]
                result[key] = util.create_value(data, value[0])
            elif type(value) is dict:
                result[key] = get_method_arguments(value, **(kwargs[key]))
        except KeyError:
            # Ignore if no kwargs found
            continue
    return result