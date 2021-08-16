class BaseCollection(object):
    
    def __init__(self, values: list = [], _type: type = str, key = lambda x: x):
        self._values = []
        self._key = key
        for value in values:
            if not isinstance(value, _type):
                raise TypeError('Expected data of type {}, got {} instead.'.format(_type.__name__, value.__class__.__name__))
            self._values.append(value)


    def __len__(self):
        return len(self._values)
        

    def __getitem__(self, index):
        return self._values[self._key(index)]


    def __setitem__(self, index, value):
        self._values[self._key(index)] = value


    def __iter__(self):
        for value in self._values:
            yield value

    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.__len__() != len(other):
            return False
        for val in self._values:
            if val not in other:
                return False
        return True


    def __repr__(self):
        return str(self._values)

    
    def insert(self, index, value):
        self._values.insert(self._key(index), value)


    def append(self, value):
        self.insert(len(self._values), value)