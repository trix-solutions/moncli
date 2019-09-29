from .enums import ColumnType


class ColumnValue():

    def __init__(self, id: str, title: str, column_type: ColumnType):
        self.id = id
        self.title = title
        self.type = column_type

    def format(self):
        pass


class CheckboxValue(ColumnValue):

    def __init__(self, id: str, title: str, column_type: ColumnType, **kwargs):
        super(CheckboxValue, self).__init__(id, title, column_type)
        
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

    def __init__(self, id: str, title: str, column_type: ColumnType, **kwargs):
        super(CountryValue, self).__init__(id, title, column_type)

        self.country_code = None
        self.country_value = None

        for key, value in kwargs.items():

            if key == 'countryCode':
                self.country_code = value

            if key == 'countryName':
                self.country_name = value

    
    def format(self):

        return {
            'countryCode': self.country_code,
            'countryName': self.country_name
        }
        

class EmailValue(ColumnValue):

    def __init__(self, id: str, title: str, column_type: ColumnType, **kwargs):
        super(EmailValue, self).__init__(id, title, column_type)

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

    def __init__(self, id: str, title: str, column_type: ColumnType, **kwargs):
        super(LongTextValue, self).__init__(id, title, column_type)

        for key, value in kwargs.items():

            if key == 'text':
                self.text = value


    def format(self):

        return { 'text': self.text}


class NameValue(ColumnValue):

    def __init__(self, id: str, title: str, column_type: ColumnType, **kwargs):
        super(NameValue, self).__init__(id, title, column_type)

        self.name: str = kwargs['name']

    
    def format(self):

        return self.name
        

class TextValue(ColumnValue):

    def __init__(self, id: str, title: str, column_type: ColumnType, **kwargs):
        super(TextValue, self).__init__(id, title, column_type)

        for key, value in kwargs.items():

            if key == 'text':
                self.text: str = value


    def format(self):
        
        return self.text


def create_column_value(id: str, title: str, column_type: ColumnType, value):

    if column_type == ColumnType.name:
        return NameValue(id, title, column_type, name=value)