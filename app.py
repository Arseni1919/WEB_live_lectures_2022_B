from flask import Flask, redirect
from flask import url_for

app = Flask(__name__)


# comment
@app.route('/home_page')
def hello_world():
    var = foo()

    return f'Welcome to HOME Page, {var}'


def foo():
    return 'abc'


@app.route('/about')
def about_page():
    # return 'Welcome to about Page'
    # DB actions
    foo()
    return redirect(url_for('hello_world'))


if __name__ == '__main__':
    app.run(debug=True)
