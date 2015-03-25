#!/usr/bin/python
__author__ = 'Shane'

import sys
import os.path as path
import MethodInteractor
import ClassInteractor

def main():
    args = sys.argv

    if not len(args) == 3:
        raise Exception("Expected:\npython mocky.py inputFile.py classToTest")

    fileName = args[1]
    moduleName = fileName.split(".")[0].strip('/')
    classToTest = args[2]

    class_ = ClassInteractor.getClass(moduleName, classToTest)
    fileExists = path.isfile(fileName)
    if not fileExists:
        raise Exception("File " + fileName + " does not exist.")

    for methodName in ClassInteractor.getAllMethodNames(class_):
        if not methodName.startswith("__"):
            method = ClassInteractor.getMethod(class_, methodName)
            if MethodInteractor.isBoundMethod(method):
                ClassInteractor.callUnboundMethodWithRandomValues(class_, methodName)
            else:
                generatedParameters = MethodInteractor.getParameterInputs(method)
                method(*generatedParameters)


main()