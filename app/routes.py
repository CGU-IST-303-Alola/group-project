from flask import session, redirect, url_for, render_template, request, flash
from database import get_db_connection

def routes_startup(app):
	@app.route("/")
	def root():
		if session.get("logged_in") is not True:
			return redirect(url_for("login"))
		return render_template("home.html")
	
	@app.route("/home")
	def home():
		return redirect(url_for("root"))
	
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
				session["role"] = user.get("ROLE")
				return redirect(url_for("home"))
			else:
				flash("Invalid Credentials")
		
		return render_template("login.html")
	
	@app.route("/logout")
	def logout():
		session.pop("logged_in", None)
		flash("You have been logged out.")
		return redirect(url_for("login"))


	