from .graphql import ArgumentValueKind

# Boards
BOARDS = 'boards'
CREATE_BOARD = 'create_board'
ARCHIVE_BOARD = 'archive_board'

BOARDS_OPTIONAL_PARAMS = {
    'limit': ArgumentValueKind.Int,
    'page': ArgumentValueKind.Int,
    
}

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