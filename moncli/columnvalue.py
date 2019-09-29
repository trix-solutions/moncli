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

            
class TextValue(ColumnValue):

    def __init__(self, id: str, title: str, **kwargs):
        super(TextValue, self).__init__(id, title)

        for key, value in kwargs.items():

            if key == 'text':
                self.text: str = value


    def format(self):
        
        return self.text


def create_column_value(id: str, title: str, column_type: ColumnType, value = None):

    if column_type == ColumnType.checkbox:

        if value is None:
            return CheckboxValue(id, title)

        return CheckboxValue(id, title, checked=value['checked'])


    elif column_type == ColumnType.country:

        if value is None:
            return CountryValue(id, title)

        return CountryValue(id, title, country_code=value['countryCode'], country_name=value['countryName'])


    elif column_type == ColumnType.dropdown:

        if value is None: 
            return DropdownValue(id, title)

        if value.__contains__('id'):
            return DropdownValue(id, title, label_id=value['id'])

        if value.__contains__('label'):
            return DropdownValue(id, title, label=value['label'])


    elif column_type == ColumnType.email:

        if value is None:
            return EmailValue(id, title)

        return EmailValue(id, title, email=value['email'], text=value['text'])


    elif column_type == ColumnType.long_text:

        if value is None:
            return LongTextValue(id, title)

        return LongTextValue(id, title, text=value['text'])


    elif column_type == ColumnType.name:
        return NameValue(id, title, name=value)


    elif column_type == ColumnType.numbers:

        if value is None:
            return NumberValue(id, title)

        return NumberValue(id, title, number=value)


    elif column_type == ColumnType.status:

        if value is None:
            return StatusValue(id, title)

        if value.__contains__('index'):
            return StatusValue(id, title, index=value['index'])

        if value.__contains__('label'):
            return StatusValue(id, title, label=value['label'])


    elif column_type == ColumnType.text:

        if value is None:
            return TextValue(id, title)

        return TextValue(id, title, text=value)