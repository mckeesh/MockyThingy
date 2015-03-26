__author__ = 'Shane'

import random
import string
import sys

def getRandomStrOfLen(length):
    charList = [random.choice(string.printable) for _ in range(length)]
    return ''.join(charList)

def createRandomListOfType(type_):
    randList = []
    listSize = random.randint(0, 1000)

    for _ in range(listSize):
        chosenType = random.choice(type_)
        randList.append(createRandomBuiltinValue(chosenType()))

    return randList

def createRandomDict(dictionaryOfTypes):
    randomDict = {}
    keyTypes = list(dictionaryOfTypes.keys())
    for keyType in keyTypes:
        valueTypes = dictionaryOfTypes[keyType]
        for valueType in valueTypes:
            randomKey = createRandomBuiltinValue(keyType())
            randomValue = createRandomBuiltinValue(valueType())
            randomDict[randomKey] = randomValue
    return randomDict

def createRandomBuiltinValue(variable):
    type_ = type(variable)
    domain1 = [0, 100]
    domain2 = [10000, 1000000]
    domain3 = [10000000, sys.maxsize]

    range = random.choice([domain1, domain2, domain3])
    randomInt = random.randint(range[0], range[1])

    if type_ == int:
        return randomInt
    elif type_ == float:
        return random.random() * randomInt
    elif type_ == complex:
        return complex(randomInt, random.randint(range[0], range[1]))
    elif type_ == str:
        #needs its own domain or this operation takes FOREVER
        domain1 = [0, 100]
        domain2 = [1000, 5000]
        domain3 = [5000, 10000]

        range = random.choice([[0,0], domain1, domain2, domain3])
        randomInt = random.randint(range[0], range[1])

        return getRandomStrOfLen(randomInt)
    elif type_ == list:
        return createRandomListOfType(variable)
    elif type_ == dict:
        return createRandomDict(variable)
    elif type_ == type(None):
        print('WARNING: Not sure how to generate random results for NoneType. Returning None')
        return None
    else:
        print("Don't know how to handle random generation for type", type_)