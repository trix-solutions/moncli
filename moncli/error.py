class MoncliError(Exception):

    def __init__(self, error_code, entity_id, entity_type, message):
        super().__init__({
            'error_code': error_code,
            'entity_id': entity_id,
            'entity_type': entity_type,
            'message': message
        })


class MondayClientError(MoncliError):
    entity_type = 'MondayClient'

    def __init__(self, error_code, message):
        super().__init__(error_code, None, self.entity_type, message)
        
        
class BoardError(MoncliError):
    entity_type = 'Board'
    def __init__(self, error_code, entity_id, message):
        super().__init__(error_code, entity_id, self.entity_type, message)
        
        
class GroupError(MoncliError):
    entity_type = 'Group'
    def __init__(self, error_code, entity_id, message):
        super().__init__(error_code, entity_id, self.entity_type, message)


class ItemError(MoncliError):
    entity_type = 'Item'
    def __init__(self, error_code, entity_id, message):
        super().__init__(error_code, entity_id, self.entity_type, message)


class ColumnValueError(MoncliError):
    entity_type = 'ColumnValue'

    def __init__(self, error_code, entity_id, message):
        super().__init__(error_code, entity_id, self.entity_type, message)