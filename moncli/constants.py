from enum import Enum

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

# Column Types
COLUMN_NAME = 'name'
COLUMN_MULTIPERSON = 'multi-person'
COLUMN_COLOR = 'color'
COLUMN_DATE = 'date'
COLUMN_NUMERIC = 'numeric'
COLUMN_DURATION = 'duration'
COLUMN_LONGTEXT = 'long-text'

# Board kind enum
class BoardKind(Enum):
    public = 1
    private = 2
    shareable = 3

# Column type enum
class ColumnType(Enum):
    auto_number = 1
    checkbox = 2
    country = 3
    color_picker = 4
    creation_log = 5
    date = 6
    dropdown = 7
    email = 8
    hour = 9
    item_id = 10
    last_updated = 11
    link = 12
    location = 13
    long_text = 14
    numbers = 15
    people = 16
    phone = 17
    progress = 18
    rating = 19
    status = 20
    team = 21
    tags = 22
    text = 23
    timeline = 24
    time_tracking = 25
    vote = 26
    week = 27
    world_clock = 28

# Board state enum
class State(Enum):
    all = 1
    active = 2
    archived = 3
    deleted = 4
