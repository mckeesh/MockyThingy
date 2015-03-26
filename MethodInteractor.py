__author__ = 'Shane'

import inspect
import ValueGenerator
import MockeryInteractor

def getParameterInputs(method):
    methodInfo = inspect.getfullargspec(method)
    defaultArgs = methodInfo[3]
    argInputs = []

    if not (len(methodInfo[0]) == 1 and methodInfo[0][0] == 'self'):
        for argument in defaultArgs:
            argumentType = type(argument)
            if _isOfPrimitiveType(argument):
                argInputs.append(ValueGenerator.createRandomBuiltinValue(argument))
            else:
                argInputs.append(MockeryInteractor.getMockedObjectForType(argumentType))

    return argInputs

def getParameterNames(method):
    methodInfo = inspect.getfullargspec(method)
    parameters = methodInfo[0]
    if 'self' in parameters:
        return parameters[1:]
    else:
        return parameters

def getMethodReturnType(method):
    methodInfo = inspect.getfullargspec(method)
    try:
        returnType = methodInfo[6]['return']
    except KeyError:
        raise Exception("Method " + method.__name__ + " must be annotated with return type")

    return returnType

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

def isBoundMethod(method):
    argspec = inspect.getfullargspec(method)
    arguments = argspec[0]
    if 'self' in arguments:
        return True
    else:
        return False

def _isOfPrimitiveType(variable):
    primitives = (int, str, float, bool, complex, list, dict, type(None))

    if isinstance(variable, primitives):
        return True
    else:
        return False