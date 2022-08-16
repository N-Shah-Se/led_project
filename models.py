# from flask_sqlalchemy import SQLAlchemy
# from .app import db

# # db = SQLAlchemy(app)


# class led_db(db.Model):
# 	id = db.Column('id', db.Integer, primary_key = True)
# 	light_code = db.Column(db.String(200))
# 	light_no = db.Column(db.String(10))  
# 	light_status = db.Column(db.String(20))
# 	street_no = db.Column(db.String(10))
	
# 	def __init__(self, light_code, light_no, light_status,street_no):
# 	   self.light_code = light_code
# 	   self.light_no = light_no
# 	   self.light_status = light_status
# 	   self.street_no = street_no

# db.create_all()