from my_flask.app_import import *
from cafe.models import *
from cafe.managers import *
from datetime import timedelta
from cafe.utility import *


def cashier_page_content():
    if request.method == 'POST':
        name = request.form.get('name')
        if name == 'cashier_order_list':
            number = int(request.form.get('number'))
            status = int(request.form.get('status'))
            om = OrderManager()
            om.update(number, 'status', status)

            rm = ReceiptManager()
            tm = TableManager()
            if status == 3:
                order = om.read(number)
                receipt = Receipt(order, 10)
                rm.create(receipt)
                tm.update(order.table.number, 'status', 0)
            elif status == -1:
                order = om.read(number)
                receipt = Receipt(order, 0)
                rm.create(receipt)
                tm.update(order.table.number, 'status', 0)
            tm.close()
            om.close()
            rm.close()
        if name == 'add_menu_item':
            operation = request.form.get('operation')
            if operation == 'add_order':
                cm = CategoryManager()
                info = request.form
                print(request.form)
                c = cm.read(info['order_category_name'])
                serving_time = ''
                if info['order_sobh'] == 'ok':
                    serving_time += '1'
                if info['order_zohr'] == 'ok':
                    serving_time += '2'
                if info['order_shab'] == 'ok':
                    serving_time += '3'
                menu_item = MenuItem(info['order_name'], int(info['order_price']), c, serving_time,
                                     int(info['order_cooking_time']), int(info['order_discount']))
                mm = MenuItemManager()
                mm.create(menu_item)
                mm.close()
                cm.close()
            elif operation == 'add_category':
                cm = CategoryManager()
                c = Category(request.form['category_name'])
                cm.create(c)
                cm.close()
            elif operation == 'delete_menu_item':
                print("delete : ", request.form['menu_item_name'])
                mm = MenuItemManager()
                mm.delete(request.form['menu_item_name'])
                mm.close()

    else:
        name = request.args.get('name')
    if name == 'cashier_order_list':
        om = OrderManager()
        orders = om.read_all()
        om.close()
        new_orders = []
        cooking_orders = []
        served_orders = []
        paid_orders = []
        deleted_orders = []
        if not orders:
            orders = []
        else:
            for i in orders:
                if i.status == 0:
                    new_orders.append(i)
                elif i.status == 1:
                    cooking_orders.append(i)
                elif i.status == 2:
                    served_orders.append(i)
                elif i.status == 3:
                    paid_orders.append(i)
                elif i.status == -1:
                    deleted_orders.append(i)
        print(orders)
        return render_template(name + '.html', new_orders=new_orders, cooking_orders=cooking_orders,
                               served_orders=served_orders, paid_orders=paid_orders, deleted_orders=deleted_orders)
    if name == 'receipt':
        rm = ReceiptManager()
        receipts = rm.read_all()
        receipts = sort_receipt(receipts)
        rm.close()
        new_receipts = get_news(receipts)
        paid_receipt = []
        deleted_receipt = []
        for i in receipts:
            if i.order.status == -1:
                deleted_receipt.append(i)
            elif i.order.status == 3:
                paid_receipt.append(i)
        paid_receipt = sort_receipt(paid_receipt)
        deleted_receipt = sort_receipt(deleted_receipt)
        for i in receipts:
            print(i.order.number)
        print()
        for i in new_receipts:
            print(i.order.number)
        print()
        for i in paid_receipt:
            print(i.order.number)
        return render_template('receipt.html', paid_receipt=paid_receipt, deleted_receipt=deleted_receipt,
                               new_receipts=new_receipts, receipts=receipts)
    if name == 'add_menu_item':
        cm = CategoryManager()
        category = cm.read_all()
        cm.close()
        mm = MenuItemManager()
        menu_items = mm.read_all()
        mm.close()
        return render_template(name + '.html', category=category, menu_items=menu_items)
    if name == 'tables':
        tm = TableManager()
        om = OrderManager()
        orders = om.read_all()
        orders = sorted(orders, key=lambda x: x.id, reverse=True)
        tables = tm.read_all()
        print(orders)
        table_orders = {}
        for i in tables:
            if i.status == 0:
                table_orders[i] = 'none'
            elif i.status == 1:
                for j in orders:
                    if j.table.number == i.number:
                        table_orders[i] = j
                        break
        print(table_orders)
        return render_template('tables_.html', table_orders=table_orders)
    if name == 'dashboard':
        return render_template('dashboard.html')
    return redirect(url_for('login'))
