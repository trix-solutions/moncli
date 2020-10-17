class MondayApiError(Exception):

    def __init__(self, query: str, status_code: int, error_code: str, messages: list):

        self.query = query
        self.status_code = status_code
        self.error_code = error_code
        self.messages = messages