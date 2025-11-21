import pytest
import os
import tempfile
import sqlite3
from app import create_app
from datetime import datetime, timedelta, time
import random
from faker import Faker

@pytest.fixture
def client():
	db_fd, db_path = tempfile.mkstemp(suffix=".db")
	
	conn = sqlite3.connect(db_path)
	with open("app/schema.sql", "r") as f:
		conn.executescript(f.read())
	
		conn.execute(
			"""
			INSERT INTO USERS (USERNAME, PASSWORD, ROLE)
			VALUES
			("testdoctor", "testpass456", "PHYSICIAN"),
			("testadmin", "testpass789", "ADMIN");
			"""
		)
		conn.execute(
			"""
			INSERT INTO PATIENTS (NAME_FIRST, NAME_LAST, SEX)
			VALUES
			("Alex", "Mendoza", 0);
			"""
		)
		
		hour = random.randint(9, 16)
		minute = random.choice([0, 30])
		if hour == 17 and minute == 30:
			minute = 0
		appointment_time = datetime.combine(datetime.now().date() + timedelta(days=1), time(hour, minute, 0, 0)).timestamp()

		conn.execute(
			"""
			INSERT INTO APPOINTMENTS (PATIENT_ID, PHYSICIAN_ID, APPOINTMENT_TIME, STATUS)
			VALUES (0, 0, ?, "SCHEDULED");
			""",
			(appointment_time,)
		)

		conn.commit()
		conn.close()

	app = create_app(config={"TESTING": True, "db_path": db_path})

	with app.test_client() as client:
		yield client

def test_login_page(client):
	response = client.get("/login")
	assert response.status_code == 200

@pytest.mark.parametrize("username, password", [
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
		"username": "testdoctor",
		"password": "testpass456"
	})
	
	response = client.get("/logout", follow_redirects=True)
	assert response.status_code == 200
	assert b"Successfully Logged Out" in response.data

def test_appointment_route_requires_login(client):
	response = client.get("/appointments/1", follow_redirects=False)
	assert response.status_code == 302
	assert "/login" in response.headers["Location"]


def test_appointment_route_requires_physician(client):
	client.post("/login", data={
		"username": "testadmin",
		"password": "testpass789"
	})

	response = client.get("/appointments/1", follow_redirects=True)
	assert response.status_code == 200
	assert b"Access Denied" in response.data or b"Home" in response.data


def test_appointment_route_requires_physician(client):
	client.post("/login", data={
		"username": "testadmin",
		"password": "testpass789"
	})

	response = client.get("/appointments/1", follow_redirects=True)

	assert response.status_code == 200
	assert b"Home" in response.data or b"home" in response.data



def test_appointment_end_saves_notes(client):
	client.post("/login", data={
		"username": "testdoctor",
		"password": "testpass456"
	})

	test_notes = "Patient is recovering well."

	response = client.post(
		"/appointment/1/end",
		data={"notes": test_notes},
		follow_redirects=True
	)

	assert response.status_code == 200

	db_path = client.application.config["db_path"]
	conn = sqlite3.connect(db_path)
	row = conn.execute(
		"SELECT STATUS, NOTES FROM APPOINTMENTS WHERE ID = 1"
	).fetchone()
	conn.close()

	assert row is not None
	assert row[0] == "COMPLETED"
	assert row[1] == test_notes
