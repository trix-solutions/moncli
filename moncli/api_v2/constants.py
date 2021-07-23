from .graphql import ArgumentValueKind

## Operation methods

# Boards
BOARDS = 'boards'
CREATE_BOARD = 'create_board'
ARCHIVE_BOARD = 'archive_board'
ADD_SUBSCRIBERS_TO_BOARD = 'add_subscribers_to_board'
DELETE_SUBSCRIBERS_FROM_BOARD = 'delete_subscribers_from_board'

# Columns
CREATE_COLUMN = 'create_column'
CHANGE_COLUMN_VALUE = 'change_column_value'
CHANGE_MULTIPLE_COLUMN_VALUES = 'change_multiple_column_values'

# Groups
DUPLICATE_GROUP = 'duplicate_group'
CREATE_GROUP = 'create_group'
ARCHIVE_GROUP = 'archive_group'
DELETE_GROUP = 'delete_group'

# Items
ITEMS = 'items'
ITEMS_BY_COLUMN_VALUES = 'items_by_column_values'
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

# Me
ME = 'me'

# Account
ACCOUNT = 'account'

# Webhooks
CREATE_WEBHOOK = 'create_webhook'
DELETE_WEBHOOK = 'delete_webhook'

# Workspace
CREATE_WORKSPACE = 'create_workspace'

# Files
ASSETS = 'assets'
ADD_FILE_TO_UPDATE = 'add_file_to_update'
ADD_FILE_TO_COLUMN = 'add_file_to_column'


##


## Default Fields


DEFAULT_BOARD_QUERY_FIELDS = [
    'id', 
    'name', 
    'board_folder_id', 
    'board_kind', 
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
    'url'
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
    'is_guest',
    'is_pending',
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


##

## Optional Parameters

BOARDS_OPTIONAL_PARAMS = {
    'limit': ArgumentValueKind.Int,
    'page': ArgumentValueKind.Int,
    'ids': (ArgumentValueKind.List, ArgumentValueKind.Int),
    'board_kind': ArgumentValueKind.Enum,
    'state': ArgumentValueKind.Enum,
    'newest_first': ArgumentValueKind.Bool,
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
    'updates': {
        'limit': ArgumentValueKind.Int,
        'page': ArgumentValueKind.Int
    },
    'views': {
        'ids': (ArgumentValueKind.List, ArgumentValueKind.Int),
        'type': ArgumentValueKind.String
    }
}

CREATE_BOARD_OPTIONAL_PARAMS = {
    'workspace_id': ArgumentValueKind.Int,
    'template_id': ArgumentValueKind.Int
}

ARCHIVE_BOARD_OPTIONAL_PARAMS = {

}

ADD_SUBSCRIBERS_TO_BOARD_OPTIONAL_PARAMS = {
    'kind': ArgumentValueKind.Enum
}

DELETE_SUBSCRIBERS_FROM_BOARD_OPTIONAL_PARAMS = {
    
}

CREATE_COLUMN_OPTIONAL_PARAMS = {

}

CHANGE_COLUMN_VALUE_OPTIONAL_PARAMS = {

}

CHANGE_MULTIPLE_COLUMN_VALUES_OPTIONAL_PARAMS = {

}

DUPLICATE_GROUP_OPTIONAL_PARAMS = {
    'add_to_top': ArgumentValueKind.Bool,
    'group_title': ArgumentValueKind.String
}

CREATE_GROUP_OPTIONAL_PARAMS = {

}

ARCHIVE_GROUP_OPTIONAL_PARAMS = {

}

DELETE_GROUP_OPTIONAL_PARAMS = {

}

ITEMS_OPTIONAL_PARAMS = {
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
}

ITEMS_BY_COLUMN_VALUES_OPTIONAL_PARAMS = {
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
}

CREATE_ITEM_OPTIONAL_PARAMS = {
    'group_id': ArgumentValueKind.String,
    'column_values': ArgumentValueKind.Json
}

CREATE_SUBITEM_OPTIONAL_PARAMS = {
    'column_values': ArgumentValueKind.Json
}

MOVE_ITEM_TO_GROUP_OPTIONAL_PARAMS = {
    
}

ARCHIVE_ITEM_OPTIONAL_PARAMS = {

}

DELETE_ITEM_OPTIONAL_PARAMS = {

}

DUPLICATE_ITEM_ARGUMENTS = {
    'board_id': ArgumentValueKind.Int,
    'with_updates': ArgumentValueKind.Bool,
    'item_id': ArgumentValueKind.Int
}

UPDATES_OPTIONAL_PARAMS = {
    'limit': ArgumentValueKind.Int,
    'page': ArgumentValueKind.Int
}

CREATE_UPDATE_OPTIONAL_PARAMS = {
    'parent_id': ArgumentValueKind.Int
}

CREATE_NOTIFICATION_OPTIONAL_PARAMS ={
    'payload': ArgumentValueKind.Json
}

TAGS_OPTIONAL_PARAMS = {
    'ids': (ArgumentValueKind.List, ArgumentValueKind.Int)
}

CREATE_OR_GET_TAG_OPTIONAL_PARAMS = {
    'board_id': ArgumentValueKind.Int
}

USERS_OPTIONAL_PARAMS = {
    'ids': (ArgumentValueKind.List, ArgumentValueKind.Int),
    'kind': ArgumentValueKind.Enum,
    'newest_first': ArgumentValueKind.String,
    'limit': ArgumentValueKind.Int
}

TEAMS_OPTIONAL_PARAMS = {
    'ids': (ArgumentValueKind.List, ArgumentValueKind.Int)
}

CREATE_WEBHOOK_OPTIONAL_PARAMS = {
    'config': ArgumentValueKind.Json
}

CREATE_WORKSPACE_OPTIONAL_PARAMS = {
    'description': ArgumentValueKind.String
}

ASSETS_OPTIONAL_PARAMS = {
    
}