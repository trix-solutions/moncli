class MoncliError(Exception):

    def __init__(self, error_code, entity_id, entity_type, message):
        super().__init__({
            'error_code': error_code,
            'entity_id': entity_id,
            'entity_type': entity_type,
            'message': message
        })

class ColumnValueError(MoncliError):
    entity_type = 'ColumnValue'

    def __init__(self, error_code, entity_id, message):
        super().__init__(error_code, entity_id, self.entity_type, message)