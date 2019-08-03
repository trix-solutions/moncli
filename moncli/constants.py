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