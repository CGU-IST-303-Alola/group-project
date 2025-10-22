import sqlite3
import os

base_fp = os.path.dirname(os.path.abspath(__file__))
schema_fp = os.path.join(base_fp, "schema.sql")

def database_initialize(db_path=None):
	if db_path is None:
		db_path = os.path.join(base_fp, "data", "database.db")
	os.makedirs(os.path.join(base_fp, "data"), exist_ok=True)
	connection = sqlite3.connect(db_path)

	with open(schema_fp, "r") as schema_f:
		connection.executescript(schema_f.read())

		connection.execute("""
			INSERT INTO USERS (USERNAME, PASSWORD, ROLE, VERIFIED)
			VALUES
			("patient1", "patientpassword", "PATIENT", 1),
			("physician1", "physicianpassword", "PHYSICIAN", 1),
			("admin1", "adminpassword", "ADMIN", 1);
			""")

		connection.commit()
		connection.close()
		print("Database Initialized at {db_path}")

if __name__ == "__main__":
	database_initialize()