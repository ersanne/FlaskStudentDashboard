from studentportal import create_app
from instance import Config

app = create_app(Config)
app.jinja_env.auto_reload = True
app.run(debug=True)
