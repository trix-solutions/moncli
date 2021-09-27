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