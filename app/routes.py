from flask import session, redirect, url_for, render_template, request, flash
from app.database import get_db_connection, get_current_user, get_appointments_physician
from datetime import datetime, timedelta

def routes_startup(app):
	@app.route("/")
	def root():
		return redirect(url_for("home"))
	
	@app.route("/home")
	def home():
		user = get_current_user()
		if not user:
			return redirect(url_for("login"))
		
		role = user["ROLE"]

		if role == "PHYSICIAN":
			print(f"[DEBUG] Physician Home Accessed - User ID: {user["ID"]}, Username: {user["USERNAME"]}")
			
			appointments = get_appointments_physician(user["ID"])
			print(f"[DEBUG] Retrieved {len(appointments)} appointments from DB")

			now = datetime.now()
			appointments_current = []
			appointments_upcoming = []
			appointments_past = []

			for appointment in appointments:
				appointment_time = datetime.fromisoformat(appointment["TIME"])
				print(f"[DEBUG] Appointment ID ({appointment['ID']}), Time: {appointment_time}")

				if ((now - timedelta(minutes=10)) <= appointment_time <= (now + timedelta(hours=1))):
					appointments_current.append(appointment)
				elif now < appointment_time:
					appointments_upcoming.append(appointment)
				else:
					appointments_past.append(appointment)
			
			print(f"[DEBUG] Grouped appointments — Current: {len(appointments_current)}, Upcoming: {len(appointments_upcoming)}, Past: {len(appointments_past)}\n")

			return render_template(
				"home_physician.html",
				user=user, appointments_current=appointments_current,
				appointments_upcoming=appointments_upcoming,
				appointments_past=appointments_past
			)
		elif role == "ADMIN":
			return render_template("home_admin.html", user=user)
		else:
			flash("Invalid Role")
			return redirect(url_for("logout"))
	
	@app.route("/login", methods=["GET", "POST"])
	def login():
		if get_current_user():
			return redirect(url_for("home"))
		
		error=None
		if request.method == "POST":
			username = request.form.get("username")
			password = request.form.get("password")

			connection = get_db_connection()
			user = connection.execute(
				"""
				SELECT *
				FROM USERS
				WHERE USERNAME = ? AND PASSWORD = ?
				""", (username, password)
			).fetchone()
			connection.close()
			
			if user:
				session["user_id"] = user["ID"]
				return redirect(url_for("home"))
			else:
				flash("Invalid Login Credentials", "error")
				return render_template("login.html", previous_attempt=username)
		
		return render_template("login.html")
	
	@app.route("/logout")
	def logout():
		session.pop("user_id", None)
		# session.clear()
		flash("Successfully Logged Out", "info")
		return redirect(url_for("login"))

