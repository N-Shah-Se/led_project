from flask_sqlalchemy import SQLAlchemy
# from 
from flask_migrate import Migrate, migrate
from .models import db


app = Flask (__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///led.sqlite3'

migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run()









