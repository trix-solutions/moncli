from .graphql import ArgumentValueKind

## API Configurations
API_V2_ENDPOINT = 'https://api.monday.com/v2'
API_V2_FILE_ENDPOINT = 'https://api.monday.com/v2/file'

## Operation methods
# Boards
BOARDS = 'boards'
CREATE_BOARD = 'create_board'
ARCHIVE_BOARD = 'archive_board'
ADD_SUBSCRIBERS_TO_BOARD = 'add_subscribers_to_board'
DELETE_SUBSCRIBERS_FROM_BOARD = 'delete_subscribers_from_board'
# Columns
CREATE_COLUMN = 'create_column'
CHANGE_COLUMN_TITLE = 'change_column_title'
CHANGE_COLUMN_VALUE = 'change_column_value'
CHANGE_SIMPLE_COLUMN_VALUE = 'change_simple_column_value'
CHANGE_MULTIPLE_COLUMN_VALUES = 'change_multiple_column_values'
# Groups
DUPLICATE_GROUP = 'duplicate_group'
CREATE_GROUP = 'create_group'
ARCHIVE_GROUP = 'archive_group'
DELETE_GROUP = 'delete_group'
# Items
ITEMS = 'items'
ITEMS_BY_COLUMN_VALUES = 'items_by_column_values'
ITEMS_BY_MULTIPLE_COLUMN_VALUES = 'items_by_multiple_column_values'
CREATE_ITEM = 'create_item'
CREATE_SUBITEM = 'create_subitem'
CLEAR_ITEM_UPDATES = 'clear_item_updates'
MOVE_ITEM_TO_GROUP = 'move_item_to_group'
ARCHIVE_ITEM = 'archive_item'
DELETE_ITEM = 'delete_item'
DUPLICATE_ITEM = 'duplicate_item'
# Updates
UPDATES = 'updates'
CREATE_UPDATE = 'create_update'
DELETE_UPDATE = 'delete_update'
# Notifications
CREATE_NOTIFICATION = 'create_notification'
# Tags
TAGS = 'tags'
CREATE_OR_GET_TAG = 'create_or_get_tag'
# Users 
USERS = 'users'
# Teams
TEAMS = 'teams'
ADD_TEAMS_TO_WORKSPACE = 'add_teams_to_workspace'
DELETE_TEAMS_FROM_WORKSPACE = 'delete_teams_from_workspace'
# Me
ME = 'me'
# Account
ACCOUNT = 'account'
# Webhooks
CREATE_WEBHOOK = 'create_webhook'
DELETE_WEBHOOK = 'delete_webhook'
# Workspace
CREATE_WORKSPACE = 'create_workspace'
ADD_USERS_TO_WORKSPACE = 'add_users_to_workspace'
DELETE_USERS_FROM_WORKSPACE = 'delete_users_from_workspace'

# Files
ASSETS = 'assets'
ADD_FILE_TO_UPDATE = 'add_file_to_update'
ADD_FILE_TO_COLUMN = 'add_file_to_column'


## Default Fields
DEFAULT_BOARD_QUERY_FIELDS = [
    'id', 
    'name', 
    'board_folder_id', 
    'board_kind',
    'communication', 
    'description', 
    'permissions',
    'pos',
    'state',
    'workspace_id',
    'updated_at'
]

DEFAULT_ACTIVITY_LOG_QUERY_FIELDS = [
    'account_id',
    'created_at',
    'data',
    'entity',
    'event',
    'id',
    'user_id'
]

DEFAULT_BOARD_VIEW_QUERY_FIELDS = [
    'id',
    'name',
    'settings_str',
    'type'
]

DEFAULT_COLUMN_QUERY_FIELDS = [
    'id',
    'title',
    'settings_str',
    'archived',
    'type',
    'width'
]

DEFAULT_ITEM_QUERY_FIELDS = [
    'id',
    'name',
    'created_at',
    'creator_id',
    'state'
]

DEFAULT_GROUP_QUERY_FIELDS = [
    'id', 
    'title', 
    'archived', 
    'color', 
    'deleted', 
    'position'
]

DEFAULT_COLUMN_VALUE_QUERY_FIELDS = [
    'id',
    'title',
    'text',
    'value',
    'additional_info'
]

DEFAULT_TAG_QUERY_FIELDS = [
    'id',
    'name',
    'color'
]

DEFAULT_NOTIFICATION_QUERY_FIELDS = [
    'id',
    'text'
]

DEFAULT_UPDATE_QUERY_FIELDS = [
    'id',
    'body',
    'created_at',
    'creator_id',
    'item_id',
    'text_body',
    'updated_at'
]

DEFAULT_REPLY_QUERY_FIELDS = [
    'id',
    'body',
    'created_at',
    'creator_id',
    'text_body',
    'updated_at'
]

DEFAULT_ASSET_QUERY_FIELDS = [
    'id',
    'name',
    'url',
    'file_size',
    'file_extension'
]

DEFAULT_WEBHOOK_QUERY_FIELDS = [
    'id',
    'board_id'
]

DEFAULT_WORKSPACE_QUERY_FIELDS = [
    'id',
    'name',
    'kind',
    'description'
]

DEFAULT_USER_QUERY_FIELDS = [
    'id',
    'name',
    'url',
    'email',
    'enabled',
    'birthday',
    'country_code',
    'is_admin',
    'is_guest',
    'is_pending',
    'is_verified',
    'is_view_only',
    'join_date',
    'location',
    'mobile_phone',
    'phone',
    'photo_original',
    'photo_thumb',
    'photo_tiny',
    'time_zone_identifier',
    'title',
    'utc_hours_diff'
]

DEFAULT_TEAM_QUERY_FIELDS = [
    'id',
    'name',
    'picture_url'
]

DEFAULT_ACCOUNT_QUERY_FIELDS = [
    'id',
    'name',
    'first_day_of_the_week',
    'logo',
    'show_timeline_weekends',
    'slug'
]

DEFAULT_PLAN_QUERY_FIELDS = [
    'max_users',
    'period',
    'tier',
    'version'
]


FIELD_MAP = {
    'account': DEFAULT_ACCOUNT_QUERY_FIELDS,
    'activity_logs': DEFAULT_ACTIVITY_LOG_QUERY_FIELDS,
    'assets': DEFAULT_ASSET_QUERY_FIELDS,
    'board': DEFAULT_BOARD_QUERY_FIELDS,
    'columns': DEFAULT_COLUMN_QUERY_FIELDS,
    'column_values': DEFAULT_COLUMN_VALUE_QUERY_FIELDS,
    'creator': DEFAULT_USER_QUERY_FIELDS,
    'group': DEFAULT_GROUP_QUERY_FIELDS,
    'groups': DEFAULT_GROUP_QUERY_FIELDS,
    'items': DEFAULT_ITEM_QUERY_FIELDS,
    'owner': DEFAULT_USER_QUERY_FIELDS,
    'replies': DEFAULT_REPLY_QUERY_FIELDS,
    'subscribers': DEFAULT_USER_QUERY_FIELDS,
    'tags': DEFAULT_TAG_QUERY_FIELDS,
    'teams': DEFAULT_TEAM_QUERY_FIELDS,
    'top_group': DEFAULT_GROUP_QUERY_FIELDS,
    'updates': DEFAULT_UPDATE_QUERY_FIELDS,
    'uploaded_by': DEFAULT_USER_QUERY_FIELDS,
    'users': DEFAULT_USER_QUERY_FIELDS,
    'views': DEFAULT_BOARD_VIEW_QUERY_FIELDS,
    'workspace': DEFAULT_WORKSPACE_QUERY_FIELDS,
}

## Field list and default arguments map
QUERY_MAP = {
    BOARDS: (
        DEFAULT_BOARD_QUERY_FIELDS, 
        {
            'limit': ArgumentValueKind.Int,
            'page': ArgumentValueKind.Int,
            'ids': (ArgumentValueKind.List, ArgumentValueKind.Int),
            'board_kind': ArgumentValueKind.Enum,
            'state': ArgumentValueKind.Enum,
            'activity_logs': {
                'limit': ArgumentValueKind.Int,
                'page': ArgumentValueKind.Int,
                'user_ids': (ArgumentValueKind.List, ArgumentValueKind.Int),
                'column_ids': (ArgumentValueKind.List, ArgumentValueKind.String),
                'group_ids': (ArgumentValueKind.List, ArgumentValueKind.String),
                'item_ids': (ArgumentValueKind.List, ArgumentValueKind.Int),
                'from': ArgumentValueKind.String,
                'to': ArgumentValueKind.String
            },
            'columns': {
                'ids': (ArgumentValueKind.List, ArgumentValueKind.String)
            },
            'groups': {
                'ids': (ArgumentValueKind.List, ArgumentValueKind.String),
                'items': {
                    'ids': (ArgumentValueKind.List, ArgumentValueKind.Int),
                    'limit': ArgumentValueKind.Int,
                    'page': ArgumentValueKind.Int
                }
            },
            'items': {
                'ids': (ArgumentValueKind.List, ArgumentValueKind.Int),
                'limit': ArgumentValueKind.Int,
                'page': ArgumentValueKind.Int
            },
            'order_by': ArgumentValueKind.Enum,
            'updates': {
                'limit': ArgumentValueKind.Int,
                'page': ArgumentValueKind.Int
            },
            'views': {
                'ids': (ArgumentValueKind.List, ArgumentValueKind.Int),
                'type': ArgumentValueKind.String
            }
        }),
    ADD_USERS_TO_WORKSPACE: (DEFAULT_USER_QUERY_FIELDS, {
        
    }),
    CREATE_BOARD: (
        DEFAULT_BOARD_QUERY_FIELDS, 
        {
            'workspace_id': ArgumentValueKind.Int,
            'template_id': ArgumentValueKind.Int
        }),
    ARCHIVE_BOARD: (DEFAULT_BOARD_QUERY_FIELDS, {}),
    ADD_SUBSCRIBERS_TO_BOARD: (
        DEFAULT_USER_QUERY_FIELDS, 
        {
            'kind': ArgumentValueKind.Enum
        }),
    DELETE_SUBSCRIBERS_FROM_BOARD: (DEFAULT_USER_QUERY_FIELDS, {}),
    CREATE_COLUMN: (
        DEFAULT_COLUMN_QUERY_FIELDS, 
        {
            'defaults': ArgumentValueKind.Json
        }),
    CHANGE_COLUMN_TITLE: (DEFAULT_COLUMN_QUERY_FIELDS, {}),
    CHANGE_COLUMN_VALUE: (DEFAULT_ITEM_QUERY_FIELDS, {}),
    CHANGE_SIMPLE_COLUMN_VALUE: (DEFAULT_ITEM_QUERY_FIELDS, {}),
    CHANGE_MULTIPLE_COLUMN_VALUES: (DEFAULT_ITEM_QUERY_FIELDS, {}),
    DUPLICATE_GROUP: (
        DEFAULT_GROUP_QUERY_FIELDS, 
        {
            'add_to_top': ArgumentValueKind.Bool,
            'group_title': ArgumentValueKind.String
        }),
    CREATE_GROUP: (DEFAULT_GROUP_QUERY_FIELDS, {}),
    ARCHIVE_GROUP: (DEFAULT_GROUP_QUERY_FIELDS, {}),
    DELETE_GROUP: (DEFAULT_GROUP_QUERY_FIELDS, {}),
    ITEMS: (
        DEFAULT_ITEM_QUERY_FIELDS, 
        {
            'assets': {
                'column_ids': (ArgumentValueKind.List, ArgumentValueKind.String)
            },
            'limit': ArgumentValueKind.Int,
            'page': ArgumentValueKind.Int,
            'ids': (ArgumentValueKind.List, ArgumentValueKind.Int),
            'newest_first': ArgumentValueKind.Bool,
            'column_values': {
                'ids': (ArgumentValueKind.List, ArgumentValueKind.Default),
            },
            'updates': {
                'limit': ArgumentValueKind.Int,
                'page': ArgumentValueKind.Int
            }
        }),
    ITEMS_BY_COLUMN_VALUES: (
        DEFAULT_ITEM_QUERY_FIELDS, 
        {
            'limit': ArgumentValueKind.Int,
            'page': ArgumentValueKind.Int,
            'column_type': ArgumentValueKind.String,
            'state': ArgumentValueKind.Enum,
            'column_values': {
                'ids': (ArgumentValueKind.List, ArgumentValueKind.Default),
            },
            'updates': {
                'limit': ArgumentValueKind.Int,
                'page': ArgumentValueKind.Int
            }
        }),
    ITEMS_BY_MULTIPLE_COLUMN_VALUES: (
        DEFAULT_ITEM_QUERY_FIELDS, 
        {
            'limit': ArgumentValueKind.Int,
            'page': ArgumentValueKind.Int,
            'column_type': ArgumentValueKind.String,
            'state': ArgumentValueKind.Enum
        }),
    CREATE_ITEM: (
        DEFAULT_ITEM_QUERY_FIELDS, 
        {
            'group_id': ArgumentValueKind.String,
            'column_values': ArgumentValueKind.Json
        }),
    CREATE_SUBITEM: (
        DEFAULT_ITEM_QUERY_FIELDS,
        {
            'column_values': ArgumentValueKind.Json
        }),
    CLEAR_ITEM_UPDATES: (DEFAULT_ITEM_QUERY_FIELDS, {}),
    MOVE_ITEM_TO_GROUP: (DEFAULT_ITEM_QUERY_FIELDS, {}),
    ARCHIVE_ITEM: (DEFAULT_ITEM_QUERY_FIELDS, {}),
    DELETE_ITEM: (DEFAULT_ITEM_QUERY_FIELDS, {}),
    DUPLICATE_ITEM: (
        DEFAULT_ITEM_QUERY_FIELDS, 
        {
            'board_id': ArgumentValueKind.Int,
            'with_updates': ArgumentValueKind.Bool,
            'item_id': ArgumentValueKind.Int
        }),
    UPDATES: (
        DEFAULT_UPDATE_QUERY_FIELDS, 
        {
            'limit': ArgumentValueKind.Int,
            'page': ArgumentValueKind.Int
        }),
    CREATE_UPDATE: (
        DEFAULT_UPDATE_QUERY_FIELDS, 
        {
            'parent_id': ArgumentValueKind.Int
        }),
    DELETE_UPDATE: (DEFAULT_UPDATE_QUERY_FIELDS, {}),
    CREATE_NOTIFICATION: (
        DEFAULT_NOTIFICATION_QUERY_FIELDS, 
        {
            'payload': ArgumentValueKind.Json
        }),
    TAGS: (
        DEFAULT_TAG_QUERY_FIELDS, 
        {
            'ids': (ArgumentValueKind.List, ArgumentValueKind.Int)
        }),
    CREATE_OR_GET_TAG: (
        DEFAULT_TAG_QUERY_FIELDS, 
        {
            'board_id': ArgumentValueKind.Int
        }),
    USERS: (
        DEFAULT_USER_QUERY_FIELDS,
        {
            'ids': (ArgumentValueKind.List, ArgumentValueKind.Int),
            'kind': ArgumentValueKind.Enum,
            'newest_first': ArgumentValueKind.String,
            'limit': ArgumentValueKind.Int
        }),
    TEAMS: (
        DEFAULT_TEAM_QUERY_FIELDS,
        {
            'ids': (ArgumentValueKind.List, ArgumentValueKind.Int)
        }),
    ADD_TEAMS_TO_WORKSPACE: (
        DEFAULT_TEAM_QUERY_FIELDS ,
         {

         }),
    DELETE_TEAMS_FROM_WORKSPACE: 
    (
        DEFAULT_TEAM_QUERY_FIELDS , 
        {
            
        }),
    ME: (DEFAULT_USER_QUERY_FIELDS, {}),
    ACCOUNT: (DEFAULT_ACCOUNT_QUERY_FIELDS, {}),
    CREATE_WEBHOOK: (
        DEFAULT_WEBHOOK_QUERY_FIELDS, 
        {
            'config': ArgumentValueKind.Json
        }),
    DELETE_WEBHOOK: (DEFAULT_WEBHOOK_QUERY_FIELDS, ),
    CREATE_WORKSPACE: (
        DEFAULT_WORKSPACE_QUERY_FIELDS, 
        {
            'description': ArgumentValueKind.String
        }),
    DELETE_USERS_FROM_WORKSPACE: (
        DEFAULT_USER_QUERY_FIELDS,
         {

         }),
    ASSETS: (DEFAULT_ASSET_QUERY_FIELDS, {}),
    ADD_FILE_TO_UPDATE: (DEFAULT_ASSET_QUERY_FIELDS, {}),
    ADD_FILE_TO_COLUMN: (DEFAULT_ASSET_QUERY_FIELDS, {})
}