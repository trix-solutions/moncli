from .. import ColumnType


SIMPLE_NULL_VALUE = ''
COMPLEX_NULL_VALUE = {}

COLUMN_TYPE_VALUE_MAPPINGS = {
    ColumnType.checkbox: 'CheckboxValue',
    ColumnType.country: 'CountryValue',
    ColumnType.creation_log: 'CreationLogValue',
    ColumnType.date: 'DateValue',
    ColumnType.dependency: 'DependencyValue',
    ColumnType.dropdown: 'DropdownValue',
    ColumnType.email: 'EmailValue',
    ColumnType.hour: 'HourValue',
    ColumnType.link: 'LinkValue',
    ColumnType.last_updated: 'LastUpdatedValue',
    ColumnType.long_text: 'LongTextValue',
    ColumnType.location: 'LocationValue',
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
    ColumnType.file: 'FileValue',
    ColumnType.board_relation : 'ItemLinkValue',
    ColumnType.subitems : 'SubitemsValue'
}