from core.models import *
import random


class Table(BaseTable):
    def __init__(self, number, position, status=0):
        self.number = number
        self.position = position
        self.status = status
        self.table_name = '"table"'


class Category(BaseCategory):
    def __init__(self, name):
        self.name = name


class MenuItem(BaseMenuItem):
    def __init__(self, name, price, category: Category, serving_time_period, estimated_cooking_time, discount=0):
        self.name = name
        self.price = price
        self.category = category
        self.discount = discount
        self.serving_time_period = serving_time_period
        self.estimated_cooking_time = estimated_cooking_time
        self.table_name = 'menu_item'


class Order(BaseOrder):
    Number = random.randint(100, 1000000)

    def __init__(self, table, status, menu_items):
        Order.Number += 1
        self.number = Order.Number
        self.table = table
        self.menu_items = menu_items  # [(menu_item,quantity),(menu_item,quantity),...]
        self.status = status
        self.date_time_stamp = date.today()
        self.time_time_stamp = time(hour=datetime.now().hour, minute=datetime.now().minute,
                                    second=datetime.now().second)
        self.table_name = 'order'


class Receipt(BaseReceipt):
    def __init__(self, order, discount: int = 0):
        self.order = order
        sum = 0
        for i in order.menu_items:
            sum += (i[0].price * i[1])
        self.total_price = sum
        self.final_price = sum - int((sum * discount) / 100)
        self.date_time_stamp = date.today()
        self.time_time_stamp = time(hour=datetime.now().hour, minute=datetime.now().minute,
                                    second=datetime.now().second)
        self.table_name = 'receipt'


class Message:
    def __init__(self, first_name, last_name, email, message):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.my_message = message
        self.date_time_stamp = date.today()
        self.time_time_stamp = time(hour=datetime.now().hour, minute=datetime.now().minute,
                                    second=datetime.now().second)
