class X:

    def __init__(self):
        self._c = None

    @property
    def c(self):
        print("yyyyy")
        return self._c

    @c.setter
    def c(self, value):
        print("xxxxx")
        self._c = value


x = X()
x.c = 2
