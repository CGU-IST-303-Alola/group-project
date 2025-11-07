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
			INSERT INTO USERS (USERNAME, PASSWORD, ROLE)
			VALUES 
			("dSalaz5", "tdNU9188", "PHYSICIAN"),
			("lRoble97", "aFaQ8160", "PHYSICIAN"),
			("mChase99", "PsGt4470", "PHYSICIAN"),
			("nCarte59", "khtQ2677", "PHYSICIAN"),
			("kRice52", "MJUE7094", "PHYSICIAN"),
			("aMolin2", "xgpp5999", "ADMIN"),
			("sHowar2", "UhUv7394", "ADMIN");
			""")

		connection.commit()
		connection.close()

if __name__ == "__main__":
	database_initialize()