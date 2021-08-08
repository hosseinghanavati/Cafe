from my_flask.app_import import *
from cafe.order import *


@app.route('/')
def home():
    return render_template('landing_base_html.html')


def page_content():
    if request.method == 'GET':
        name = request.args.get('name')
    elif request.method == 'POST':
        name = request.form.get('name')
        if name == 'Contact':
            mm = MessageManager()
            m = Message(request.form['first_name'], request.form['last_name'], request.form['email'],
                        request.form['message'])
            mm.create(m)
            mm.close()

    if name == 'menu':
        category_manager = CategoryManager()
        categories = category_manager.read_all()
        menu_item_manager = MenuItemManager()
        menu_items = menu_item_manager.read_all()

        return render_template(name + '.html', menu_items=menu_items, categories=categories)
    elif name == 'order_list':
        print(name)
        table_manager = TableManager()
        tables = table_manager.read_all()

        # firstly_orders = add_orders()

        return render_template(name + '.html', orders=add_orders(), tables=tables)
    else:
        return render_template(name + '.html')


app.add_url_rule('/page_content', 'page_content', page_content, methods=['GET', 'POST'])
