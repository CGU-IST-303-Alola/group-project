# Table of Contents
- [Version 1](#version-1)
	- [Initial Setup](#initial-setup)
	- [Begin Front End](#begin-front-end)
	- [Begin Routing](#begin-routing)
- [Version 2](#version-2)

# Version 1

## Initial Setup

- Create Python virtual enviroment
- Create Github Repository for version control
	- Initialize repo
	- Set branch
	- Add `.gitignore`
	- Set name and email
- Install `Flask`
- Create `run.py` for Flask App
	- Add `app` as Flask App
- Create guide.md
	- Add instructions

## Begin Front End

- Create Login Page with figma
- Create `templates` and `static` folders
- Create `portal.html`
	- Add username and password input form
	- Add submit button
	- Create `portal.css`
- Create `home.html`
	- Add welcome message
	- Add logout button

## Begin Routing

- Create `routes.py`
	- Create routing function
	- Add `/login` route handling
	- Add `/home` route handling
	- Add root redirect
- Add login functionality
	- Request username and password from input form
	- Check credentials (hardcoded)
	- Store login status in session
	- Redirect to home
- Add page restrictions
	- Check for login status in session
	- Restrict anonymous users from `/home`
	- Restrict logged-in user from `/login`

## Implement Database

- Install `Flask-SQLAlchemy`
- Create SQLAlchemy Database
	- Add `db` as `app` database connection
- Create `models.py`
	- Import `db` from `run`
	- Create `PATIENT` table
	- Create `PHYSICIAN` table
	- Create `ADMIN` table
- Create `init_db.py`
	- Create function `initialize_database`
		- Import `app`, `db`, and tables from models
		- Create tables
		- Create entries
		- Add entries to `db`
- Add database to `run.py`
	- Import and call`initialize_database`
- Add check for existing database
	- Import `os`
	- Add check for directory and file of database

## Update Routing for Database Authentication

- Modify `/login` in `routes.py`
	- Import `PATIENT`, `PHYSICIAN`, and `ADMIN` from `models.py`
	- Add a query for user
	- Check users credentials

## Test Login Credentials

- Install `Pytest`
- Create `pytests.py`
	- Import `pytest` and `run` from `app`
	- Create test client
	- Parameterize test cases
- Add and Test client with cases

# Version 2

