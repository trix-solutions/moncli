from moncli import enums

class PersonOrTeam(object):
    """
    
    Properties
        id - `int`
            the ID of the Person or Team
        kind - str
            the name of the  enums.PeopleKind  associated with the Person or Team

    """
    def __init__(self,id,kind, **kwargs):
        # super(PersonOrTeam, self).__init__(kwargs)
        self.id = id 
        self.kind=kind

class Person(PersonOrTeam):
   def __init__(self, **kwargs):
        super(Person, self).__init__(kwargs)
        self.id = id 
        self.kind = enums.PeopleKind.person

class Team(PersonOrTeam):
   def __init__(self, **kwargs):
        super(Team, self).__init__(kwargs)
        self.id = id 
        self.kind = enums.PeopleKind.team