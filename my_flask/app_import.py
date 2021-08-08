from flask import Flask, request, render_template, redirect, url_for, Response

from cafe.managers import *
from cafe.models import *

app = Flask(__name__, template_folder='templates', static_folder='static')

# @app.route('/')
# def home():
#     return render_template('landing_base_html.html')
#
#
# def page_content():
#     if request.method == 'GET':
#         name = request.args.get('name')
#     elif request.method == 'POST':
#         name = request.form.get('name')
#         if name == 'Contact':
#             mm = MessageManager()
#             m = Message(request.form['first_name'], request.form['last_name'], request.form['email'],
#                         request.form['message'])
#             mm.create(m)
#             mm.close()
#     return render_template(name + '.html')
#
#
# app.add_url_rule('/page_content', 'page_content', page_content, methods=['GET', 'POST'])
# app.run()
