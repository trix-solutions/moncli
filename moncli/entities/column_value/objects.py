from moncli import enums

class PersonOrTeam(object):
    """
    
    Properties
        id - `int`
            the ID of the Person or Team
        kind - str
            the name of the  enums.PeopleKind  associated with the Person or Team

    """
    def __init__():
        def __init__(self, **kwargs):
            super(PersonOrTeam, self).__init__(kwargs)
            id = (int,str)
            kind = enums.PeopleKind
