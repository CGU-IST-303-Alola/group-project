import os
from app.init_db import database_initialize
from flask import Flask
from app.routes import routes_startup

def create_app():
	app = Flask(__name__)
	app.config["SECRET_KEY"] = "your secret key"

	if not os.path.exists(os.path.join(os.path.dirname(__file__), "data", "database.db")):
		database_initialize()
	
	routes_startup(app)
	return app