from .enums import ColumnType

DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

TIMEOUT = 10  # seconds

API_V2_ENDPOINT = 'https://api.monday.com/v2'
API_V2_FILE_ENDPOINT = 'https://api.monday.com/v2/file'
TIMEOUT = 10

# Column Types
COLUMN_NAME = 'name'
COLUMN_MULTIPERSON = 'multi-person'
COLUMN_COLOR = 'color'
COLUMN_DATE = 'date'
COLUMN_NUMERIC = 'numeric'
COLUMN_DURATION = 'duration'
COLUMN_LONGTEXT = 'long-text'