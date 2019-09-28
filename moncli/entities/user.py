from .. import api_v2 as client
from ..enums import NotificationTargetType
from .objects import Notification, Plan

class User():

    def __init__(self, **kwargs):
        self.__creds = kwargs['creds']
          
        self.id = kwargs['id']

        for key, value in kwargs.items():

            if key == 'name':
                self.name = value

            elif key == 'url':
                self.url = value

            elif key == 'email':
                self.email = value

            elif key == 'enabled':
                self.enabled = value

            elif key == 'teams':
                self.__team_ids = [int(team_data['id']) for team_data in value]

            if key == 'birthday':
                self.birthday = value

            elif key == 'country_code':
                self.country_code = value

            elif key == 'created_at': 
                self.create_at = value

            elif key == 'is_guest':
                self.is_guest = value

            elif key == 'is_pending':
                self.is_pending = value

            elif key == 'join_date':
                self.join_date = value

            elif key == 'location':
                self.locaiton = value

            elif key == 'mobile_phone':
                self.mobile_phone = value

            elif key == 'phone':
                self.phone = value

            elif key == 'photo_original':
                self.photo_original = value

            elif key == 'photo_thumb':
                self.photo_thumb = value

            elif key == 'title':
                self.title = value

            elif key == 'utc_hours_diff':
                self.utc_hours_diff = value

        
    def get_account(self):

        users_data = client.get_users(
            self.__creds.api_key_v2, 
            'account.first_day_of_the_week',
            'account.id',
            'account.name',
            'account.show_timeline_weekends',
            'account.slug',
            'account.logo',
            ids=[int(self.id)])

        return Account(
            creds=self.__creds, 
            user_id=self.id,
            **users_data[0]['account'])

    
    def get_teams(self):

        teams_data = client.get_teams(
            self.__creds.api_key_v2,
            'id',
            'name',
            'picture_url',
            'users.id',
            ids=self.__team_ids)

        return [Team(creds=self.__creds, **team_data) for team_data in teams_data]

    
    def send_notification(self, text: str, target_id: str, target_type: NotificationTargetType, *argv, **kwargs):

        notification_data = client.create_notification(
            self.__creds.api_key_v2, 
            text, 
            self.id, 
            target_id, 
            target_type, 
            *argv, 
            **kwargs)

        return Notification(**notification_data)


class Team():

    def __init__(self, **kwargs):
        self.__creds = kwargs['creds']
        
        self.id = kwargs['id']
        self.name = kwargs['name']

        for key, value in kwargs.items():

            if key == 'picture_url':
                self.picture_url = value

            if key == 'users':
                self.__user_ids = [int(user['id']) for user in value]

        
    def get_users(self):

        users_data = client.get_users(
            self.__creds.api_key_v2, 
            'id',
            'name',
            'url',
            'email',
            'enabled',
            'account.id',
            'teams.id',
            ids=self.__user_ids)

        return [User(creds=self.__creds, **user_data) for user_data in users_data]


class Account():

    def __init__(self, **kwargs):
        self.__creds = kwargs['creds']
        self.__user_id = kwargs['user_id']

        self.first_day_of_the_week = kwargs['first_day_of_the_week']
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.show_timeline_weekends = kwargs['show_timeline_weekends']
        self.slug = kwargs['slug']

        for key, value in kwargs.items():

            if key == 'logo':
                self.logo = value


    def get_plan(self):

        plan_data = client.get_users(
            self.__creds.api_key_v2, 
            'account.plan.max_users',
            'account.plan.period',
            'account.plan.tier',
            'account.plan.version',
            ids=[int(self.__user_id)])

        return Plan(**plan_data[0]['account']['plan'])