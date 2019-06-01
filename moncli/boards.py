from datetime import datetime

from moncli.routes import boards 
from .constants import DATE_FORMAT

class Board():

    def __init__(self, resp):

        self.id = resp['id']
        self.name = resp['name']
        self.description = resp['description']
        self.board_kind = resp['board_kind']
        self.created_at = datetime.strptime(resp['created_at'], DATE_FORMAT)
        self.updated_at = datetime.strptime(resp['updated_at'], DATE_FORMAT)
        self.columns = resp['columns']
        self.groups = resp['groups']

    