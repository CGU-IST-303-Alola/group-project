from flask import session, current_app
import sqlite3
import os
from datetime import datetime, timedelta, time
import random
from faker import Faker
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
	return dict(user)

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
			ORDER BY DATETIME(APPOINTMENT_TIME) ASC
			""",
			(physician_id,)
		)
		rows = cursor.fetchall()
	return [dict(row) for row in rows]

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
	return dict(user)

@print_logs
def get_appointment(appointment_id, LOGS_STATUS=False):
	appointment = None
	with get_db_connection() as connection:
		cursor = connection.cursor()
		cursor.execute(
			"""
			SELECT *
			FROM APPOINTMENTS
			WHERE ID = ?
			""",
			(appointment_id,)
		)
		appointment = cursor.fetchone()
	return dict(appointment)

@print_logs
def get_patient(patient_id, LOGS_STATUS=False):
	patient = None
	with get_db_connection() as connection:
		cursor = connection.cursor()
		cursor.execute(
			"""
			SELECT *
			FROM PATIENTS
			WHERE ID = ?
			""",
			(patient_id,)
		)
		patient = cursor.fetchone()
	return dict(patient)

@print_logs
def appointment_update(id, status, notes, LOGS_STATUS=False):
	if id is None:
		return None
	with get_db_connection() as connection:
		cursor = connection.cursor()
		cursor.execute(
			"""
			UPDATE APPOINTMENTS
			SET
				STATUS = ?,
				NOTES = ?
			WHERE ID = ?
			""",
			(status, notes, id,)
		)
		connection.commit()
	return None

@print_logs
def db_check_update(LOGS_STATUS=False):
	@print_logs
	def generate_5_appointments(date, LOGS_STATUS=False):
		appointments = []
		for i in range(5):
			patient_id = patient_ids[i]
			hour = random.randint(9, 16)
			minute = random.choice([0, 30])
			if hour == 17 and minute == 30:
				minute = 0
			appointment_time = datetime.combine(date, time(hour, minute, 0, 0)).timestamp()
			
			physician = random.choice(physician_ids)
			appointments.append((patient_id, physician, appointment_time, "SCHEDULED"))
		return appointments
	
	with get_db_connection() as connection:
		cursor = connection.cursor()
		cursor.execute(
			"""
			UPDATE APPOINTMENTS
			SET STATUS = "MISSED"
			WHERE DATE(APPOINTMENT_TIME) < DATE('now')
			AND STATUS = "SCHEDULED"
			"""
		)


		cursor.execute(
			"""
			SELECT COUNT(*)
			FROM APPOINTMENTS
			WHERE DATE(APPOINTMENT_TIME) = DATE('now')
			"""
		)
		(appointments_today,) = cursor.fetchone()

		if 0 < appointments_today:
			return
		
		appointments_new = []
		patient_ids = list(range(1,11))
		physician_ids = [1,2,3]

		today = datetime.now().date()
		tomorrow = today + timedelta(days=1)
		appointments_new.extend(generate_5_appointments(today))
		appointments_new.extend(generate_5_appointments(tomorrow))
		appointments_new.sort(key=lambda x: x[2])
		cursor.executemany(
			"""
			INSERT INTO APPOINTMENTS (PATIENT_ID, PHYSICIAN_ID, APPOINTMENT_TIME, STATUS)
			VALUES (?, ?, ?, ?)
			""",
		appointments_new)
		connection.commit()
		return
