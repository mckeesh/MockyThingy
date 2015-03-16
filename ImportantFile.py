__author__ = 'Shane'

from ClassToPass import ClassToPass

class ImportantClass:

    def __init__(self):
        pass

    def doTheThing(self, number1=int(), number2=int()) -> int:
        print("TheThing")
        # print(number1, "plus", number2)
        added = number1 + number2
        return added

    def doTheOtherThing(self, class1=ClassToPass()) -> int:
        print("TheOtherThing")
        print(class1.int1, "plus", class1.int2)
        added = class1.int1 + class1.int2
        return added

    def doTheStringThing(self, str1="", str2="") -> str:
        print("TheStringThing")
        return str1+str2

    def returnTheThing(self, class_=ClassToPass()) -> ClassToPass:
        class_.int1 = 1000
        class_.int2 = 2000
        return class_