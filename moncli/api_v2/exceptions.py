class MondayApiError(Exception):

    def __init__(self, query: str, status_code: int, messages: list):

        self.query = query
        self.status_code = status_code
        self.messages = messages