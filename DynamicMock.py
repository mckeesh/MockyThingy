__author__ = 'Shane'
from unittest.mock import Mock
import ClassInteractor
import MethodInteractor
import MockeryInteractor


class DynamicMock(Mock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'spec' in kwargs:
            self.mockedClass = kwargs['spec']

    # def __call__(self, *args, **kwargs):
    # 	print("Intercepted call")
    # 	print("args", args)
    # 	print("kwargs", **kwargs)
    # 	print("class:", self.mockedClass)
    #
    # 	if self.methodCalled is not None:
    # 		method = ClassInteractor.getMethod(self.mockedClass, self.methodCalled)
    # 		returnType = MethodInteractor.getMethodReturnType(method)
    # 		MockeryInteractor.addMethodToMockedClass(self, self.methodCalled, returnType)
    #
    # 	curframe = inspect.currentframe()
    # 	# calframe = inspect.getouterframes(curframe, 0)[1][3]
    # 	stack = inspect.stack(0)
    #
    # 	super().__call__(self, *args, **kwargs)
    # 	self.methodCalled = None

    # Thanks to kindall of StackOverflow for this idea
    def __getattr__(self, attributeName):
        inVariables = self.mockedClass().__dict__
        inMethods = self.mockedClass.__dict__

        if inVariables or inMethods:
            try:
                method = ClassInteractor.getMethod(self.mockedClass, attributeName)
                returnType = MethodInteractor.getMethodReturnType(method)
                returnValue = MethodInteractor.getRandomValueFor(returnType)
                MockeryInteractor.addMethodToMockedClass(self, attributeName, returnValue)
                #hacky. Change later :/
                return ClassInteractor.getMethod(self, attributeName)
            except AttributeError:
                variable = self.mockedClass().__dict__[attributeName]
                randomVariable = MethodInteractor.getRandomValueFor(variable)
                self.__dict__[attributeName] = randomVariable
                return self.__dict__[attributeName]
        else:
            raise AttributeError('No attribute ' +  attributeName + ' in class ' + self.mockedClass.__name__)