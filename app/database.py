from flask import session, current_app
import sqlite3
import os
from app.logger_print import print_logs

@print_logs
def get_db_connection(LOGS_STATUS=False):
	db_path = current_app.config.get("db_path")
	if not db_path:
		base_fp = os.path.dirname(os.path.abspath(__file__))
		db_path = os.path.join(base_fp, "data", "database.db")
	connection = sqlite3.connect(db_path)
	connection.row_factory = sqlite3.Row
	
	return connection

@print_logs
def get_current_user(LOGS_STATUS=False):
	user_id = session.get("user_id")
	if not user_id:
		return None
	connection = get_db_connection()
	user = connection.execute("SELECT * FROM USERS WHERE ID = ?", (user_id,)).fetchone()
	connection.close()
	return user

@print_logs
def get_appointments_physician(physician_id, LOGS_STATUS=False):
	connection = get_db_connection()
	appointments = connection.execute(
		"""
		SELECT *
		FROM APPOINTMENTS
		WHERE PHYSICIAN_ID = ?
		ORDER BY DATETIME(TIME) ASC
		""",
	(physician_id,),).fetchall()
	connection.close()
	return appointments

@print_logs
def get_info_patient(patient_id, LOGS_STATUS=False):
	patient = None
	return patient