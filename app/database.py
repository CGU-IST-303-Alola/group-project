from flask import session, current_app
import sqlite3
import os

def get_db_connection():
	db_path = current_app.config.get("db_path")

	if not db_path:
		base_fp = os.path.dirname(os.path.abspath(__file__))
		db_path = os.path.join(base_fp, "data", "database.db")
	
	connection = sqlite3.connect(db_path)
	connection.row_factory = sqlite3.Row
	return connection

def get_current_user():
	user_id = session.get("user_id")
	if not user_id:
		return None
	connection = get_db_connection()
	user = connection.execute("SELECT * FROM USERS WHERE ID = ?", (user_id)).fetchone()
	connection.close()
	return user