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

DEFAULT_ITEM_QUERY_FIELDS = [
    'id',
    'name',
    'created_at',
    'creator_id',
    'state'
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
    'timezone': ColumnType.world_clock
}