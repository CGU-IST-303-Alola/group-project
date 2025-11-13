# Table of Contents
- [V0.1 Initial Setup](#version-01-initial-setup)
	- [Project Setup](#begin-project-setup)
	- [Begin Front End](#begin-front-end)
	- [Begin Routing](#begin-routing)
	- [Implement Database](#implement-database)
	- [Update Routing](#update-routing-for-database-authentication)
	- [Test Login](#test-login-credentials)
- [V0.2 Refactoring](#version-02-refactoring)
	- [Refactor App](#refactor-app)
	- [Refactor Database](#refactor-database)
	- [Refactor Routing](#refactor-routing)
	- [Refactor Pytests](#refactor-pytests)
	- [Redesign Login Portal](#redesign-login-page)

# Version 0.1 Initial Setup

## Begin Project Setup

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
	- Create function `initialize_database()`
		- Import `app`, `db`, and tables from models
		- Create tables
		- Create entries
		- Add entries to `db`
- Add database to `run.py`
	- Import and call`initialize_database()`
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

# Version 0.2 Refactoring

## Refactor App

- Remove pip installations
- Install `Flask` and `pytest`
- Create `requirements.txt`
	- Run `pip freeze` to save imports
- Create `app/` package
	- Move `run.py` outside of `app`
	- Update all module imports with `app.`
	- Create `__init__.py`
		- Import `os`, `app.init_db`, `Flask`, and `app.routes`
		- Create function `create_app()`
			- Create Flask `app`
			- Check for file of database
			- Call `database_initialize()` from `app.init_db`
			- Add Route Handling with `routes_startup()` from `app.routes`
- Update `run.py`
	- Import and Call `create_app()`
	- Run `app` in main
- Update file handling
	- Replace hardcoded paths using `os.path`
- Update `guide.md`
	- Modify directory for running Flask app

## Refactor Database

- Remove `models.py`
- Create `schema.sql`
	- Create `USERS` Table
		- Add `ID`, `USERNAME`, `PASSWORD`, and `ROLE`
		- Add role constraint to `ROLE`
	- Create `PROFILES` Table
		- Add User details and Foreign Key to `USERS`
- Refactor `init_db.py`
	- Import `sqlite3`
	- Modify `database_initialize()`
		- Check for database existence
		- Connect to `db_path`
		- Read and Execute `schema.sql`
- Create `database.py`
	- Import `session` and `current_app` from `Flask`
	- Import `sqlite3`
	- Create function to get connection
		- Check for database existence
		- Connect to `db_path`
	- Add `db_path` to config across files
	- Create function `get_db_connection()` to get user from `USERS`
		- Get `user_id` from session
		- Connect and Search for user with `user_id`

## Refactor Routing

- Modify `routes.py`
	- Replace `models` and `run` imports with `app.database` functions
	- Add necessary `Flask` imports
	- Create `routes_startup()`
		- Move routes into function
		- Update `/login` route
			- Check login status
			- Check Input from form
				- Request Credentials from form
				- Connect to database
				- Authenticate Credentials
				- Handle Credentials
				- Add `user_id` to session
		- Add `/home` route
			- Check login status
				- Get User
			- Render User's `ROLE` as Page
				- Pass user as argument
		- Add `/logout` route
			- Remove `user_id` from session

## Refactor Pytests

- Delete `pytests.py`
- Create `tests/` directory outside of `app/`
- Create and Set up `conftest.py`
- Create `test_protected_routes.py`
	- Import `pytest` and `create_app()`
	- Create `client()`
		- Add `pytest.fixture`
		- Add `create_app()`
			- Set `app` to `TESTING`
	- Create `test_protected_routes()`
		- Parametrize routes
		- Test redirects for unauthenticated users
- Create `test_login.py`
	- Import `pytest`, `create_app()` and necessary libraries
	- Create `client()`
		- Add `pytest.fixture`
		- Create tempfile
		- Create `sqlite3` connection to tempfile
		- Read and Execute `schema.sql`
		- Create Test Database
		- Add `create_app()`
			- Set `app` to `TESTING`
			- Set `db_path` to tempfile
	- Create `test_login_page()`
		- Test response of `/login`
	- Create `test_login_success()`
		- Parametrize correct usernames and passwords
		- Test Correct usernames and passwords
	- Create `test_login_invalid()`
		- Test Incorrect username and password
	- Create `test_logout()`
		- Login with correct credentials
		- Test `/logout` response


## Redesign Login Page

- Design UI in Figma
- Create `templates/login.html`
	- Create Top Section
	- Create Bottom Section
		- Create Sign In Container
			- Show Flash Message
				- Get Flash Messages
				- Display Info or Error Message
			- Create Username Container
				- Add Username Field
			- Create Password Container
				- Add Password Field
			- Create Log In Button
				- Add Submit Button
- Create `static/css/login.css`
	- Add Styling

# Version 0.3 Adding Apointments

## Update User Tables

- Remove `Patients` as User
- Remove `VERIFIED` from `USERS`
- Create `PATIENTS` Table
	- Add `ID`, `NAME_FIRST`, `NAME_LAST`, `EMAIL`, `DOB`, `SEX`, `PHONE_NUMBER`, `ADDRESS`, `MEDICAL_RECORD_NUMBER`
- Update `Profiles` Table
	- Rename to `USER_DETAILS`
	- Add `ID` (PK, FK), `NAME_FIRST`, `NAME_LAST`, `EMAIL`, `DOB`, `PHONE_NUMBER`, `ADDRESS`
- Update code to updates

## Create Appointments

- Create `APPOINTMENTS` Table
	- Add `ID` (PK), `PATIENT_ID` (FK), `PHYSICIAN_ID` (FK), `TIME`, `STATUS`
