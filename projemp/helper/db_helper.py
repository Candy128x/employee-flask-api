from flaskext.mysql import MySQL
from app import app

mysql = MySQL()


class DbHelper:

    def db_conn(self):
        app.config['MYSQL_DATABASE_USER'] = 'root'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'qwerty'
        app.config['MYSQL_DATABASE_DB'] = 'employee_db'
        app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
        mysql.init_app(app)
        return 1