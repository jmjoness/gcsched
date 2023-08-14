from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
#from flask_cors import CORS, cross_origin
# from flask_login import LoginManager

db = SQLAlchemy()
# login_manager = LoginManager()

def create_app(config_name):
	app = Flask(__name__)
	print(config_name, __name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	if app.config['SSL_REDIRECT']:
		print("use sslify")
		from flask_sslify import SSLify
		sslify = SSLify(app)

	db.init_app(app)
	# login_manager.init_app(app)
	# login_manager.login_view = 'main.login'

	#CORS(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app