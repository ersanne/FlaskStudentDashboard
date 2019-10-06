from flask import Flask, render_template

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404


@app.route('/')
def hello_world():
    return render_template('layout.html'), 200


@app.route("/login")
def login():
    return render_template('login.html'), 200


@app.route("/signup")
def signup():
    return render_template('signup.html'), 200


@app.route("/feed")
def feed():
    return render_template('feed.html'), 200


@app.route("/profile")
def profile():
    return render_template('profile.html'), 200


@app.route("/calender")
def calender():
    return render_template('calender.html'), 200


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
