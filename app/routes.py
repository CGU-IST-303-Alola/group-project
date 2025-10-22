from flask import session, redirect, url_for, render_template, request, flash
from database import get_db_connection, get_current_user

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

		if role == "PATIENT":
			return render_template("home_patient.html", user=user)
		elif role == "PHYSICIAN":
			return render_template("home_physician.html", user=user)
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


	