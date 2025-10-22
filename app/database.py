import sqlite3
import os

def get_db_connection():
	connection = sqlite3.connect("data/database.db")
	connection.row_factory = sqlite3.Row
	return connection