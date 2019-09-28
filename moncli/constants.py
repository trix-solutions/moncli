DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

API_V2_ENDPOINT = 'https://api.monday.com/v2'

# Column Types
COLUMN_NAME = 'name'
COLUMN_MULTIPERSON = 'multi-person'
COLUMN_COLOR = 'color'
COLUMN_DATE = 'date'
COLUMN_NUMERIC = 'numeric'
COLUMN_DURATION = 'duration'
COLUMN_LONGTEXT = 'long-text'

## Column type mappings
COLUMN_TYPE_MAPPINGS = {
    'boolean': 'checkbox',
    'country': 'country',
    'date': 'date',
    'dropdown': 'dropdown',
    'email': 'email',
    'hour': 'hour',
    'link': 'link',
    'long-text': 'long_text',
    'name': 'name',
    'numeric': 'numbers',
    'multiple-person': 'people',
    'phone': 'phone',
    'rating': 'rating',
    'color': 'status',
    'tag': 'tags',
    'team': 'team',
    'text': 'text',
    'timerange': 'timeline',
    'week': 'week',
    'timezone': 'world_clock'
}