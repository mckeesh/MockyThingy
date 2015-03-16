__author__ = 'Shane'

class ClassToPass:
    def __init__(self, int1=int(), int2=int()):
        self.int1 = int1
        self.int2 = int2

    def gimmeTheSum(self, a, b) -> int:
        return a + b