BASE_URL = 'https://api.monday.com'
PORT = '443'
API_VERSION = 'v1'

# User route signatures
USERS = 'users.json'
USER_BY_ID = 'users/{}.json'
USER_POSTS = 'users/{}/posts.json'
USER_NEWSFEED = 'users/{}/newsfeed.json'
USER_UNREAD_FEED = 'users/{}/unread_feed'

# Updates route signatures
UPDATES = 'updates.json'
UPDATES_BY_ID = 'updates/{}.json'
UPDATE_LIKE = 'updates/{}/like.json'
UPDATE_UNLIKE = 'updates/{}/unlike.json'

# Pulses route signatures
PULSES = 'pulses.json'
PULSE_BY_ID = 'pulses/{}.json'
PULSE_SUBSCRIBERS = 'pulses/{}/subscribers.json'
PULSE_SUBSCRIBERS_BY_USER_ID = 'pulses/{}/subscribers/{}.json'
PULSE_NOTES = 'pulses/{}/notes.json'
PULSE_NOTE_BY_ID = 'pulses/{}/notes/{}.json'
PULSE_UPDATES = 'pulses/{}/updates.json'

# Boards route signatures
BOARDS = 'boards.json'
BOARD_BY_ID = 'boards/{}.json'
BOARD_GROUPS = 'boards/{}/groups.json'
BOARD_MOVE_GROUP = 'boards/{}/groups/{}/move.json'
BOARD_GROUP_BY_ID = 'boards/{}/groups/{}.json'
BOARD_COLUMNS = 'boards/{}/columns.json'
BOARD_COLUMN_BY_ID = 'boards/{}/columns/{}.json'
BOARD_COLUMN_VALUE = 'boards/{}/columns/{}/value.json'
BOARD_TEXT_COLUMN = 'boards/{}/columns/{}/text.json'
BOARD_PERSON_COLUMN = 'boards/{}/columns/{}/person.json'
BOARD_STATUS_COLUMN = 'boards/{}/columns/{}/status.json'
BOARD_DATE_COLUMN = 'boards/{}/columns/{}/date.json'
BOARD_NUMERIC_COLUMN = 'boards/{}/columns/{}/numeric.json'
BOARD_TAGS_COLUMN = 'boards/{}/columns/{}/tags.json'
BOARD_TIMELINE_COLUMN = 'boards/{}/columns/{}/timeline.json'
BOARD_PULSES = 'boards/{}/pulses.json'
BOARD_DUPLICATE_PULSE = 'boards/{}/pulses/{}/duplicate.json'
BOARD_MOVE_PULSES = 'boards/{}/pulses/move.json'
BOARD_SUBSCRIBERS = 'boards/{}/subscribers.json'
BOARD_SUBSCRIBERS_BY_ID = 'boards/{}/subscribers/{}.json'

# Tags route signatures
TAGS_BY_ID = 'tags/{}.json'