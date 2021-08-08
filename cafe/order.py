from my_flask.app_import import *
from datetime import timedelta
from cafe.managers import *
from cafe.models import *

orders = []
orders_show = []


def add_orders():
    item = request.args.get('item')
    number = request.args.get('number')
    # try:
    if item and number:
        print('a')
        menu_item_manager = MenuItemManager()
        menu_item = menu_item_manager.read(item)
        order = (menu_item, int(number))
        order_show = (item, number)
        orders_show.append(order_show)
        orders.append(order)
    if request.args.get('index'):
        print('b')
        orders.pop(int(request.args.get('index')))
        orders_show.pop(int(request.args.get('index')))

    if request.args.get('confirm'):
        print('c')
        table_manager = TableManager()
        order_manager = OrderManager()
        if request.args.get('table-number'):
            table = table_manager.read(request.args.get('table-number'))
            table_manager.update(request.args.get('table-number'), 'status', 1)
            table_manager.close()
        else:
            print('else')
            return orders_show

        order_model = Order(table, 0, orders)
        order_manager.create(order_model)
    return orders_show
    # except:
    #     return False
