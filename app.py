from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify
import mysql.connector

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


# ------------------------------------------------- #
# ------------- DATABASE CONNECTION --------------- #
# ------------------------------------------------- #
def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root1234',
                                         database='myflaskappdb')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)
    #

    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value


# query = "INSERT INTO try_table_1(name) VALUES ('try_name_1')"
# interact_db(query=query, query_type='commit')
#
# query = "select * from try_table_1"
# query_result = interact_db(query=query, query_type='fetch')
# print(query_result)
# ------------------------------------------------- #
# ------------------------------------------------- #


# ------------------------------------------------- #
# ------------------- SELECT ---------------------- #
# ------------------------------------------------- #
@app.route('/users')
def users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('users.html', users=users_list)
# ------------------------------------------------- #
# ------------------------------------------------- #


# ------------------------------------------------- #
# -------------------- INSERT --------------------- #
# ------------------------------------------------- #
@app.route('/insert_user', methods=['POST'])
def insert_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    print(f'{name} {email} {password}')
    query = "INSERT INTO users(name, email, password) VALUES ('%s', '%s', '%s')" % (name, email, password)
    interact_db(query=query, query_type='commit')
    return redirect('/users')


# @app.route('/insert_user', methods=['GET', 'POST'])
# def insert_user():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         # recheck
#         query = "INSERT INTO users(name, email, password) VALUES ('%s', '%s', '%s')" % (name, email, password)
#         interact_db(query=query, query_type='commit')
#         return redirect('/users')
#     return render_template('insert_user.html', req_method=request.method)


# ------------------------------------------------- #
# ------------------------------------------------- #


# ------------------------------------------------- #
# -------------------- DELETE --------------------- #
# ------------------------------------------------- #
@app.route('/delete_user', methods=['POST'])
def delete_user_func():
    user_id = request.form['user_id']
    query = "DELETE FROM users WHERE id='%s';" % user_id
    # print(query)
    interact_db(query, query_type='commit')
    return redirect('/users')


# @app.route('/delete_user', methods=['POST'])
# def delete_user():
#     user_id = request.form['id']
#     query = "DELETE FROM users WHERE id='%s';" % user_id
#     interact_db(query, query_type='commit')
#     return redirect('/users')


# ------------------------------------------------- #
# ------------------------------------------------- #


if __name__ == '__main__':
    app.run(debug=True)
