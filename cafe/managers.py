from core.managers import *
from cafe.models import *

from core.managers import *
from user.models import *


class TableManager(DataBaseManager):
    def __init__(self):
        super(TableManager, self).__init__('"table"')

    def create(self, t: Table):
        self.curs.execute(
            f"INSERT INTO {self.table_name}(number,position,status) VALUES ({t.number},'{t.position}',{t.status})"
        )
        self.conn.commit()

    def read(self, number):
        try:
            self.curs.execute(
                f"select * from {self.table_name} where number={number}")
            table = self.curs.fetchone()

            t = Table(table[1], table[2], table[3])
            t.id = table[0]
            return t
        except:
            return False

    def read_by_id(self, id: int):
        self.curs.execute(
            f"select * from {self.table_name} where id={id}")
        table = self.curs.fetchone()
        if table:
            t = Table(table[1], table[2], table[3])
            t.id = table[0]
            return t
        else:
            return False

    def update(self, number, col, val):
        self.curs.execute(
            f"update {self.table_name} set {col}='{val}' where number={number}"
        )
        self.conn.commit()

    def delete(self, number):
        self.curs.execute(
            f"delete from {self.table_name} where number={number}"
        )
        self.conn.commit()

    def read_all(self):
        try:
            self.curs.execute(
                f"select * from {self.table_name}")
            table = self.curs.fetchall()
            tables = []
            for i in table:
                t = Table(i[1], i[2], i[3])
                t.id = i[0]
                tables.append(t)
            return tables
        except:
            return False


class CategoryManager(DataBaseManager):
    def __init__(self):
        super(CategoryManager, self).__init__('"category"')

    def create(self, c: Category):
        self.curs.execute(
            f"INSERT INTO {self.table_name}(name) VALUES ('{c.name}')"
        )
        self.conn.commit()

    def read(self, name):
        try:
            self.curs.execute(
                f"select * from {self.table_name} where name='{name}'")
            category = self.curs.fetchone()

            c = Category(category[1])
            c.id = category[0]
            return c
        except:
            return False

    def read_by_id(self, id: int):
        try:
            self.curs.execute(
                f"select * from {self.table_name} where id={id}")
            category = self.curs.fetchone()

            c = Category(category[1])
            c.id = category[0]
            return c
        except:
            return False

    def update(self, name, col, val):
        self.curs.execute(
            f"update {self.table_name} set {col}='{val}' where name='{name}'"
        )
        self.conn.commit()

    def delete(self, name):
        self.curs.execute(
            f"delete from {self.table_name} where name='{name}'"
        )
        self.conn.commit()

    def read_all(self):
        try:
            self.curs.execute(
                f"select name from {self.table_name}")
            names = self.curs.fetchall()
            categories = []
            for i in names:
                c = self.read(i[0])
                categories.append(c)
            return categories
        except:
            return False
        # try:
        #     self.curs.execute(
        #         f"select * from {self.table_name}")
        #     category = self.curs.fetchall()
        #     categoryes = []
        #     for i in category:
        #         c = Category(i[1])
        #         c.id = i[0]
        #         categoryes.append(c)
        #     return categoryes
        # except:
        #     return False


class MenuItemManager(DataBaseManager):
    def __init__(self):
        super(MenuItemManager, self).__init__('"menu_item"')

    def create(self, m: MenuItem):
        cm = CategoryManager()
        category = cm.read(m.category.name)
        if category:
            c_id = category.id
        else:
            cm.create(m.category)
            c_id = cm.read(m.category.name).id
        cm.close()
        self.curs.execute(
            f"INSERT INTO {self.table_name}(name,price,discount,serving_time_period,estimate_cooking_time,category_id) VALUES ('{m.name}',{m.price},{m.discount},{m.serving_time_period},{m.estimated_cooking_time},{c_id})"
        )
        self.conn.commit()

    def read(self, name):
        try:
            cm = CategoryManager()
            self.curs.execute(
                f"select * from {self.table_name} where name='{name}'")
            menu_item = self.curs.fetchone()

            c_id = menu_item[6]
            category = cm.read_by_id(c_id)
            m = MenuItem(menu_item[1], menu_item[2], category, menu_item[4], menu_item[5], menu_item[3])
            m.id = menu_item[0]
            cm.close()
            return m
        except:
            return False

    def read_by_id(self, id: int):
        try:
            cm = CategoryManager()
            self.curs.execute(
                f"select * from {self.table_name} where id={id}")
            menu_item = self.curs.fetchone()

            c_id = menu_item[6]
            category = cm.read_by_id(c_id)
            m = MenuItem(menu_item[1], menu_item[2], category, menu_item[4], menu_item[5], menu_item[3])
            m.id = menu_item[0]
            cm.close()
            return m
        except:
            return False

    def update(self, name, col, val):
        self.curs.execute(
            f"update {self.table_name} set {col}='{val}' where name='{name}'"
        )
        self.conn.commit()

    def delete(self, name):
        self.curs.execute(
            f"delete from {self.table_name} where name='{name}'"
        )
        self.conn.commit()

    def read_all(self):
        try:
            self.curs.execute(
                f"select name from {self.table_name}")
            names = self.curs.fetchall()
            menu_items = []
            for i in names:
                m = self.read(i[0])
                menu_items.append(m)
            return menu_items
        except:
            return False


class OrderManager(DataBaseManager):
    def __init__(self):
        super(OrderManager, self).__init__('"order"')

    def create(self, o: Order):
        tm = TableManager()
        table = tm.read(o.table.number)
        self.curs.execute(
            f"INSERT INTO {self.table_name}(table_id,number,status,date_time_stamp,time_time_stamp) VALUES ({table.id},{o.number},{o.status},'{o.date_time_stamp}','{o.time_time_stamp}')"
        )
        self.conn.commit()

        mm = MenuItemManager()
        for i in o.menu_items:
            m = mm.read(i[0].name)
            o_id = self.get_id(o.number)
            self.curs.execute(
                f"insert into order_menu_item(order_id,menu_item_id,quantity) values ({o_id},{m.id},{i[1]})"
            )
            self.conn.commit()
        tm.close()
        mm.close()

    def get_id(self, number):
        self.curs.execute(
            f"select * from {self.table_name} where number={number}")
        o = self.curs.fetchone()
        return o[0]

    def read(self, number):
        try:
            self.curs.execute(
                f"select * from {self.table_name} where number={number}")
            order = self.curs.fetchone()
            self.curs.execute(
                f"select * from order_menu_item where order_id={order[0]}")
            order_menu_item = self.curs.fetchall()
            mm = MenuItemManager()
            lis = []
            for i in order_menu_item:
                lis.append((mm.read_by_id(i[2]), i[3]))
            mm.close()
            tm = TableManager()
            table = tm.read_by_id(order[1])

            o = Order(table, order[3], lis)
            o.date_time_stamp = order[4]
            o.time_time_stamp = order[5]
            o.number = order[2]
            o.id = order[0]
            tm.close()
            mm.close()
            return o
        except:
            return False

    def update(self, number, col, val):
        self.curs.execute(
            f"update {self.table_name} set {col}='{val}' where number={number}"
        )
        self.conn.commit()

    def read_all(self):
        try:
            self.curs.execute(
                f"select number from {self.table_name}")
            numbers = self.curs.fetchall()
            orders = []
            for i in numbers:
                o = self.read(i[0])
                orders.append(o)
            return orders
        except:
            return False

    def delete(self, number):
        self.curs.execute(
            f"delete from {self.table_name} where number={number}"
        )
        self.conn.commit()


class ReceiptManager(DataBaseManager):
    def __init__(self):
        super(ReceiptManager, self).__init__('"receipt"')

    def create(self, r: Receipt):
        om = OrderManager()
        order = om.read(r.order.number)
        self.curs.execute(
            f"INSERT INTO {self.table_name}(order_id,order_number,total_price,final_price,date_time_stamp,time_time_stamp) VALUES ({order.id},{order.number},{r.total_price},{r.final_price},'{r.date_time_stamp}','{r.time_time_stamp}')"
        )
        self.conn.commit()
        om.close()

    def read(self, order_number):
        try:
            self.curs.execute(
                f"select * from {self.table_name} where order_number={order_number}")
            receipt = self.curs.fetchone()
            om = OrderManager()
            order = om.read(receipt[2])
            r = Receipt(order, 0)
            r.total_price = receipt[3]
            r.final_price = receipt[4]
            r.date_time_stamp = receipt[5]
            r.time_time_stamp = receipt[6]
            r.id = receipt[0]
            om.close()
            return r
        except:
            return False

    def update(self, order_number, col, val):
        self.curs.execute(
            f"update {self.table_name} set {col}='{val}' where order_number={order_number}"
        )
        self.conn.commit()

    def delete(self, order_number):
        self.curs.execute(
            f"delete from {self.table_name} where order_number={order_number}"
        )
        self.conn.commit()

    def read_all(self):
        try:
            table_name = '"order"'
            self.curs.execute(
                f"select number from {table_name} ")
            numbers = self.curs.fetchall()
            receipt = []
            for i in numbers:
                r = self.read(i[0])
                if r:
                    receipt.append(r)
            return receipt
        except:
            return False


class MessageManager(DataBaseManager):
    def __init__(self):
        super(MessageManager, self).__init__('"message"')

    def create(self, m: Message):
        self.curs.execute(
            f"INSERT INTO {self.table_name}(first_name,last_name,email,my_message,date_time_stamp,time_time_stamp) VALUES ('{m.first_name}','{m.last_name}','{m.email}','{m.my_message}','{m.date_time_stamp}','{m.time_time_stamp}')"
        )
        self.conn.commit()

    def read(self, email):
        try:
            self.curs.execute(
                f"select * from {self.table_name} where email='{email}'")
            message = self.curs.fetchone()

            m = Message(message[1], message[2], message[3], message[4])
            m.id = message[0]
            m.date_time_stamp = message[5]
            m.time_time_stamp = message[6]
            return m
        except:
            return False

    def update(self, email, col, val):
        self.curs.execute(
            f"update {self.table_name} set {col}='{val}' where email='{email}'"
        )
        self.conn.commit()

    def delete(self, email):
        self.curs.execute(
            f"delete from {self.table_name} where email='{email}'"
        )
        self.conn.commit()

    def read_all(self):
        try:
            self.curs.execute(
                f"select email from {self.table_name}")
            emails = self.curs.fetchall()
            messages = []
            for i in emails:
                m = self.read(i[0])
                messages.append(m)
            return messages
        except:
            return False
