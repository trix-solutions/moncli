from .graphql import ArgumentValueKind

## Operation methods

# Boards
BOARDS = 'boards'
CREATE_BOARD = 'create_board'
ARCHIVE_BOARD = 'archive_board'

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
MOVE_ITEM_TO_GROUP = 'move_item_to_group'
ARCHIVE_ITEM = 'archive_item'
DELETE_ITEM = 'delete_item'

# Updates
UPDATES = 'updates'
CREATE_UPDATE = 'create_update'

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


##

## Optional Parameters

BOARDS_OPTIONAL_PARAMS = {
    'limit': ArgumentValueKind.Int,
    'page': ArgumentValueKind.Int,
    'ids': ArgumentValueKind.List,
    'board_kind': ArgumentValueKind.Enum,
    'state': ArgumentValueKind.Enum,
    'newest_first': ArgumentValueKind.Bool
}

CREATE_BOARD_OPTIONAL_PARAMS = {

}

ARCHIVE_BOARD_OPTIONAL_PARAMS = {

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
    'limit': ArgumentValueKind.Int,
    'page': ArgumentValueKind.Int,
    'ids': ArgumentValueKind.List,
    'newest_first': ArgumentValueKind.Bool
}

ITEMS_BY_COLUMN_VALUES_OPTIONAL_PARAMS = {
    'limit': ArgumentValueKind.Int,
    'page': ArgumentValueKind.Int,
    'column_type': ArgumentValueKind.String,
    'state': ArgumentValueKind.Enum
}

CREATE_ITEM_OPTIONAL_PARAMS ={
    'group_id': ArgumentValueKind.String,
    'column_values': ArgumentValueKind.Json
}

MOVE_ITEM_TO_GROUP_OPTIONAL_PARAMS = {
    
}

ARCHIVE_ITEM_OPTIONAL_PARAMS = {

}

DELETE_ITEM_OPTIONAL_PARAMS = {

}

UPDATES_OPTIONAL_PARAMS = {
    'limit': ArgumentValueKind.Int,
    'page': ArgumentValueKind.Int
}

CREATE_UPDATE_OPTIONAL_PARAMS = {

}

CREATE_NOTIFICATION_OPTIONAL_PARAMS ={
    'payload': ArgumentValueKind.Json
}

TAGS_OPTIONAL_PARAMS = {
    'ids': ArgumentValueKind.List
}

CREATE_OR_GET_TAG_OPTIONAL_PARAMS = {
    'board_id': ArgumentValueKind.Int
}

USERS_OPTIONAL_PARAMS = {
    'ids': ArgumentValueKind.List,
    'kind': ArgumentValueKind.Enum,
    'newest_first': ArgumentValueKind.String,
    'limit': ArgumentValueKind.Int
}

TEAMS_OPTIONAL_PARAMS = {
    'ids': ArgumentValueKind.List
}