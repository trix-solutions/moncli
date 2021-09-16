from enum import Enum

class BoardKind(Enum):
    public = 1
    private = 2
    share = 3


class BoardsOrderBy(Enum):
    created_at = 1
    used_at = 2


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
    file = 29
    subitems = 30
    board_relation = 31
    integration = 32
    name = 99999 # This column is a text type but comes standard with every board.
    dependency = 34

class NotificationTargetType(Enum):
    Project = 1
    Post = 2


# Board state enum
class State(Enum):
    all = 1
    active = 2
    archived = 3
    deleted = 4


class UserKind(Enum):
    all = 1
    non_guests = 2
    guests = 3
    non_pending = 4

    
class FirstDayOfTheWeek(Enum):
    sunday = 1
    monday = 2


class PeopleKind(Enum):
    person = 1
    team = 2


class WebhookEventType(Enum):
    create_item = 1
    change_column_value = 2
    change_specific_column_value = 3
    create_update = 4
    incoming_notification = 5
    change_name = 6
    create_subitem = 7
    change_subitem_column_value = 8
    change_subitem_name = 9
    create_subitem_update = 10


class WorkspaceKind(Enum):
    open = 1
    closed = 2


class SubscriberKind(Enum):
    subscriber = 1
    owner = 2


class WorkspaceSubscriberKind(Enum):
    subscriber = 0
    owner = 1