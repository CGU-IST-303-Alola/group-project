from flask import Flask
import os
from app.init_db import database_initialize
from app.database import db_check_update
from app.routes import routes_startup
from app.logger_print import print_logs

@print_logs
def create_app(config=None, LOGS_STATUS=False):
	app = Flask(__name__)
	app.config["SECRET_KEY"] = "super secret key"
	# app.config["SECRET_KEY"] = os.urandom(24)

	if config:
		app.config.update(config)

	if "db_path" not in app.config:
		app.config["db_path"] = os.path.join(os.path.dirname(__file__), "data", "database.db")
	
	if not os.path.exists(app.config["db_path"]):
		os.makedirs(os.path.dirname(app.config["db_path"]), exist_ok=True)
		database_initialize(app.config["db_path"])
	with app.app_context():
		db_check_update()
	routes_startup(app)
	return app