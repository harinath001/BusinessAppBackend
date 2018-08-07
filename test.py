class A():
    def __init__(self):
        print(self.__class__.__name__)
a = A()
print(a.__class__.__name__)