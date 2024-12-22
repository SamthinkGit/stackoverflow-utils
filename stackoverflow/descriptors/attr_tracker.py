from collections import defaultdict

VERBOSE_TRACKING = True
ACCESS_LOG = defaultdict(lambda: defaultdict(bool))


class TrackedItem:

    def __init__(self, instance, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        global ACCESS_LOG
        if instance is None:
            return self

        if VERBOSE_TRACKING:
            print(f"[GET] Variable {self.storage_name} has been accesed.")
            ACCESS_LOG[instance][self.storage_name] = True

        return instance.__dict__[self.storage_name]

    def __set__(self, instance, value):
        if VERBOSE_TRACKING:
            print(f"[SET] Variable {self.storage_name} has been accesed.")
            ACCESS_LOG[instance][self.storage_name] = True

        instance.__dict__[self.storage_name] = value


class AttributeTracker:

    def __setattr__(self, name, value):
        cls = self.__class__
        setattr(cls, name, TrackedItem(self, name))
        self.__dict__[name] = value

    def accesed(self, key):
        return ACCESS_LOG[self][key]


class Cat(AttributeTracker):
    def __init__(self):
        self.head = "Head"
        self.paw = "Paw"

    def __repr__(self):
        return f"Cat({self.head=}, {self.paw=})"


if __name__ == "__main__":
    cat = Cat()
    cat_2 = Cat()

    print(cat)

    print(cat.accesed("head"))  # -> True
    print(cat.accesed("paw"))  # -> True

    print(cat_2.accesed("head"))  # -> False
    print(cat_2.accesed("paw"))  # -> False
