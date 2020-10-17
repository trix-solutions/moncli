from .enums import ColumnType


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