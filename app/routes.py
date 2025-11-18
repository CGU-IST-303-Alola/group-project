from flask import session, redirect, url_for, render_template, request, flash
from datetime import datetime
from app.database import get_db_connection, get_current_user, get_user_details, get_appointments_physician
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

			data = []

			for appointment in appointments:
				row = {}
				row["ID"] = appointment["ID"]
				row["PATIENT_ID"] = appointment["PATIENT_ID"]
				row["PHYSICIAN_ID"] = appointment["PHYSICIAN_ID"]

				dt = datetime.strptime(appointment["TIME"], "%Y-%m-%d %H:%M:%S")
				row["TIME"] = f"{dt.strftime('%b %d')}, {dt.hour % 12 or 12}:{dt.strftime('%M %p')}"
				row["NAME"] = f"{appointment["NAME_FIRST"]} {appointment["NAME_LAST"]}"
				data.append(row)
			
			return render_template(
				"home_physician.html",
				user=get_user_details(user["ID"]),
				appointments=data,
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

