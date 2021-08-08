from core.managers import *
from user.models import *


class UserManager(DataBaseManager):
    def __init__(self):
        super(UserManager, self).__init__('"user"')

    def create(self, user_: User):
        self.curs.execute(
            f"INSERT INTO {self.table_name}(first_name,last_name,phone_number,email,password,type) VALUES ('{user_.first_name}','{user_.last_name}','{user_.phone_number}','{user_.email}','{user_.password}','{user_.type}')"
        )
        self.conn.commit()

    def read(self, phone_number, password):
        try:
            self.curs.execute(
                f"select * from {self.table_name} where phone_number='{phone_number}' and password='{password}'")
            user = self.curs.fetchone()

            u = User(user[1], user[2], user[3], user[4], user[5], user[6])
            u.id = user[0]
            return u
        except:
            return False

    def update(self, phone_number, password, col, val):
        self.curs.execute(
            f"update {self.table_name} set {col}='{val}' where phone_number='{phone_number}' and password='{password}'"
        )
        self.conn.commit()

    def delete(self, phone_number, password):
        self.curs.execute(
            f"delete from {self.table_name} where phone_number='{phone_number}' and password='{password}'"
        )
        self.conn.commit()

    def read_all(self):
        try:
            self.curs.execute(
                f"select phone_number, password from {self.table_name}")
            phone_pass = self.curs.fetchall()
            users = []
            for i in phone_pass:
                u = self.read(i[0], i[1])
                users.append(u)
            return users
        except:
            return False
