from addict import Dict


class Base:
    name = "aaaa"

    def __init__(self):
        n = self.getname()
        print(f"name: {n}")
        print(self.name)

    @classmethod
    def getname(cls):
        return cls.name


class Derived(Base):
    name = "derived"


b = Base()

d = Derived()

x = Dict()

x.a.b = "c"
print(x)

del x.a["b"]
print(x)
