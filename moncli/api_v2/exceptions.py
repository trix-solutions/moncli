class MondayApiError(Exception):
    """monday.com API exception

    __________
    Properties
    __________
    query : `str`
        The submitted query resulting in error.
    status_code : `int`
        The http status code of the response.
    error_code : `str`
        The monday.com API error code.
    messages : `list[str]`
        The list of error messages.
    """

    def __init__(self, query: str, status_code: int, error_code: str, messages: list):

        self.query = query
        self.status_code = status_code
        self.error_code = error_code
        self.messages = messages