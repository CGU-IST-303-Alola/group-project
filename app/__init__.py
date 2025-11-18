from flask import Flask
import os
from app.init_db import database_initialize
from app.routes import routes_startup

def create_app(config=None):
	app = Flask(__name__)
	app.config["SECRET_KEY"] = "your secret key"

	if config:
		app.config.update(config)

	if "db_path" not in app.config:
		app.config["db_path"] = os.path.join(os.path.dirname(__file__), "data", "database.db")
	
	if not os.path.exists(app.config["db_path"]):
		os.makedirs(os.path.dirname(app.config["db_path"]), exist_ok=True)
		database_initialize(app.config["db_path"])

	routes_startup(app)
	return app