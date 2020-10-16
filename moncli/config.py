from .enums import ColumnType

DEFAULT_BOARD_QUERY_FIELDS = [
    'id', 
    'name', 
    'board_folder_id', 
    'board_kind', 
    'description', 
    'permissions',
    'pos',
    'state']

DEFAULT_COLUMN_QUERY_FIELDS = [
    'id',
    'title',
    'settings_str',
    'archived',
    'type',
    'width'
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

DEFAULT_TAG_QUERY_FIELDS = [
    'id',
    'name',
    'color'
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

DEFAULT_NOTIFICATION_QUERY_FIELDS = [
    'id',
    'text'
]

DEFAULT_WEBHOOK_QUERY_FIELDS = [
    'id',
    'board_id'
]

 
## Column type mappings
COLUMN_TYPE_MAPPINGS = {
    'boolean': ColumnType.checkbox,
    'country': ColumnType.country,
    'date': ColumnType.date,
    'dropdown': ColumnType.dropdown,
    'email': ColumnType.email,
    'hour': ColumnType.hour,
    'link': ColumnType.link,
    'long-text': ColumnType.long_text,
    'name': ColumnType.name,
    'numeric': ColumnType.numbers,
    'multiple-person': ColumnType.people,
    'phone': ColumnType.phone,
    'rating': ColumnType.rating,
    'color': ColumnType.status,
    'tag': ColumnType.tags,
    'team': ColumnType.team,
    'text': ColumnType.text,
    'timerange': ColumnType.timeline,
    'week': ColumnType.week,
    'timezone': ColumnType.world_clock,
    'file': ColumnType.file
}

COLUMN_TYPE_VALUE_MAPPINGS = {
    ColumnType.checkbox: 'CheckboxValue',
    ColumnType.country: 'CountryValue',
    ColumnType.date: 'DateValue',
    ColumnType.dropdown: 'DropdownValue',
    ColumnType.email: 'EmailValue',
    ColumnType.hour: 'HourValue',
    ColumnType.link: 'LinkValue',
    ColumnType.long_text: 'LongTextValue',
    ColumnType.name: 'NameValue',
    ColumnType.numbers: 'NumberValue',
    ColumnType.people: 'PeopleValue',
    ColumnType.phone: 'PhoneValue',
    ColumnType.rating: 'RatingValue',
    ColumnType.status: 'StatusValue',
    ColumnType.tags: 'TagsValue',
    ColumnType.team: 'TeamValue',
    ColumnType.text: 'TextValue',
    ColumnType.timeline: 'TimelineValue',
    ColumnType.world_clock: 'TimezoneValue',
    ColumnType.week: 'WeekValue',
    ColumnType.file: 'FileValue'
}