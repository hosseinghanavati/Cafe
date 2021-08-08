from cafe.landing_html_views import *
from user.html_views import *
from cafe.panel_html_views import *

# app.add_url_rule('/', 'index', index)

app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/home', 'cashier_page_content', cashier_page_content, methods=['GET', 'POST'])

app.run('0.0.0.0')
