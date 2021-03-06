import random

from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify
import mysql.connector
import time
import requests

import asyncio
import aiohttp

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


# ------------------------------------------------- #
# ------------------------------------------------- #


@app.route('/fetch_fe')
def fetch_fe_func():
    return render_template('fetch_frontend.html')


async def fetch_url(client_session, url):
    """Fetch the specified URL using the aiohttp session specified."""
    # response = await session.get(url)
    async with client_session.get(url, ssl=False) as resp:
        response = await resp.json()
        return response


async def get_all_urls(from_val, until_val):
    async with aiohttp.ClientSession(trust_env=True) as client_session:
        tasks = []
        for i in range(from_val, until_val):
            url = f'https://pokeapi.co/api/v2/pokemon/{i}'
            task = asyncio.create_task(fetch_url(client_session, url))
            tasks.append(task)
        data = await asyncio.gather(*tasks)
    return data


def save_users_to_session(pockemons):
    users_list_to_save = []
    for pockemon in pockemons:
        pockemons_dict = {
            'sprites': {
                'front_default': pockemon['sprites']['front_default']
            },
            'name': pockemon['name'],
            'height': pockemon['height'],
            'weight': pockemon['weight'],
        }
        users_list_to_save.append(pockemons_dict)
    session['pockemons'] = users_list_to_save


def get_pockemons_sync(from_val, until_val):
    pockemons = []
    for i in range(from_val, until_val):
        res = requests.get(f'https://pokeapi.co/api/v2/pokemon/{i}')
        print(res)
        pockemons.append(res.json())
    return pockemons


# @app.route('/fetch_be')
# def fetch_be_func():
#     if 'type' in request.args:
#         num = int(request.args['num'])
#         random_start = random.randint(1, 30)
#         random_end = random_start + num
#         session['num'] = num
#         pockemons = get_pockemons_sync(random_start, random_end)
#         save_users_to_session(pockemons)
#     else:
#         session.clear()
#     return render_template('fetch_backend.html')

@app.route('/fetch_be')
def fetch_be_func():
    if 'type' in request.args:
        start_time = time.time()
        # from_val, until_val = int(request.args['from']), int(request.args['until'])
        num = int(request.args['num'])
        rand_start = random.randint(1, 30)
        rand_end = rand_start + num
        session['num'] = num
        pockemons = []

        # SYNC
        if request.args['type'] == 'sync':
            pockemons = get_pockemons_sync(rand_start, rand_end)

        # ASYNC
        if request.args['type'] == 'async':
            pockemons = asyncio.run(get_all_urls(rand_start, rand_end))
            print('run')

        end_time = time.time()
        time_to_finish = f'{end_time - start_time: .2f} seconds'
        session[f'{request.args["type"]}_time'] = time_to_finish
        session[f'{request.args["type"]}_num'] = session['num']

        save_users_to_session(pockemons)
    else:
        session.clear()
    return render_template('fetch_backend.html')


@app.route('/get_json')
def json_func():
    sample_dic = {
        'name': 'Yossi',
        'age': 25,
        'hobbies': ['swimming', 'art', 'sports']
    }
    return jsonify(sample_dic)


# ------------------------------------------------- #
# --------------- URL PARAMETERS ------------------ #
# ------------------------------------------------- #
@app.route('/profile', defaults={'user_id': -1})
@app.route('/profile/<int:user_id>')
def profile_func(user_id):
    # DB
    response = {}

    if user_id == -1:
        response['message'] = 'No user inserted'

    else:

        query = "SELECT * FROM users WHERE id='%s';" % user_id
        query_result = interact_db(query=query, query_type='fetch')
        if len(query_result) != 0:
            response = query_result[0]

    response = jsonify(response)
    return response


@app.route('/get_users', defaults={'user_id': -1})
@app.route('/get_users/<user_id>')
def get_user(user_id):
    if user_id == -1:
        query = f'select * from users'
        users_list = interact_db(query, query_type='fetch')
        return_list = []
        for user in users_list:
            user_dict = {
                'name': user.name,
                'email': user.email,
                'create_date': user.create_date
            }
            return_list.append(user_dict)
        return jsonify(return_list)

    query = f'select * from users where id={user_id}'
    users_list = interact_db(query, query_type='fetch')

    if len(users_list) == 0:
        return_dict = {
            'message': 'user not found'
        }
    else:
        user_list = users_list[0]
        return_dict = {
            'name': user_list.name,
            'email': user_list.email,
            'create_date': user_list.create_date
        }
    return jsonify(return_dict)


if __name__ == '__main__':
    app.run(debug=True)
