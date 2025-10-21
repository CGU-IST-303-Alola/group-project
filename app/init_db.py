import sqlite3
import os

base_fp = os.path.dirname(os.path.abspath(__file__))
data_fp = os.path.join(base_fp, "data/database.sql")
schema_fp = os.path.join(base_fp, "schema.sql")

os.makedirs(os.path.join(base_fp, "data"), exist_ok=True)

def database_initialize():
	connection = sqlite3.connect(data_fp)

	with open(schema_fp, "r") as schema_f:
		connection.executescript(schema_f.read())

		connection.execute("INSERT INTO USERS (USERNAME, PASSWORD, ROLE, VERIFIED) VALUES (?, ?, ?, ?)", ("patient1", "test123", "PATIENT", 1))
		connection.execute("INSERT INTO USERS (USERNAME, PASSWORD, ROLE, VERIFIED) VALUES (?, ?, ?, ?)", ("doctor1", "docpass", "PHYSICIAN", 1))
		connection.execute("INSERT INTO USERS (USERNAME, PASSWORD, ROLE, VERIFIED) VALUES (?, ?, ?, ?)", ("admin1", "adminpass", "ADMIN", 1))

		connection.commit()
		connection.close()
		print("Database Initialized")

if __name__ == "__main__":
	database_initialize()