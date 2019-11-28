from studentportal import create_app

app = create_app()
app.jinja_env.auto_reload = True
app.run()
