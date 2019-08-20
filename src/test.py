

class Something(object):
    a = 0
    b = 1

    def __new__(cls, *args, **kwargs):
        print(f"__new__ : {Something.a}")
        return super(Something, cls).__new__(cls)

    def __init__(self, a=2, b=3):
        Something.c = -1
        # self.a = a
        # self.b = b
        for name, val in locals().items():
            print(name, val)
            if name != "self":
                setattr(self, name, val)
        print(">>>", locals())
        # print(Something.a)


inst0 = Something()
inst1 = Something()

setattr(Something, "d", "Cool!")

print(inst0.a)
print("...", inst1.__dict__)
print(Something.__dict__)


def func(x, y):
    print(locals())


func(1, 2)

