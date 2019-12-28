from schematics.models import Model
from schematics import types

from .. import api_v2 as client
from .. import config
from ..enums import NotificationTargetType
from .objects import Notification, Plan


class _User(Model):
    id = types.StringType(required=True)
    name = types.StringType()
    created_at = types.StringType()
    url = types.StringType()
    email = types.StringType()
    enabled = types.BooleanType()
    birthday = types.StringType()
    country_code = types.StringType()
    is_guest = types.BooleanType()
    is_pending = types.BooleanType()
    join_date = types.StringType()
    location = types.StringType()
    mobile_phone = types.StringType()
    phone = types.StringType()
    photo_original = types.StringType()
    photo_thumb = types.StringType()
    photo_tiny = types.StringType()
    time_zone_identifier = types.StringType()
    title = types.StringType()
    utc_hours_diff = types.IntType()


class User(_User):
    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        self.__account = None
        self.__teams = None
        super(User, self).__init__(kwargs)

    @property
    def account(self):
        if not self.__account:
            self.__account = self.get_account()
        return self.__account

    @property
    def teams(self):
        if not self.__teams:
            self.__teams = self.get_teams()
        return self.__teams

    def get_account(self):
        field_list = ['account.' + field for field in config.DEFAULT_ACCOUNT_QUERY_FIELDS]
        account_data = client.get_users(
            self.__creds.api_key_v2, 
            *field_list,
            ids=[int(self.id)])[0]['account']

        return Account(
            creds=self.__creds,
            **account_data)
    
    def get_teams(self):
        field_list = ['team.' + field for field in config.DEFAULT_TEAM_QUERY_FIELDS]
        teams_data = client.get_users(
            self.__creds.api_key_v2,
            *field_list,
            ids=[int(self.id)])

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


class _Team(Model):
    id = types.StringType(required=True)
    name = types.StringType()
    picture_url = types.StringType()


class Team(_Team):

    def __init__(self, **kwargs):
        self.__creds = kwargs.pop('creds')
        self.__users = None

    @property
    def users(self):
        if not self.__users:
            self.__users = self.get_users()
        return self.__users

    def get_users(self):
        field_list = ['users.' + field for field in config.DEFAULT_USER_QUERY_FIELDS]
        users_data = client.get_teams(
            self.__creds.api_key_v2, 
            *field_list,
            ids=[int(self.id)])

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