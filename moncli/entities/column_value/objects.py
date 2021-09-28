from moncli import enums
from datetime import timedelta
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