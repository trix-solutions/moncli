class AuthorizationError(Exception):

    def __init__(self, user_name: str):

        self.message = 'User {} was not recognized by the applied token'.format(user_name)


class BoardNotFound(Exception):

    def __init__(self, search_type, value):
        
        if search_type == 'id':
            self.message = 'Unable to find board with name: "{}".'.format(value)
        
        elif search_type == 'name':
            self.message = 'Unable to find board with the ID: "{}".'.format(value)

        else:
            self.message = 'Unable to find the requested board.'


class TooManyGetBoardParameters(Exception):

    def __init__(self):
        self.message = "Unable to use both 'id' and 'name' when querying for a board."
        

class NotEnoughGetBoardParameters(Exception):

    def __init__(self):
        self.message = "Either the 'id' or 'name' is required when querying a board."


class TooManyGetGroupParameters(Exception):

    def __init__(self):
        self.message = "Unable to use both 'id' and 'title' when querying for a group."
        

class NotEnoughGetGroupParameters(Exception):

    def __init__(self):
        self.message = "Either the 'id' or 'title' is required when querying a group."


class TooManyGetColumnValueParameters(Exception):

    def __init__(self):
        self.message = "Unable to use both 'id' and 'title' when querying for a column value."
        

class NotEnoughGetColumnValueParameters(Exception):

    def __init__(self):
        self.message = "Either the 'id' or 'title' is required when querying a column value."


class ColumnValueRequired(Exception):

    def __init__(self):
        self.message = "A column value is required if no 'column_id' value is present."


class InvalidColumnValue(Exception):

    def __init__(self, column_value_type: str):
        self.message = "Unable to use column value of type '{}' with the given set of input parameters".format(column_value_type)