from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('layout.html'), 200


@app.route("/login")
def login():
    return render_template('auth/login.html'), 200


@app.route("/signup")
def signup():
    return render_template('auth/signup.html'), 200


if __name__ == '__main__':
    app.run()
