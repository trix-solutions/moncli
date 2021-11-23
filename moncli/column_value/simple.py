import pytz
from datetime import datetime, timedelta

from .. import enums, DATE_FORMAT, TIME_FORMAT, ColumnValueError
from .base import SimpleNullValue, ComplexNullValue
from .constants import SIMPLE_NULL_VALUE, COMPLEX_NULL_VALUE
from .objects import Email, Link, PersonOrTeam, Location, PersonOrTeam, Phone


class DateValue(ComplexNullValue):
    """A date column value."""
    native_type = datetime
    allow_casts = (int, str)
    has_time = False

    def _convert(self,value):
        try:
            new_time = datetime.strptime(value['time'], TIME_FORMAT)
            new_date = datetime.strptime(value['date'], DATE_FORMAT)
            self.has_time = True
            new_date = pytz.timezone('UTC').localize(new_date)
            new_date = new_date + timedelta(hours=new_time.hour, minutes=new_time.minute, seconds=new_time.second)
            date_value = new_date.astimezone(datetime.now().astimezone().tzinfo) 
            return date_value

        except (KeyError, TypeError):
            new_date = datetime.strptime(value['date'], DATE_FORMAT)
            return new_date
        
    def _cast(self,value):
        if isinstance(value,int):
            try: 
                new_date_value =  datetime.fromtimestamp(value)
                self.has_time = True
                return new_date_value

            except ValueError:
                raise ColumnValueError(
                    'invalid_unix_date',
                     self.id,
                    'Unable to convert "{}" from UNIX timestamp.'.format(value)
                )

        if isinstance(value, str):
            date_value = value.split()
            try:
                if len(date_value) == 1:
                    new_date = datetime.strptime(value, DATE_FORMAT)
                    return new_date
                if len(date_value) == 2:
                    self.has_time = True
                    new_format = '{} {}'.format(DATE_FORMAT, TIME_FORMAT) 
                    new_date = datetime.strptime(value, new_format)
                    return new_date
            except (TypeError, ValueError) as e:
                raise ColumnValueError(
                    'invalid_simple_date',
                     self.id,
                    'Unable to convert "{}" from a simple string date format.'.format(value)
                )
            
    def _format(self):
        if self.has_time:
            utc_date = self.value.astimezone(pytz.timezone('UTC'))
            date = datetime.strftime(utc_date, DATE_FORMAT)
            time = datetime.strftime(utc_date, TIME_FORMAT)
            return {'date': date, 'time': time}
        return {'date': datetime.strftime(self.value, DATE_FORMAT)}
        
        


class DropdownValue(ComplexNullValue):
    """A dropdown column value."""
    native_type = list
    native_default = []

    def _convert(self, value):
        labels = self.settings['labels']
        ids = value['ids']
        label_list = []

        for item in labels:
            if item['id'] in ids:
                label_list.append(item['name'])   
        return label_list

    def _format(self):
        labels = self.settings['labels']
        label_ids = [label['id'] for label in labels]
        label_names = [label['name'] for label in labels]
        ids = []
        for value in self.value:
            if isinstance(value,(int,str)):
                try:
                    value = int(value)
                    if value in label_ids:
                        ids.append(value)
                    else:
                        raise ColumnValueError(
                                'invalid_dropdown_index',
                                self.id,
                                'Dropdown does not contain index "{}".'.format(value)
                              )
                except ValueError:
                    if value in label_names:
                        list_id = [label['id'] for label in labels if label['name']==value][0]
                        ids.append(list_id)
                    else:
                        raise ColumnValueError(
                                'invalid_dropdown_label',
                                self.id,
                                'Dropdown does not contain label "{}".'.format(value)
                                   )
        ids = list(set(ids))
        return dict(ids=ids)    


class EmailValue(ComplexNullValue):
    """An email column value."""
    
    native_type = Email
    allow_casts = (str, dict)

    def _convert(self, value):
        try:
            email = value['email']
            text = value['text']
            return Email(email=email, text=text)
        except KeyError:
            raise ColumnValueError('invalid_email_data', self.id, 'Unable to convert "{}" to Email value.'.format(value))

    
    def _cast(self, value):
        try:
            if isinstance(value, str):
                email, text = value.split(' ',1)
                return Email(email=email, text=text)

            if isinstance(value, dict):
                email = value['email']
                text = value['text']
                return Email(email=email, text=text)

        except KeyError:
            raise ColumnValueError('invalid_email_data', self.id, 'Unable to convert "{}" to Email value.'.format(value))


    def _format(self):
        if self.value.email == None:
            return COMPLEX_NULL_VALUE
        if self.value.email != None and self.value.text == None:
            return {'email': self.value.email, 'text': self.value.email}
        
        return {'email': self.value.email, 'text': self.value.text}


class LinkValue(ComplexNullValue):
    """A link column value."""
    
    native_type = Link
    allow_casts = (str, dict)

    def _convert(self, value):
        try: 
            url = value['url']
            text = value['text']
            return Link(url=url, text=text)
        except KeyError:
            raise ColumnValueError('invalid_link_data', self.id, 'Unable to convert "{}" to Link value.'.format(value))

    
    def _cast(self, value):
        try:
            if isinstance(value, str):
                url, text = value.split(' ',1)
                return Link(url=url, text=text)

            if isinstance(value, dict):
                url = value['url']
                text = value['text']
                return Link(url=url, text=text)

        except KeyError:
            raise ColumnValueError('invalid_link_data', self.id, 'Unable to convert "{}" to Link value.'.format(value))


    def _format(self):
        if self.value.url == None:
            return COMPLEX_NULL_VALUE
        if self.value.url != None and self.value.text == None:
            return {'url': self.value.url, 'text': self.value.url}
        return {'url': self.value.url, 'text': self.value.text}


class LongTextValue(ComplexNullValue):
    """A long text column value."""
    
    native_type = (str)
    allow_casts = (int, float)
    
    def _convert(self, value): 
        return value['text']            
   
    def _format(self):
        return {'text': self._value}

class LocationValue(ComplexNullValue):
    """A location column value."""

    native_type = Location
    allow_casts = (dict, str)

    def _convert(self, value):
        return Location(lat=value['lat'],lng=value['lng'],address=value['address'])

    def _cast(self, value):

        if isinstance(value, dict):
            try:
                return Location(
                    value['lat'],
                    value['lng'],
                    value.get('address', None))
            except KeyError:
                raise ColumnValueError(
                    'invalid_location_data',
                    self.id,
                    'Unable to convert "{}" to Location value.'.format(value)
                )
        elif isinstance(value, str):
            values = value.split(' ', 2)
            if len(values) < 2:
                raise ColumnValueError(
                    'invalid_location_data',
                    self.id,
                    'Both a latitude and longitude are required for a Location value.')
            try:
                location = Location(float(values[0]), float(values[1])) # The lat and lng values must be cast into floats
                try:
                    location.address = values[2] 
                except IndexError:
                    pass 
                return location
            except ValueError:
                raise ColumnValueError(
                    'invalid_location_data',
                    self.id,
                    'Input str value "{}" contains invalid coordinates.'.format(value))
    
    def _format(self):
        return {'lat': self.value.lat, 'lng': self.value.lng, 'address': self.value.address}
 



class NumberValue(SimpleNullValue):
    """A number column value."""

    native_type = (int,float)
    allow_casts = (str)
    
    def _convert(self, value):
        if self.__isint(value):
           return int(float(value))
        elif self.__isfloat(value):
           return float(value)
        

    def _cast(self, value):
        if isinstance(value,self.allow_casts):
            if self.__isint(value):
                return int(value)
            elif self.__isfloat(value):
                return float(value)
        raise ColumnValueError(
                'invalid_number',
                self.id,
                'Unable to convert "{}" to a number value.'.format(value)
                )

    def _format(self):
        if self.value != None:
            return self.allow_casts(self.value)
        return SIMPLE_NULL_VALUE

    def __isfloat(self, value):
        """Is the value a float."""
        try:
            float(value)
        except ValueError:
            return False
        return True
  
    def __isint(self, value):
        """Is the value an int."""
        try:
            a = float(value)
            b = int(a)
        except ValueError:
            return False
        return a == b


class PeopleValue(ComplexNullValue):
    """A people column value."""

    native_type = list
    native_default = []
    allow_casts = ()

    def _convert(self, value):
        return_list = []
        value_list = value['personsAndTeams']
        for value_data in value_list:
            return_data = PersonOrTeam(
                            value_data['id'], 
                            enums.PeopleKind[value_data['kind']]
                            )
            return_list.append(return_data)
        return return_list
    
    def _format(self):
        personsAndTeams = []
        for list_item in self.value:
            if not isinstance(list_item,PersonOrTeam):
                raise ColumnValueError(
                    'invalid_people_value',
                    self.id,
                    'Invalid person or team value "{}".'.format(list_item)
                )
            id = list_item.id
            peopleKind = list_item.kind
            personsAndTeams.append({ 'id': id, 'kind': peopleKind.name })
        return {'personsAndTeams': personsAndTeams}


class PhoneValue(ComplexNullValue):
    """A phone column value."""

    native_type = Phone
    allow_casts = (str, dict)


    def _convert(self, value):
        try:
            phone = value['phone']
            code = value['countryShortName']
            return Phone(phone=phone, code=code)
        except KeyError:
            raise ColumnValueError('invalid_phone_data', self.id, 'Unable to convert "{}" to Phone value.'.format(value))

    
    def _cast(self, value):
        try:
            if isinstance(value, str):
                phone, code = value.split(' ', 1)
                return Phone(phone=phone, code=code)

            if isinstance(value, dict):
                phone = value['phone']
                code = value['code']
                return Phone(phone=phone, code=code)
        except KeyError:
            raise ColumnValueError('invalid_phone_data', self.id, 'Unable to convert "{}" to Phone value.'.format(value))


    def _format(self):
        if (self.value.phone == None) or (self.value.code == None):
            return COMPLEX_NULL_VALUE
        return {'phone': self.value.phone, 'countryShortName': self.value.code}

class StatusValue(ComplexNullValue):
    """A status column value."""
    native_type = str
    allow_casts = (int, str)

    def _convert(self, value):
        settings = self.settings
        labels = settings['labels']
        index = str(value['index'])
        if not self.text and index not in labels:
            return None
        return labels[index]
    
    def _cast(self, value):
        if isinstance(value,int):
            index = str(value)
            labels = self.settings['labels']
            try:
                value = labels[index]
                return value
            except KeyError:
                raise ColumnValueError( 'invalid_status_index',self.id,
                                        'Cannot find a status with the following index "{}"'.format(value)
                 )
        if isinstance(value,str):
            labels = self.settings['labels']
            try:
                int(value)
                label = labels[value]
                return label
            except (ValueError,KeyError):
                if value in labels.values():
                    return value
                raise ColumnValueError( 'invalid_status_index',self.id,
                                        'Cannot find a status with the following index "{}"'.format(value))
        
    def _format(self):
        index = None
        labels = self.settings['labels']
        for key, value in labels.items():
            if self.value == value:
                index= int(key)
                break
        return dict(index=index)

class TextValue(SimpleNullValue):
    """A text column value."""

    native_type = str
    allow_casts = (int, float)
