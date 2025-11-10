import sqlite3
import os
from app.database import get_db_connection

base_fp = os.path.dirname(os.path.abspath(__file__))
schema_fp = os.path.join(base_fp, "schema.sql")

def database_initialize(db_path=None):
	data_users = [
		("dSalaz5", "tdNU9188", "PHYSICIAN"),
		("lRoble97", "aFaQ8160", "PHYSICIAN"),
		("mChase99", "PsGt4470", "PHYSICIAN"),
		("nCarte59", "khtQ2677", "PHYSICIAN"),
		("kRice52", "MJUE7094", "PHYSICIAN"),
		("aMolin2", "xgpp5999", "ADMIN"),
		("sHowar2", "UhUv7394", "ADMIN")
	]
	data_patients = [
		("Andre", "Mitchel", 0),
		("Stephanie", "Johnson", 1)
	]
	data_appointments = [
		(0, 2, "2025-11-12 14:30:00"),
		(1, 5, "2025-11-16 11:00:00")
	]
	connection = sqlite3.connect(db_path)
	with open(schema_fp, "r") as schema_f:
		connection.executescript(schema_f.read())
		
		connection.executemany("""
			INSERT INTO USERS (USERNAME, PASSWORD, ROLE)
			VALUES (?, ?, ?)""", data_users)
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