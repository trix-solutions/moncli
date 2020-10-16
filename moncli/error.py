class MoncliError(Exception):

    def __init__(self, status_code: int, messages: list):

        self.status_code = status_code
        self.messages = messages