from flask import session, redirect, url_for, render_template, request, flash
from datetime import datetime, timedelta
from app.database import get_db_connection, get_current_user, get_appointments_physician
from app.logger_print import print_logs

def routes_startup(app):
	@app.route("/")
	@print_logs
	def root(LOGS_STATUS=False):
		return redirect(url_for("home"))
	
	@app.route("/home")
	@print_logs
	def home(LOGS_STATUS=False):
		user = get_current_user()
		if not user:
			return redirect(url_for("login"))
		
		role = user["ROLE"]

		if role == "PHYSICIAN":
			print(f"[LOG] Physician Home Accessed - User ID: {user["ID"]}, Username: {user["USERNAME"]}")
			
			appointments = get_appointments_physician(user["ID"])
			print(f"[LOG] Retrieved {len(appointments)} appointments")

			now = datetime.now()
			appointments_current = []
			appointments_upcoming = []
			appointments_past = []

			for appointment in appointments:
				appointment_time = datetime.fromisoformat(appointment["TIME"])

				if ((now - timedelta(minutes=10)) <= appointment_time <= (now + timedelta(hours=1))):
					appointments_current.append(appointment)
				elif now < appointment_time:
					appointments_upcoming.append(appointment)
				else:
					appointments_past.append(appointment)
			
			print(f"[LOG] Grouped appointments — Current: {len(appointments_current)}, Upcoming: {len(appointments_upcoming)}, Past: {len(appointments_past)}")

			patient = None
			
			return render_template(
				"home_physician.html",
				user=user,
				appointments_current=appointments_current,
				appointments_upcoming=appointments_upcoming,
				appointments_past=appointments_past,
				patient=patient
			)
		elif role == "ADMIN":
			return render_template("home_admin.html", user=user)
		else:
			flash("Invalid Role")
			return redirect(url_for("logout"))
	
	@app.route("/login", methods=["GET", "POST"])
	@print_logs
	def login(LOGS_STATUS=False):
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
	@print_logs
	def logout(LOGS_STATUS=False):
		session.pop("user_id", None)
		# session.clear()
		flash("Successfully Logged Out", "info")
		return redirect(url_for("login"))

