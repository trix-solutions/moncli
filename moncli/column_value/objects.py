from datetime import datetime, timedelta

from .. import enums


class Country(object):
  def __init__(self, name: str, code: str):
    self.name = name
    self.code = code


class Email(object):

    def __init__(self, email: str = None, text: str = None):
        self.email = email
        if not text:
            text = email
        self._text = text
        
    @property
    def text(self):
      return self._text
    
    @text.setter
    def text(self, value):
      if not value:
        self._text = self.email
      else:
        self._text = value
    
    def __repr__(self):
      return str({
        'email': self.email,
        'text': self.text
      })


class Hour(object):
  def __init__(self, hour: int, minute: int = 0):
    self.hour = hour
    self._minute = minute
    
  @property
  def minute(self):
    return self._minute
  
  @minute.setter
  def minute(self, value):
    if not value:
      self._minute = 0
    else: 
      self._minute = value


class Link(object):
  def __init__(self, url: str = None, text: str = None):
    self.url = url
    if not text:
      text = url
    self._text = text
    
  @property
  def text(self):
    return self._text
  
  @text.setter
  def text(self, value):
    if not value:
      self._text = self.url
    else:
      self._text = value


class Location(object):
  def __init__(self, lat: float = 0, lng: float = 0, address: str = None):
    self._lat = lat
    self._lng = lng
    self.address = address
    
  @property
  def lat(self):
    if not self._lat:
      return 0
    return self._lat
  
  @property
  def lng(self):
    if not self._lng:
      return 0
    return self._lng
  
  def __repr__(self):
    return str({
      'lat': self.lat,
      'lng': self.lng,
      'address': self.address
    })


class PersonOrTeam(object):
    """
    
    Properties
        id - `int`
            the ID of the Person or Team
        kind - str
            the name of the  enums.PeopleKind  associated with the Person or Team

    """
    def __init__(self,id,kind):
        self.id = id 
        self.kind=kind

    def __repr__(self):
        return str({
            'id': self.id,
            'kind': self.kind.name
        })


class Person(PersonOrTeam):
   def __init__(self, id):
        super(Person, self).__init__(id,kind=enums.PeopleKind.person)


class Team(PersonOrTeam):
   def __init__(self,id):
        super(Team, self).__init__(id, kind=enums.PeopleKind.team)


class Phone(object):
  def __init__(self, phone: str, code: str):
    self.phone = phone
    self.code = code
    
  def __repr__(self):
    return str({
      'phone': self.phone,
      'code': self.code
    })

      
class Timeline(object):
  
  def __init__(self, from_date: datetime, to_date: datetime, is_milestone: bool = False):
    self._from_date = from_date
    self._to_date = to_date
    self._is_milestone = is_milestone
    
  @property
  def from_date(self):
    return self._from_date
  
  @from_date.setter
  def from_date(self, value):
    self._from_date = value
    if self._is_milestone:
       self._to_date = value
        
  @property
  def to_date(self):
    return self._to_date
  
  @to_date.setter
  def to_date(self, value):
    self._to_date = value
    if self._is_milestone:
       self._from_date = value
        
  def __repr__(self):
    return str({
      'from': self.from_date,
      'to': self.to_date
    })


class Week(object):

    def __init__(self, start = None, end = None):
        self._start = start
        self._end = end
        self._calculate_dates(start)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._calculate_dates(value)

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        return self._calculate_dates(value)

    @property
    def week_number(self):
        return self._week_number

    def _calculate_dates(self, value):
        if not value:
            return value   
        self._start = value - timedelta(days=value.weekday())
        self._end = self._start + timedelta(days=6)
        self._week_number = self._start.isocalendar()[1]

    def __repr__(self):
        return str({
            'start': self._start,
            'end': self._end
        })