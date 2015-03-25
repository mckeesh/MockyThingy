__author__ = 'Shane'

import inspect
import MethodInteractor

def callUnboundMethodWithRandomValues(class_, methodName):
    instantiatedClass = class_()
    unboundMethod = getattr(instantiatedClass, methodName)
    generatedParameters = MethodInteractor.getParameterInputs(unboundMethod)
    unboundMethod(*generatedParameters)

def getAttribute(class_, propertyName):
    return class_.__dict__[propertyName]

def addAttribute(class_, propertyName, propertyValue):
    class_.__dict__[propertyName] = propertyValue

def getMethod(class_, methodName):
    return getattr(class_, methodName)

def addMethodToClass(class_, method):
    class_.__dict__[method.__name__] = method

def getAllMethodNames(class_):
    names = []
    for each in inspect.getmembers(class_, predicate=inspect.isfunction):
        if not each[0].startswith("__"):
            names.append(each[0])
    return names

def getClass(moduleName, className):
    module = __import__(moduleName, fromlist=[className])
    class_ = getattr(module, className)
    return class_