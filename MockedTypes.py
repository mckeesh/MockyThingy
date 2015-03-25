__author__ = 'Shane'

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MockedTypes(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.typeToInstanceDict = {}

    def getMockedInstanceForType(self, type_):
        return self.typeToInstanceDict[type_]

    def setMockedInstanceForType(self, type_, instance):
        self.typeToInstanceDict[type_] = instance

    def contains(self, type_):
        return type_ in self.typeToInstanceDict