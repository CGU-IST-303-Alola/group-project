import sqlite3
import os
from app.logger_print import print_logs

base_fp = os.path.dirname(os.path.abspath(__file__))
schema_fp = os.path.join(base_fp, "schema.sql")

@print_logs
def database_initialize(db_path=None, LOGS_STATUS=False):
	data_users = [
		("eGarri53", "password123", "PHYSICIAN"),
		("jMcdon96", "olxl885", "PHYSICIAN"),
		("cMitch50", "cWgf2896", "PHYSICIAN"),
		("dMarti56", "wojc1182", "PHYSICIAN"),
		("kMoore63", "hyKE5105", "ADMIN")
	]
	data_user_details = [
		(1, "Edward", "Garrison", "edward.garrison4248@gmail.com"),
		(2, "Joseph", "Mcdonald", "joseph.mcdonald5447@gmail.com"),
		(3, "Carrie", "Mitchell", "carrie.mitchell3039@gmail.com"),
		(4, "Dennis", "Martinez", "dennis.martinez5880@gmail.com"),
		(5, "Kathleen", "Moore", "kathleen.moore6781@gmail.com")
	]
	data_patients = [
		("Alex", "Mendoza", 0),
		("Casey", "Lang", 1),
		("Diana", "Potts", 1),
		("Susan", "Mills", 1),
		("Patrick", "Rocha", 0),
		("Jessica", "Stark", 1),
		("Latoya", "Neal", 1),
		("Randy", "Garcia", 0),
		("Brandy", "Rodriguez", 1),
		("Justin", "Hall", 0)
	]
	data_appointments = [
		(1, 1, "2025-11-12 14:30:00", "COMPLETED"),
		(2, 1, "2025-11-12 16:40:00", "COMPLETED"),
		(3, 1, "2025-11-13 20:30:00", "COMPLETED"),
		(4, 1, "2025-11-16 11:00:00", "COMPLETED"),
		(5, 1, "2025-11-19 15:00:00", "COMPLETED"),
		(1, 1, "2025-11-20 01:30:00", "SCHEDULED"),
		(2, 1, "2025-11-20 10:00:00", "SCHEDULED"),
		(3, 1, "2025-11-20 12:30:00", "SCHEDULED"),
		(4, 1, "2025-11-20 13:00:00", "SCHEDULED"),
		(5, 1, "2025-11-20 13:30:00", "SCHEDULED"),
	]
	connection = sqlite3.connect(db_path)
	with open(schema_fp, "r") as schema_f:
		connection.executescript(schema_f.read())
		
		connection.executemany("""
			INSERT INTO USERS (USERNAME, PASSWORD, ROLE)
			VALUES (?, ?, ?)""", data_users)
		connection.executemany("""
			INSERT INTO USER_DETAILS (USER_ID, NAME_FIRST, NAME_LAST, EMAIL)
			VALUES (?, ?, ?, ?)""", data_user_details)
		connection.executemany("""
			INSERT INTO PATIENTS (NAME_FIRST, NAME_LAST, SEX)
			VALUES (?, ?, ?)""", data_patients)
		connection.executemany("""
			INSERT INTO APPOINTMENTS (PATIENT_ID, PHYSICIAN_ID, TIME, STATUS)
			VALUES (?, ?, ?, ?)""", data_appointments)
		connection.commit()
		connection.close()

if __name__ == "__main__":
	database_initialize()