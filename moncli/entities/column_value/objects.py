from datetime import datetime

from moncli.config import DATE_FORMAT
from moncli import enums

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


class Timeline(object):
  
  def __init__(self, from_date: str, to_date: str, is_milestone: bool = False):
    self._from_date = datetime.strptime(from_date, DATE_FORMAT)
    self._to_date = datetime.strptime(to_date, DATE_FORMAT)
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