from datetime import datetime

from .constants import DATETIME_FORMAT

class User():

    def __init__(self, resp):

        self.id = resp['id']
        self.name = resp['name']
        self.username = resp['email']
        self.title = resp['title']
        self.position = resp['position']
        self.phone = resp['phone']
        self.location = resp['location']
        self.status = resp['status']
        self.birthday = resp['birthday']
        self.is_guest = resp['is_guest']
        self.created_at = datetime.strptime(resp['created_at'], DATETIME_FORMAT)
        self.updated_at = datetime.strptime(resp['updated_at'], DATETIME_FORMAT)