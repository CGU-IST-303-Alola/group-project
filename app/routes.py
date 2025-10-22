from flask import session, redirect, url_for, render_template, request, flash
from database import get_db_connection

def routes_startup(app):
	@app.route("/")
	def root():
		return redirect(url_for("home"))
	
	@app.route("/home")
	def home():
		if session.get("logged_in") is not True:
			return redirect(url_for("login"))
		
		role = session.get("role")

		if role == "PATIENT":
			return render_template("home_patient.html")
		elif role == "PHYSICIAN":
			return render_template("home_physician.html")
		elif role == "ADMIN":
			return render_template("home_admin.html")
		else:
			flash("Invalid Role")
			return redirect(url_for("logout"))
	
	@app.route("/login", methods=["GET", "POST"])
	def login():
		if session.get("logged_in") is True:
			return redirect(url_for("home"))
		
		error=None
		if request.method == "POST":
			username = request.form.get("user_id")
			password = request.form.get("user_password")

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
				session["logged_in"] = True
				session["role"] = user["ROLE"]
				return redirect(url_for("home"))
			else:
				flash("Invalid Credentials")
		
		return render_template("login.html")
	
	@app.route("/logout")
	def logout():
		session.pop("logged_in", None)
		session.pop("role", None)
		flash("You have been logged out.")
		return redirect(url_for("login"))


	