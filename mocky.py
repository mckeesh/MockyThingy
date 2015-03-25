#!/usr/bin/python
__author__ = 'Shane'

import sys
import os.path as path
import inspect
import random
import string
from unittest.mock import Mock

mockedTypes = {}


def getClass(moduleName, className):
    module = __import__(moduleName, fromlist=[className])
    class_ = getattr(module, className)
    return class_

def getAllMethodNames(class_):
    names = []
    for each in inspect.getmembers(class_, predicate=inspect.isfunction):
        if not each[0].startswith("__"):
            names.append(each[0])
    return names

def getMethod(class_, methodName):
    return getattr(class_, methodName)

def addMethodToClass(class_, method):
    class_.__dict__[method.__name__] = method

def addMethodToMockedClass(class_, methodName, returnValue):
    class_.__dict__[methodName] = Mock(return_value=returnValue)


def isBoundMethod(method):
    argspec = inspect.getfullargspec(method)
    arguments = argspec[0]
    if 'self' in arguments:
        return True
    else:
        return False


def allArgsHaveDefaults(method):
    methodInfo = inspect.getargspec(method)
    arguments = methodInfo[0]
    defaultArgs = methodInfo[3]

    if isBoundMethod(method):
        if len(arguments) > 1 and (not len(arguments) - 1 == len(defaultArgs)):
            raise Exception("Method " + method.__name__ + " doesn't seem to have defaults for every argument."
                                                          "This helps us determine what kind of random type to generate.")
    else:
        if len(arguments) > 1 and (not len(arguments) == len(defaultArgs)):
            raise Exception("Method " + method.__name__ + " doesn't seem to have defaults for every argument."
                                                          "This helps us determine what kind of random type to generate.")
    return True


def isOfPrimitiveType(variable):
    primitives = (int, str, float, bool, complex, list, type(None))

    if isinstance(variable, primitives):
        return True
    else:
        return False

def getRandomStrOfLen(length):
    charList = [random.choice(string.printable) for _ in range(length)]
    return ''.join(charList)

def createRandomListOfType(type_):
    randList = []
    listSize = random.randint(0, 1000)

    for _ in range(listSize):
        randList.append(createRandomBuiltinValue(type_()))

    return randList

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
        return createRandomListOfType(variable[0])
    elif type_ == type(None):
        print('WARNING: Not sure how to generate random results for NoneType. Returning None')
        return None
    else:
        print("Don't know how to handle random generation for type", type_)

def createMockClassOfType(type_):
    mockObject = Mock(spec=type_)
    class_ = type_()

    for each in getAllMethodNames(class_):
        addMethodToMockedClass(mockObject, each, getMethodReturnType(getMethod(class_, each)))

    return mockObject

def callMockedMethod(mockedObj, methodName):
    mockedObj.__dict__[methodName]()

def addAttribute(class_, propertyName, propertyValue):
    class_.__dict__[propertyName] = propertyValue

def getAttribute(class_, propertyName):
    return class_.__dict__[propertyName]

def getMockedObjectForType(type_):
    print("Mocking your object")
    if type_ in mockedTypes:
        return mockedTypes[type_]
    else:
        initParameterNames = getParameterNames(type_.__init__)
        initParameterValues = getParameterInputs(type_.__init__)
        mockedClass = createMockClassOfType(type_)

        index = 0
        for each in initParameterNames:
            randomPrimitive = createRandomBuiltinValue(initParameterValues[index])
            addAttribute(mockedClass,each, randomPrimitive)
            index += 1

        realMethods = getAllMethodNames(type_)
        for each in realMethods:
            returnType = getMethodReturnType(getMethod(type_, each))
            randomReturnValue = createRandomBuiltinValue(returnType())
            addMethodToMockedClass(mockedClass, each, randomReturnValue)

        mockedTypes[type_] = mockedClass
        return mockedClass

def getParameterInputs(method):
    methodInfo = inspect.getfullargspec(method)
    defaultArgs = methodInfo[3]
    argInputs = []

    for argument in defaultArgs:
        argumentType = type(argument)
        if isOfPrimitiveType(argument):
            argInputs.append(createRandomBuiltinValue(argument))
        else:
            argInputs.append(getMockedObjectForType(argumentType))

    return argInputs

def getParameterNames(method):
    methodInfo = inspect.getfullargspec(method)
    parameters = methodInfo[0]
    if 'self' in parameters:
        return parameters[1:]
    else:
        return parameters

def callUnboundMethodWithRandomValues(class_, methodName):
    instantiatedClass = class_()
    unboundMethod = getattr(instantiatedClass, methodName)
    generatedParameters = getParameterInputs(unboundMethod)
    unboundMethod(*generatedParameters)

def getMethodReturnType(method):
    methodInfo = inspect.getfullargspec(method)
    try:
        returnType = methodInfo[6]['return']
    except KeyError:
        raise Exception("Method " + method.__name__ + " must be annotated with return type")

    return returnType

def main():
    args = sys.argv

    if not len(args) == 3:
        raise Exception("Expected:\npython mocky.py inputFile.py classToTest")

    fileName = args[1]
    moduleName = fileName.split(".")[0].strip('/')
    classToTest = args[2]

    class_ = getClass(moduleName, classToTest)
    fileExists = path.isfile(fileName)
    if not fileExists:
        raise Exception("File " + fileName + " does not exist.")

    for methodName in getAllMethodNames(class_):
        if not methodName.startswith("__"):
            method = getMethod(class_, methodName)
            if isBoundMethod(method):
                callUnboundMethodWithRandomValues(class_, methodName)
            else:
                generatedParameters = getParameterInputs(method)
                method(*generatedParameters)


main()