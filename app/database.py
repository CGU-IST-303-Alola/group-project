from flask import session
import sqlite3

def get_db_connection():
	connection = sqlite3.connect("data/database.db")
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