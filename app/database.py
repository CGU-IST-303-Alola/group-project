from flask import session
import sqlite3
import os

def get_db_connection():
	base_fp = os.path.dirname(os.path.abspath(__file__))
	data_fp = os.path.join(base_fp, "data", "database.db")
	
	connection = sqlite3.connect(data_fp)
	connection.row_factory = sqlite3.Row
	return connection

def get_current_user():
	user_id = session.get("user_id")
	if not user_id:
		return None
	connection = get_db_connection()
	user = connection.execute("SELECT * FROM USERS WHERE ID = ?", (user_id,)).fetchone()
	connection.close()
	return user