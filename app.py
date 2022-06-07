from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify
app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)


# root of our website
@app.route('/')
def index_func():
    user_from_db = 'aRIeL'
    user_second_name_from_db = 'Katz'
    return render_template('home_page.html',
                           user_name=user_from_db)
                           # user_second_name=user_second_name_from_db)


@app.route('/about')
def about_page():
    user_info = {'name': 'Jacky', 'second_name': 'Sparrow', 'nickname': 'pirate'}
    degrees = ['BSc', 'MsD', 'PhD']
    hobbies = ('drawing', 'books', 'ships', 'chips', 'TV', 'sea')
    session['CHECK'] = 'about'
    return render_template('about_page.html',
                           user_info=user_info,
                           user_degrees=degrees,
                           hobbies=hobbies)


catalog_dict = {
    'computer': 4000,
    'mouse': 100,
    'screen': 2000,
    'keyboard': 100,
}


@app.route('/catalog')
def catalog_func():
    if 'product_name' in request.args:
        product_name = request.args['product_name']
        product_color = request.args['product_color']
        product_size = request.args['product_size']
        if product_name in catalog_dict:
            return render_template('catalog_page.html',
                                   product_name=product_name,
                                   product_price=catalog_dict[product_name],
                                   product_color=product_color,
                                   product_size=product_size)
        else:
            return render_template('catalog_page.html',
                                   message='Product not found.')
    return render_template('catalog_page.html',
                           catalog_dict=catalog_dict)

user_dict = {
    'arsenip': '1919',
    'yossi': '1234'
}


@app.route('/log_in', methods=['GET', 'POST'])
def login_func():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in user_dict:
            pas_in_dict = user_dict[username]
            if pas_in_dict == password:
                session['username'] = username
                session['logedin'] = True
                return render_template('log_in.html',
                                       message='Success',
                                       username=username)
            else:
                return render_template('log_in.html',
                                       message='Wrong password!')
        else:
            return render_template('log_in.html',
                                   message='Please sign in!')
    return render_template('log_in.html')


@app.route('/log_out')
def logout_func():
    session['logedin'] = False
    session.clear()
    return redirect(url_for('login_func'))


@app.route('/session')
def session_func():
    # print(session['CHECK'])
    return jsonify(dict(session))

# @app.route('/catalog', methods=['POST', 'PUT', 'DELETE', 'GET'])
# def catalog_func():
#     curr_user = {'firstname': "Ariel", 'lastname': "Perchik", 'wok': 'BGU', 'adress': 'Israel'}
#
#     current_method = request.method
#     if 'username' in session:
#         user_name, last_name = session['username'], session['lastname']
#     else:
#         if current_method == 'GET':
#             if 'username' in request.args:
#                 user_name = request.args['username']
#                 last_name = request.args['lastname']
#             else:
#                 user_name, last_name = '', ''
#         elif current_method == 'POST':
#             if 'username' in request.form:
#                 user_name = request.form['username']
#                 last_name = request.form['lastname']
#             else:
#                 user_name, last_name = '', ''
#         else:
#             user_name, last_name = '', ''
#         session['username'] = ''
#         session['lastname'] = ''
#     return render_template('catalog.html',
#                            curr_user=curr_user,
#                            user_name=user_name,
#                            last_name=last_name,
#                            current_method=current_method)
#
# @app.route('/log_out')
# def log_out():
#     session['username'] = ''
#     session['lastname'] = ''
#     return redirect(url_for('index'))
#
#
# @app.route('/log_in', methods=['GET', 'POST'])
# def log_in():
#     if request.method == 'GET':
#         return render_template('log_in.html')
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         session['lastname'] = request.form['lastname']
#     return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
