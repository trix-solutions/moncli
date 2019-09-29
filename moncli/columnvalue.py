from .enums import ColumnType


class ColumnValue():

    def __init__(self, id: str, title: str):
        self.id = id
        self.title = title

    def format(self):
        pass


class CheckboxValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(CheckboxValue, self).__init__(id, title)
        
        self.checked: bool = False

        value: str = kwargs['checked']
        if value == 'true':
            self.checked = True

    
    def format(self):

        value: str = 'false'

        if hasattr(self, 'checked') and self.checked:
            value = 'true'

        return { "checked": value }


class CountryValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(CountryValue, self).__init__(id, title)

        self.country_code = None
        self.country_value = None

        for key, value in kwargs.items():

            if key == 'country_code':
                self.country_code = value

            if key == 'country_name':
                self.country_name = value

    
    def format(self):

        return {
            'countryCode': self.country_code,
            'countryName': self.country_name
        }
        

class DropdownValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(DropdownValue, self).__init__(id, title)

        self.label_id: int = None
        self.label: str = None

        for key, value in kwargs.items():

            if key == 'label_id':
                self.label_id = value

            if key == 'label':
                self.label = value


    def format(self):

        if self.label is not None:
            return { 'label': self.label }

        if self.label_id is not None:
            return { 'id': self.label_id}


class EmailValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(EmailValue, self).__init__(id, title)

        self.email = None
        self.text = None

        for key, value in kwargs.items():

            if key == 'email':
                self.email = value

            elif key == 'text':
                self.text = value

    
    def format(self):

        return {
            'email': self.email,
            'text': self.text
        }


class LongTextValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(LongTextValue, self).__init__(id, title)

        for key, value in kwargs.items():

            if key == 'text':
                self.text = value


    def format(self):

        return { 'text': self.text}


class NameValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(NameValue, self).__init__(id, title)

        self.name: str = kwargs['name']

    
    def format(self):

        return self.name
        

class NumberValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(NumberValue, self).__init__(id, title)

        self.number = None

        for key, value in kwargs.items():

            if key == 'number':
                if self.__isint(value):
                    self.number = int(value)

                elif self.__isfloat(value):
                    self.number = float(value)


    def format(self):

        if self.number is not None:
            return str(self.number)

        return self.number


    def __isfloat(self, value):

        try:
            float(value)

        except ValueError:
            return False

        return True

    
    def __isint(self, value):

        try:
            a = float(value)
            b = int(a)

        except ValueError:
            return False

        return a == b


class PeopleValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(PeopleValue, self).__init__(id, title)

        self.persons_and_teams = None

        for key, value in kwargs.items():

            if key == 'persons_and_teams':
                self.persons_and_teams = value

    
    def format(self):

        if self.persons_and_teams is None:
            return self.persons_and_teams

        return { 'personsAndTeams': self.persons_and_teams }


class PhoneValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(PhoneValue, self).__init__(id, title)

        self.phone = None
        self.country_short_name = None

        if kwargs.__contains__('phone') or kwargs.__contains__('country_short_name'):
            self.phone = kwargs['phone']
            self.country_short_name = kwargs['country_short_name']

    
    def format(self):

        if self.phone is None or self.country_short_name is None:
            return None

        return { 'phone': self.phone, 'countryShortName': self.country_short_name }


class StatusValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(StatusValue, self).__init__(id, title)

        self.index = None
        self.label = None

        for key, value in kwargs.items():

            if key == 'index':
                self.index: int = value

            if key == 'label':
                self.label: str = value


    def format(self):

        if self.label is not None:
            return { 'label': self.label }

        if self.index is not None:
            return { 'index': self.index }


class TeamValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(TeamValue, self).__init__(id, title)

        self.team_id = None

        for key, value in kwargs.items():

            if key == 'team_id':
                self.team_id: int = value


    def format(self):

        if self.team_id is not None:
            return { 'team_id': self.team_id }

        return self.team_id


class TextValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(TextValue, self).__init__(id, title)

        for key, value in kwargs.items():

            if key == 'text':
                self.text: str = value


    def format(self):
        
        return self.text


class TimezoneValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(TimezoneValue, self).__init__(id, title)

        self.timezone = None

        for key, value in kwargs.items():

            if key == 'timezone':
                self.timezone = value


    def format(self):

        if self.timezone is not None:
            return { 'timezone': self.timezone }

        return self.timezone


def create_column_value(id: str, column_type: ColumnType, title: str = None, value = None):

    if column_type == ColumnType.checkbox:

        if value is None:
            return CheckboxValue(id, title)

        return CheckboxValue(id, title, **value)


    elif column_type == ColumnType.country:

        if value is None:
            return CountryValue(id, title)

        return CountryValue(id, title, country_code=value['countryCode'], country_name=value['countryName'])


    elif column_type == ColumnType.dropdown:

        if value is None: 
            return DropdownValue(id, title)

        if value.__contains__('label'):
            return DropdownValue(id, title, label=value['label'])

        if value.__contains__('id'):
            return DropdownValue(id, title, label_id=value['id'])


    elif column_type == ColumnType.email:

        if value is None:
            return EmailValue(id, title)

        return EmailValue(id, title, **value)


    elif column_type == ColumnType.long_text:

        if value is None:
            return LongTextValue(id, title)

        return LongTextValue(id, title, **value)


    elif column_type == ColumnType.name:
        return NameValue(id, title, name=value)


    elif column_type == ColumnType.numbers:

        if value is None:
            return NumberValue(id, title)

        return NumberValue(id, title, number=value)


    elif column_type == ColumnType.people:

        if value is None:
            return PeopleValue(id, title)

        return PeopleValue(id, title, persons_and_teams=value['personsAndTeams'])


    elif column_type == ColumnType.phone:

        if value is None:
            return PhoneValue(id, title)

        return PhoneValue(id, title, phone=value['phone'], country_short_name=value['countryShortName'])
    
    
    elif column_type == ColumnType.status:

        if value is None:
            return StatusValue(id, title)

        if value.__contains__('label'):
            return StatusValue(id, title, label=value['label'])

        if value.__contains__('index'):
            return StatusValue(id, title, index=value['index'])


    elif column_type == ColumnType.team:

        if value is None:
            return TeamValue(id, title)

        return TeamValue(id, title, **value)


    elif column_type == ColumnType.text:

        if value is None:
            return TextValue(id, title)

        return TextValue(id, title, text=value)


    elif column_type == ColumnType.world_clock:

        if value is None:
            return TimezoneValue(id, title)

        return TimezoneValue(id, title, **value)