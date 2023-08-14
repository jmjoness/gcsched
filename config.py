import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'matsu'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
	DEBUG = False
	SSL_REDIRECT = False

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	# on desktop
	MYSQL = {
	'user': 'trees',
	'pw': 'trees',
	'db': 'gcsched',
	'host': 'localhost',
	'port': '3306'
	}
	SQLALCHEMY_DATABASE_URI = 'mysql://%(user)s:%(pw)s@%(host)s/%(db)s' % MYSQL
	DEBUG = True

class LinuxConfig(Config):
	# on HostWinds
	MYSQL = {
		'user':'smarter',
		'pw':'SmartPlot#33',
		'db':'plane',
		'host':'localhost',
		'port':'3306'
		}
	SQLALCHEMY_DATABASE_URI = 'mysql://%(user)s:%(pw)s@%(host)s/%(db)s' % MYSQL

class ProductionConfig(Config):
	# on pythonanywhere
	MYSQL = {
	   'user': 'treemon',
	   'pw': 'matsubayashi',
	   'db': 'treemon$trees',
	   'host': 'treemon.mysql.pythonanywhere-services.com',
	   'port': '5432'
	   }
	SQLALCHEMY_DATABASE_URI = 'mysql://%(user)s:%(pw)s@%(host)s/%(db)s' % MYSQL
	SSL_REDIRECT = True

config = {
	'development': DevelopmentConfig,
	'linuxconfig': LinuxConfig,
	'production': ProductionConfig,
}

