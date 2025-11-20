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
	
	with get_db_connection() as connection:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM USERS WHERE ID = ?", (user_id,))
		user = cursor.fetchone()
	return user

@print_logs
def get_appointments_physician(physician_id, LOGS_STATUS=False):
	with get_db_connection() as connection:
		cursor = connection.cursor()
		cursor.execute(
			"""
			SELECT 
				APPOINTMENTS.*,
				PATIENTS.NAME_FIRST,
				PATIENTS.NAME_LAST
			FROM APPOINTMENTS
			JOIN PATIENTS
			ON APPOINTMENTS.PATIENT_ID = PATIENTS.ID
			WHERE PHYSICIAN_ID = ?
			ORDER BY DATETIME(TIME) ASC
			""",
			(physician_id,)
		)
		rows = cursor.fetchall()
	return rows

@print_logs
def get_user_details(user_id, LOGS_STATUS=False):
	if user_id == None:
		if LOGS_STATUS: print("[LOG] No User Recieved")
		return None
	
	with get_db_connection() as connection:
		cursor = connection.cursor()
		cursor.execute(
			"""
			SELECT
				USERS.ID, USERS.USERNAME, USERS.ROLE,
				USER_DETAILS.NAME_FIRST, USER_DETAILS.NAME_LAST
			FROM USERS
			LEFT JOIN USER_DETAILS
			ON USERS.ID = USER_DETAILS.USER_ID
			WHERE USERS.ID = ?
			""",
			(user_id,)
		)
		user = cursor.fetchone()
	
	if LOGS_STATUS: 
		print("[LOG] User Details Recieved")
		# print(f"[LOG] {user['NAME_FIRST']}")
	return user
