import pytest
import os
import tempfile
import sqlite3
from app import create_app

@pytest.fixture
def client():
	db_dir, db_path = tempfile.mkstemp(suffix=".db")
	
	conn = sqlite3.connect(db_path)
	with open("app/schema.sql", "r") as f:
		conn.executescript(f.read())
	
	conn.execute("""
		INSERT INTO USERS (USERNAME, PASSWORD, ROLE, VERIFIED)
		VALUES
		("testpatient", "testpass123", "PATIENT", 1),
		("testdoctor", "testpass456", "PHYSICIAN", 1),
		("testadmin", "testpass789", "ADMIN", 1);
	""")
	conn.commit()
	conn.close()

	app = create_app(config={"TESTING": True, "db_path": db_path})

	with app.test_client() as client:
		yield client
	
	os.close(db_dir)
	os.unlink(db_path)

def test_login_page(client):
	response = client.get("/login")
	assert response.status_code == 200

@pytest.mark.parametrize("username, password", [
	("testpatient", "testpass123"),
	("testdoctor", "testpass456"),
	("testadmin", "testpass789"),
])
def test_login_success(client, username, password):
	response = client.post("/login", data={
		"username": username,
		"password": password
	}, follow_redirects=True)
	
	assert response.status_code == 200

def test_login_invalid(client):
	response = client.post("/login", data={
		"username": "wronguser",
		"password": "wrongpassword"
	}, follow_redirects=True)
	
	assert response.status_code == 200
	assert b"Invalid Login Credentials" in response.data

def test_logout(client):
	client.post("/login", data={
		"username": "testpatient",
		"password": "testpass123"
	})
	
	response = client.get("/logout", follow_redirects=True)
	assert response.status_code == 200
	assert b"Successfully Logged Out" in response.data
