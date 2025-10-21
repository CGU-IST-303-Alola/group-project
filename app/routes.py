import sqlite3
from flask import session, redirect, url_for, render_template, request, flash


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

			if username != "admin" or password != "admin":
				error = "Invalid Credentials. Please Try Again"
			else:
				session["logged_in"] = True
				return redirect(url_for("home"))
		return render_template("login.html", error=error)
	
	@app.route("/logout")
	def logout():
		session.pop("logged_in", None)
		flash("You have been logged out.")
		return redirect(url_for("login"))


	