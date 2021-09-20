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
