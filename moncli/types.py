import pytz, json, re
from datetime import datetime, timedelta, timezone
from enum import EnumMeta
from pytz.exceptions import UnknownTimeZoneError

from pycountry import countries
from schematics.exceptions import ConversionError, ValidationError
from schematics.types import BaseType

from . import enums

from . import column_value as cv
from .config import *


class MondayType(BaseType):

    native_type = None
    null_value = None
    allow_casts = ()
    native_default = None
    is_readonly = False

    def __init__(self, id: str = None, title: str = None, *args, **kwargs):
        self.original_value = None
        metadata = kwargs.pop('metadata', {})

        if not id and not title:
            raise TypeError('"id" or "title" parameter is required.')
        if id:
            metadata['id'] = id
        if title:
            metadata['title'] = title

        # Handle defaults
        default = kwargs.pop('default', None)
        if not default:
            default = self.native_default
        super(MondayType, self).__init__(*args, default=default, metadata=metadata, **kwargs)

    @property
    def changed_at(self):
        value = self.metadata.get('changed_at', None)
        if not value:
            return None
        changed_at = datetime.strptime(value, ZULU_FORMAT)
        utc = pytz.timezone('UTC')
        changed_at = utc.localize(changed_at, is_dst=False)
        return changed_at.astimezone(datetime.now().astimezone().tzinfo)

    def to_native(self, value, context=None):
        if not value:
            return self.native_default

        if not isinstance(value, cv.ColumnValue):
            if self.is_readonly:
                return value
            if isinstance(value, self.native_type):
                return self._process(value)
            if self.allow_casts and isinstance(value, self.allow_casts):
                return self._cast(value)
            raise ConversionError("Couldn't interpret '{}' as type {}.".format(str(value), self.native_type.__name__))

        self.metadata['id'] = value.id
        self.metadata['title'] = value.title
        settings = json.loads(value.settings_str) if value.settings_str else {}
        for k, v in settings.items():
            self.metadata[k] = v
        return self._process_column_value(value)

    def to_primitive(self, value, context=None):
        if self.null_value == None:
            return None
        if not value:
            return self.null_value
        # Assume that conversions are necessary before exporting
        value = self.to_native(value)
        return self._export(value)

    def _process(self, value):
        return value

    def _cast(self, value):
        return self.native_type(value)

    def _process_column_value(self, value: cv.ColumnValue):
        return value.value

    def _export(self, value):
        return value


class CheckboxType(MondayType):
    native_type = bool
    native_default = False
    allow_casts = (int, str)
    null_value = {}

    def _export(self, value):
        if value == True:
            return {'checked': 'true'}

class CountryType(MondayType):

    native_type = cv.Country
    allow_casts = (dict,)
    null_value = {}

    def _cast(self, value):
        try:
            return cv.Country(name = value['country'], code = value['code'])
        except KeyError:
            raise ConversionError('Unable to convert value "{}" to Country.'.format(value))
        
    def _export(self, value):
        if value.name and value.code:
            return {'countryName': value.name, 'countryCode': value.code}
        return self.null_value
    
    def validate_country(self, value): 
        country = countries.get(name=value.name)
        if not country:
            raise ValidationError('Value "{}" is not a valid country.'.format(value.name))
        code = countries.get(alpha_2=value.code)
        if not code:
            raise ValidationError('Value "{}" is not a valid alpha 2 country code.'.format(value.code))


class CreationLogType(MondayType):

    native_type = datetime
    native_default = None
    is_readonly = True

    
class DateType(MondayType):

    native_type = datetime
    allow_casts = (str, int)
    null_value = {}
    has_time = False

    def __init__(self, id: str = None, title: str = None, has_time: bool = False, *args, **kwargs):
        self.id = id
        self.title = title
        self.has_time = has_time
        super().__init__(self.id, self.title, *args, **kwargs)

    def _cast(self, value):
        if isinstance(value, int):
            try:
                return datetime.fromtimestamp(value)
            except ValueError:
                raise ConversionError('Invalid UNIX timestamp "{}".'.format(value))
        if isinstance(value, str):
            try:
                date = datetime.strptime(value.split(' ', 1)[0], DATE_FORMAT)
            except ValueError:
                raise ConversionError('Cannot convert value "{}" into Date.'.format(value))
            if self.has_time == True:
                try:
                    time = datetime.strptime(value.split(' ', 1)[1], TIME_FORMAT)
                    date = date + timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
                    return date
                except ValueError:
                    raise ConversionError('Cannot convert value "{}" into Time.'.format(value))
            return date

    def _export(self, value):
        if self.has_time == True:
            value = value.astimezone(timezone.utc)
            date = value.date().strftime(DATE_FORMAT)
            time = value.time().strftime(TIME_FORMAT)
            return {'date': date, 'time': time}
        return {'date': value.date().strftime(DATE_FORMAT), 'time': None}


class DependencyType(MondayType):

    native_type = list
    native_default = []
    null_value = {}

    def _process(self, value):
        value_list = []
        for data in value:
            try:
                value_list.append(int(data))
            except ValueError:
                raise ConversionError('Invalid item ID: "{}".'.format(data))
        return value_list
    
    def _export(self, value):
        return { 'item_ids': [data for data in value]}


class DropdownType(MondayType):
    native_type = list
    native_default = []
    null_value = {}
    element_type = str

    def __init__(self, id: str = None, title: str = None, as_enum: type = None, *args, **kwargs):
        if as_enum:
            self.element_type = as_enum
        super().__init__(id=id, title=title, *args, **kwargs)


    def _process(self, value):
        labels = {}
        return_list = []
        
        [labels.__setitem__(data['id'], data['name']) for data in self.metadata['labels']]
        for val in value:
            if isinstance(self.element_type, EnumMeta) and isinstance(val, self.element_type):
                return_list.append(val)
                continue
            try:
                label = labels[int(val)]
            except KeyError:
                raise ConversionError('Value "{}" is not a valid dropdown index.'.format(val))
            except ValueError:
                label = str(val)
                if not (label in labels.values()):
                    raise ConversionError('Value "{}" is not a valid dropdown label.'.format(val))
            if isinstance(self.element_type, EnumMeta):
                return_list.append(self.element_type(label))
            else:
                return_list.append(label)
        return return_list

    
    def _process_column_value(self, value: cv.ColumnValue):
        if isinstance(self.element_type,EnumMeta):
            return [self.element_type(data) for data in value.value]
        return super()._process_column_value(value)


    def _export(self, value):
        labels = {}
        for data in self.metadata['labels']:
            k,v = data.values()
            labels[v] = k
        
        labels_str = value
        if isinstance(self.element_type,EnumMeta):
            labels_str = [data.value for data in value]

        return_list =  [labels[label] for label in labels_str]
        return { 'ids': return_list}


class EmailType(MondayType):
    native_type = cv.Email
    null_value = {}
    allow_casts = (dict, )

    def _cast(self, value):
        try:
            return cv.Email(value['email'],value.get('text', value['email']))
        except KeyError:
            raise ConversionError('Cannot convert value "{}" to Email.'.format(value))

    def _export(self, value):
        return {'email': value.email, 'text': value.text}

    def validate_email(self, value):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if value.email and not re.fullmatch(regex, value.email):
            raise ValidationError('Value "{}" is not a valid email address.'.format(value))


class HourType(MondayType):
    native_type = cv.Hour
    null_value = {}
    allow_casts = (dict, )

    def _cast(self, value):
        try:
            return cv.Hour(value['hour'],value.get('minute', 0))
        except KeyError:
            raise ConversionError('Cannot convert value "{}" into Hour.'.format(value))
    def _export(self, value):
        return {'hour': value.hour, 'minute': value.minute}

    def validate_hour(self,value):
        if (value.hour > 23) or (value.hour < 0):
            raise ValidationError('Hour values must be between 0-23, not "{}".'.format(value.hour))
        if (value.minute > 59) or (value.minute < 0):
            raise ValidationError('Minute values must be between 0-59, not "{}".'.format(value.minute))


class ItemLinkType(MondayType):

    native_type = list
    native_default = []
    null_value = {}
    multiple_values = True
    element_type = int

    def __init__(self, id: str = None, title: str = None, multiple_values: bool = True, *args, **kwargs):
        self.multiple_values = multiple_values
        if not multiple_values:
            self.native_type = int
            self.native_default = None
            self.element_type = None
            self.allow_casts = (str,)
        super().__init__(id, title, *args, **kwargs)

    def _process(self, value):
        if not self.multiple_values:
            return value
        elif self.multiple_values:
            return_list = []   
            for data in value:
                try:
                    return_list.append(int(data))
                except ValueError:
                    raise ConversionError('Invalid item ID "{}".'.format(data))
            return return_list
            
    def _process_column_value(self, value: cv.ItemLinkValue):
        try:
            self.multiple_values = value.settings['allowMultipleItems']
        except KeyError:
            self.multiple_values = True
        if not self.multiple_values:
            self.native_type = int
            self.native_default = None
            self.element_type = None
            self.allow_casts = (str,)
            return value.value[0]
        return super()._process_column_value(value)

    def _export(self, value):
        if not self.multiple_values:
            return_value = int(value) if isinstance(value,int) else int(value[0])
            return {'item_ids': [return_value] }
        return {'item_ids': [int(data) for data in value ] }


class LastUpdatedType(MondayType):

    native_type = datetime
    native_default = None
    is_readonly = True


class LinkType(MondayType):
    
    native_type = cv.Link
    null_value = {}
    allow_casts = (dict,)

    def _cast(self, value):
        try:
            return cv.Link(value['url'],value['text'])
        except KeyError:
            raise ConversionError('Cannot convert value "{}" to Link.'.format(value))
    
    def _export(self, value):
        if value.url != None:
            return {'url': value.url, 'text': value.text}
        return self.null_value

    def validate_link(self,value):
        str_value = value.url
        if not (str_value.startswith('https://') or str_value.startswith('http://')):
            raise ValidationError('Value "{}" is not a valid URL link.'.format(value))
        return str_value


class LocationType(MondayType):

    native_type = cv.Location
    allow_casts = (dict,)
    null_value = {}

    def _cast(self, value):
        try:
            return cv.Location(lat=value['lat'],lng=value['lng'], address=value.get('address', None))
        except KeyError:
            raise ConversionError('Cannot convert "{}" to Location.'.format(value))

    def _export(self, value):
        if value.lat and value.lng:
            return { 'lat': value.lat,'lng': value.lng, 'address': value.address }
        return self.null_value
    
    def validate_location(self,value):
        if not (-90 <= value.lat <= 90):
            raise ValidationError('Value "{}" is not a valid Latitude.'.format(value))
        if not (-180 <= value.lng <= 180):
            raise ValidationError('Value "{}" is not a valid Longitude.'.format(value))


class LongTextType(MondayType):
    native_type = str
    allow_casts = (int, float)
    null_value = {}

    def _export(self, value):
        return {'text': value}


class NumberType(MondayType):
    native_type = (int, float)
    allow_casts = (str, )
    null_value = ""
    
    def _cast(self, value):
        try:
            number_value = int(value) if int(value) else float(value)
            return number_value
        except TypeError:
            raise ConversionError('Couldn\'t interpret str {} as int or float.'.format(value))
    
    def _export(self, value):
        return str(value)


class PeopleType(MondayType):

    native_type = list
    native_default = []
    null_value = {}
    element_type = cv.PersonOrTeam
    max_allowed = 0

    def __init__(self, id: str = None, title: str = None, max_allowed: int = 0, *args, **kwargs):
        self.max_allowed = max_allowed
        if max_allowed > 4 or max_allowed < 0:
            self.max_allowed = 0
        if max_allowed == 1:
            self.native_type = cv.PersonOrTeam
            self.native_default = None
            self.allow_casts = (dict, int, str)
            self.element_type = None
        super().__init__(id, title, *args, **kwargs)

    def _process(self, value):
        if isinstance(value,cv.PersonOrTeam):
            return value
        return_list = []
        for data in value:
            if isinstance(data,cv.PersonOrTeam):
                return_list.append(data)
                continue
            try:
                if isinstance(data, dict):
                    id = int(data['id'])
                    kind = enums.PeopleKind[data['kind']]
                    return_list.append(cv.PersonOrTeam(id=id,kind=kind))               
                elif isinstance(data, (str,int)):
                    return_list.append(cv.Person(int(data)))
                else:
                    raise ValueError('')
            except (ValueError, KeyError):
                raise ConversionError('Cannot convert value "{}" to Person or Team.'.format(data))
        return return_list


    def _cast(self, value):
        try:
            if isinstance(value, dict):
                return cv.PersonOrTeam(value['id'],enums.PeopleKind[value['kind']])
            if isinstance(value, (int,str)):
                return cv.Person(int(value))
        except (ValueError, KeyError):
            raise ConversionError('Cannot convert value "{}" to Person or Team.'.format(value))


    def _process_column_value(self, value: cv.ColumnValue):
        if 'max_people_allowed' in self.metadata:
            self.max_allowed = int(self.metadata['max_people_allowed'])
        if self.max_allowed == 1:
            self.native_type = cv.PersonOrTeam
            self.native_default = None
            self.allow_casts = (dict, int, str)
            self.element_type = None
            try:
                return value.value[0]
            except IndexError:
                return self.native_default
        return super()._process_column_value(value)

    def _export(self, value):
        if self.max_allowed == 1:
            return {'personsAndTeams': [{'id': value.id, 'kind': value.kind.name}]}
        personsAndTeams = [{'id': data.id, 'kind': data.kind.name} for data in value]
        return {'personsAndTeams': personsAndTeams}
        
    def validate_people(self, value):
        if self.max_allowed == 1 and not isinstance(value, cv.PersonOrTeam):
            raise ValidationError('Value contains too many Person or Team values: "{}".'.format(len(value)))
        if self.max_allowed in [2, 3] and len(value) > 4:
            raise ValidationError('Value contains too many Person or Team values: "{}".'.format(len(value)))


class PhoneType(MondayType):

    native_type = cv.Phone
    allow_casts = (dict,str)
    null_value = {}

    def _cast(self, value):
        if isinstance(value, dict):
            try:
                return cv.Phone(phone=value['phone'],code=value['code'])
            except KeyError:
                raise ConversionError('Unable to convert value "{}" to Phone.'.format(value))
        elif isinstance(value, str):
            values = value.split(" ",1)
            try:
                return cv.Phone(phone=values[0],code=values[1])
            except IndexError:
                raise ConversionError('Unable to convert value "{}" to Phone.'.format(value))

    def _export(self, value):
        if value.phone and value.code:
            return {'phone': value.phone, 'countryShortName': value.code}
        return self.null_value
    
    def validate_country_code(self, value):
        country = countries.get(alpha_2=value.code)
        if not country:
            raise ValidationError('Value "{}" is not a valid alpha 2 country code.'.format(value.code))


class RatingType(MondayType):
    native_type = int
    allow_casts = (str,)
    null_value = {}

    def _cast(self, value):
        try:
            return int(value)
        except ValueError:
            raise ConversionError('Value "{}" is not a valid rating.'.format(value))
    
    def _export(self, value):
        return { 'rating': value}


class StatusType(MondayType):
    native_type = str
    allow_casts = (int,)
    null_value = {}

    def __init__(self, id: str = None, title: str = None, as_enum: type = None ,  *args, **kwargs):
        if as_enum:
            if not isinstance(as_enum, EnumMeta):
                raise TypeError('Invalid type "{}" for status Enum.'.format(as_enum.__name__))
            self.choices = list(as_enum)
            for value in self.choices:
                if not isinstance(value.value, str):
                    raise TypeError('Invalid value "{}" for status Enum "{}".'.format(value.value, value.__class__.__name__))
            self.native_type =  as_enum
            self.allow_casts = (str,)
            
        super().__init__(id=id, title=title, *args, **kwargs)
    
    def _process(self, value):
        labels = self.metadata['labels']
        if self.native_type != str:
            return value
        try:
            int(value)
            try:
                return labels[value]
            except KeyError:
                raise ConversionError('Cannot find status label with index "{}".'.format(value))
        except ValueError:
            if value in labels.values():
                return value
            raise ConversionError('Cannot find status label "{}".'.format(value))
                
    def _cast(self, value):
        labels = self.metadata['labels']
        label = str(value)
        if self.native_type == str and isinstance(value,int):
            try:    
                return labels[label]
            except KeyError:
                raise ConversionError('Cannot find status label with index "{}".'.format(value))
            
        if isinstance(self.native_type, EnumMeta) and isinstance(value,str):
            try:
                return self.native_type(label)
            except ValueError:
                    raise ConversionError('Cannot find status label with index "{}".'.format(value))
    
    def _process_column_value(self, value: cv.ColumnValue):
        if self.native_type == str:
            self.choices = [value for value in self.metadata['labels'].values()]
        return super()._process_column_value(value)
                      
    def _export(self, value):
            labels = self.metadata['labels']
            if self.native_type == str:
                label = value
            elif isinstance(self.native_type, EnumMeta):
                label = value.value
            for index, value in labels.items():
                if value == label:
                    return {'index': int(index)}


class SubItemType(MondayType):

    native_type = list
    native_default = []
    null_value = {}
    is_readonly = True
 

class TextType(MondayType):
    native_type = str
    allow_casts = (int, float)
    null_value = ""


class TagsType(MondayType):
    native_type = list
    native_default = []
    null_value = {}

    def _process(self, value):
        for tag in value:
            try:
                return_value = [int(tag) for tag in value]
            except ValueError:
                raise ConversionError('Invalid Tag ID "{}".'.format(tag))
        return return_value
    
    def _export(self, value):
        return {'tag_ids': value}
        
        
class TimelineType(MondayType):

    native_type = cv.Timeline
    allow_casts = (dict,)
    null_value = {}

    def _cast(self, value):
        try:
            from_date = value['from']
            to_date = value['to']
            return cv.Timeline(from_date=from_date, to_date=to_date)
        except KeyError:
            raise ConversionError('Could not convert value "{}" to Timeline.'.format(value))

    def  _process_column_value(self, value: cv.ColumnValue):
        try:
            if value.settings['visualization_type']:
                self.metadata['is_milestone'] = True
        except KeyError:
            self.metadata['is_milestone'] = False
        return super()._process_column_value(value)

    def _export(self, value):
        if value.from_date == None or value.to_date == None:
            return {}
        return {'from': value.from_date.strftime(DATE_FORMAT), 'to': value.to_date.strftime(DATE_FORMAT)}
        
    def validate_timeline(self,value):
         if value.from_date > value.to_date:
            raise ValidationError('Timeline from date cannot be after to date.')


class TimeZoneType(MondayType):
    native_type = str
    null_value = {}

    def _export(self, value):
        return {'timezone': value}

    def validate_timezone(self, value):
        try:
            pytz.timezone(value)
        except (UnknownTimeZoneError):
            raise ValidationError('Unknown time zone "{}".'.format(value))


class WeekType(MondayType):
    
    native_type = cv.Week
    null_value = {}
    allow_casts = (dict,)

    def _cast(self, value):
        try:
            return cv.Week(value['start'],value['end'])
        except KeyError:
            raise ConversionError('Cannot convert value "{}" to Week.'.format(value))
    
    def _export(self, value):
        if not (value.start and value.end) :
            return self.null_value
        start =  value.start.strftime(DATE_FORMAT) 
        end  = value.end.strftime(DATE_FORMAT)
        return  {'week': {'startDate': start, 'endDate': end}}