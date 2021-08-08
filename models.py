import abc

from database_manager import DBManager


class AbstractModel(abc.ABC):
    pass


class Model(AbstractModel):
    def __init__(self, *args, **kwargs):
        if args:
            raise TypeError(
                "Instantiating a document with positional arguments is not "
                "supported. Please use `field_name=value` keyword arguments."
            )
        for arg in kwargs:
            self.__getattr__(arg)

        self.data = kwargs

        for name in self.__annotations__:
            self.__setattr__(name, kwargs.get(name) or self.__getattr__(name))

    def __getattr__(self, item):
        if item in self.__annotations__:
            return None
        return self.__getattribute__(item)

    def __str__(self):
        return str({key: value for key, value in vars(self).items()})

    def objects(self):
        return DBManager(self)


class UserModel(Model):
    _id: int
    first_name: str
    last_name: str
    email: str
    p_number: str


class OrderModel(Model):
    id: int
    table: int
    status: str


UserModel(_id=12).objects().create()
