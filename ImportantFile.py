__author__ = 'Shane'

from ClassToPass import ClassToPass

class ImportantClass:

    def __init__(self):
        pass

    def doTheThing(self, number1=int(), number2=int(), classToPass=ClassToPass()) -> int:
        print("TheThing")
        print(number1, "plus", number2)
        added = classToPass.gimmeTheSum(number1, number2)
        print(added)
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
        print("ReturnsAClass")
        class_.int1 = 1000
        class_.int2 = 2000
        return class_

    def doTheListyThing(self, listy1=[int], listy2=[str]) -> int:
        return sum(listy1) + len(listy2)

    def doTheDictyThing(self, dict1={int:[int,str], str:[str]}) -> str:
        bigstring = ""
        for each in dict1.keys():
            bigstring += str(dict1[each])
        return bigstring