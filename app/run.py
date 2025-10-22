import os
from init_db import database_initialize
from flask import Flask
from routes import routes_startup

if not os.path.exists("data/database.db"):
	database_initialize()

app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"

routes_startup(app)

if __name__ == "__main__":
	app.run(debug=True)
