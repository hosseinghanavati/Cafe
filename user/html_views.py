from my_flask.app_import import *
from user.models import *
from user.managers import *
from datetime import timedelta


def login():
    if request.method == 'GET':
        if request.cookies:
            if request.cookies['phone'] and request.cookies['pass']:
                user_manager = UserManager()
                if user_manager.read(request.cookies['phone'], request.cookies['pass']):
                    user_manager.close()
                    return render_template('cashier_base_html.html')
                else:
                    user_manager.close()

        return render_template('login.html')

    else:
        info = request.form
        user_manager = UserManager()
        if user_manager.read(info['phone'], info['pass']):
            user_manager.close()
            resp = Response(render_template('cashier_base_html.html'))
            resp.set_cookie('phone', info['phone'], max_age=timedelta(minutes=10))
            resp.set_cookie('pass', info['pass'], max_age=timedelta(minutes=10))
            return resp
        else:
            user_manager.close()
            return render_template('login.html')
