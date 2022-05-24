from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template

app = Flask(__name__)


# @app.route('/')
# def index_func():
#     return render_template('index.html')


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
    return render_template('about_page.html',
                           user_info=user_info,
                           user_degrees=degrees,
                           hobbies=hobbies)


@app.route('/catalog')
def catalog_func():
    return render_template('catalog_page.html')




if __name__ == '__main__':
    app.run(debug=True)
