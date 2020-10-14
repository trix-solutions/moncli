class Update():

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        
        for key, value in kwargs.items():

            if key == 'body':
                self.body = value