__author__ = 'Shane'

from DynamicMock import DynamicMock
import ClassInteractor
import MethodInteractor
from MockedTypes import MockedTypes

def createMockClassOfType(type_):
    mockObject = DynamicMock(spec=type_)
    class_ = type_()

    for each in ClassInteractor.getAllMethodNames(class_):
        method = ClassInteractor.getMethod(class_, each)
        returnType = MethodInteractor.getMethodReturnType(method)
        addMethodToMockedClass(mockObject, each, returnType)

    return mockObject

def getMockedObjectForType(type_):
    print("Mocking your object")

    if not isinstance(type_, type):
        type_ = type(type_)

    mockedTypesSingleton = MockedTypes()

    if mockedTypesSingleton.contains(type_):
        return mockedTypesSingleton.getMockedInstanceForType(type_)
    else:
        initParameterNames = MethodInteractor.getParameterNames(type_.__init__)
        initParameterValues = MethodInteractor.getParameterInputs(type_.__init__)
        mockedClass = createMockClassOfType(type_)
        # mockedClass.mockedClass = type_

        # index = 0
        # for each in initParameterNames:
        #     randomPrimitive = ValueGenerator.createRandomBuiltinValue(initParameterValues[index])
        #     ClassInteractor.addAttribute(mockedClass,each, randomPrimitive)
        #     index += 1
		#
        # realMethods = ClassInteractor.getAllMethodNames(type_)
        # for each in realMethods:
        #     method = ClassInteractor.getMethod(type_, each)
        #     returnType = MethodInteractor.getMethodReturnType(method)
        #     randomReturnValue = ValueGenerator.createRandomBuiltinValue(returnType())
        #     addMethodToMockedClass(mockedClass, each, randomReturnValue)

        mockedTypesSingleton.setMockedInstanceForType(type_, mockedClass)

        return mockedClass

def addMethodToMockedClass(class_, methodName, returnValue):
    class_.__dict__[methodName] = DynamicMock(return_value=returnValue)

