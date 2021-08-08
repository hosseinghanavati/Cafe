from core.models import BaseUser


class User(BaseUser):
    def __init__(self, first_name, last_name, phone_number, password,  email, type='cashier'):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.type = type
        self.table_name = '"user"'
