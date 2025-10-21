from flask import Flask
from routes import routes_startup

app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"
routes_startup(app)

if __name__ == "__main__":
	app.run(debug=True)
