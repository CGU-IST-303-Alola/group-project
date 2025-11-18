import sqlite3
import os
from app.logger_print import print_logs

base_fp = os.path.dirname(os.path.abspath(__file__))
schema_fp = os.path.join(base_fp, "schema.sql")

@print_logs
def database_initialize(db_path=None, LOGS_STATUS=False):
	data_users = [
		("eGarri53", "LohD2986", "PHYSICIAN"),
		("jMcdon96", "olxl885", "PHYSICIAN"),
		("cMitch50", "cWgf2896", "PHYSICIAN"),
		("mBerry32", "oAeT4592", "PHYSICIAN"),
		("rWilli72", "vbSe9237", "PHYSICIAN"),
		("sWalke55", "iqWz1405", "PHYSICIAN"),
		("dMarti56", "wojc1182", "PHYSICIAN"),
		("kMoore63", "hyKE5105", "ADMIN"),
		("cWilli71", "pmVY8763", "ADMIN"),
		("bFishe73", "EzUO1689", "ADMIN")
	]
	data_user_details = [
		(1, "Edward", "Garrison", "edward.garrison4248@gmail.com"),
		(2, "Joseph", "Mcdonald", "joseph.mcdonald5447@gmail.com"),
		(3, "Carrie", "Mitchell", "carrie.mitchell3039@gmail.com"),
		(4, "Miranda", "Berry", "miranda.berry9274@gmail.com"),
		(5, "Reginald", "Williamson", "reginald.williamson6166@gmail.com"),
		(6, "Sarah", "Walker", "sarah.walker6568@gmail.com"),
		(7, "Dennis", "Martinez", "dennis.martinez5880@gmail.com"),
		(8, "Kathleen", "Moore", "kathleen.moore6781@gmail.com"),
		(9, "Christopher", "Williams", "christopher.williams2549@gmail.com"),
		(10, "Brandon", "Fisher", "brandon.fisher4182@gmail.com")
	]
	data_patients = [
		("Andre", "Mitchel", 0),
		("Stephanie", "Johnson", 1)
	]
	data_appointments = [
		(1, 1, "2025-11-12 14:30:00"),
		(2, 1, "2025-11-12 16:40:00"),
		(1, 1, "2025-11-13 20:30:00"),
		(2, 1, "2025-11-16 11:00:00"),
		(2, 1, "2025-11-19 15:30:00")
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
			INSERT INTO APPOINTMENTS (PATIENT_ID, PHYSICIAN_ID, TIME)
			VALUES (?, ?, ?)""", data_appointments)
		connection.commit()
		connection.close()

if __name__ == "__main__":
	database_initialize()