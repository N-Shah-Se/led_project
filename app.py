from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
import logging as logger


logger.basicConfig(level="DEBUG")


flaskAppInstance = Flask(__name__, instance_relative_config=True)

### DB part

flaskAppInstance.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///led_db.sqlite3'

flaskAppInstance.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(flaskAppInstance)


# class Student(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#      = db.Column(db.String(100), nullable=False)
#     lastname = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(80), unique=True, nullable=False)
#     age = db.Column(db.Integer)
#     created_at = db.Column(db.DateTime(timezone=True),
#                            server_default=func.now())
#     bio = db.Column(db.Text)

#     def __repr__(self):
#         return f'<Student {self.firstname}>'

class led_db(db.Model):
	id = db.Column('id', db.Integer, primary_key = True)
	light_code = db.Column(db.String(200))
	light_no = db.Column(db.String(10))  
	light_status = db.Column(db.String(20))
	street_no = db.Column(db.String(10))
	
	def __init__(self, light_code, light_no, light_status,street_no):
	   self.light_code = light_code
	   self.light_no = light_no
	   self.light_status = light_status
	   self.street_no = street_no


###

# flaskAppInstance.config['TESTING'] = True
# flaskAppInstance.config['DEBUG'] = True
# flaskAppInstance.config['FLASK_ENV'] = 'development'
# flaskAppInstance.config['SECRET_KEY'] = 'GDtfDCFYjD'
# flaskAppInstance.config['DEBUG'] = False  # actually I want debug to be off now

# if __name__ == '__main__':

#     logger.debug("Starting Flask Server")
#     from api import *
#     flaskAppInstance.run(host="0.0.0.0",port=5000,debug=True,use_reloader=True)
import paho.mqtt.client as mqtt
import time
import paho.mqtt.client as paho
from paho import mqtt


address = "882bf8e5c2354d2785ab4b8d065f81f5.s1.eu.hivemq.cloud"
username = 'nshah'
password = 'Nasir123'
# address = 'test.mosquitto.org'

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload.decode("utf-8")))
    data = led_db(str(msg.payload.decode("utf-8")),"light_no","ON","123-A")
    db.session.add(data)
    db.session.commit()	
    # ("INSERT INTO led (light_code, light_no) VALUES (?,?)", ['123', str(msg.payload.decode("utf-8"))])
    #conn.commit()
    # data = msg.payload.decode("utf-8")
    # print(data)

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
# client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
db.create_all()

@flaskAppInstance.route('/')
def index():
	
	client = paho.Client()
	client.on_connect = on_connect

	# enable TLS for secure connection
	client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
	# set username and password
	client.username_pw_set(username, password)
	# connect to HiveMQ Cloud on port 8883 (default for MQTT)
	client.connect(address, 8883)

	# setting callbacks, use separate functions like above for better visibility
	client.on_subscribe = on_subscribe
	client.on_message = on_message
	client.on_publish = on_publish

	# subscribe to all topics of encyclopedia by using the wildcard "#"
	# topic = 'LightStatus'
	topic = "Test/Temperature/Temp3"
	client.subscribe(topic, qos=1)
	client.loop_forever()
	return 'Hello, world!'

@flaskAppInstance.route('/show_db')
def show():
	data = led_db.query.all()
	led_data = []
	for i in data:
		data_dict = {}
		# print(i.light_code)
		data_dict['light_code'] = i.light_code
		data_dict['light_no'] = i.light_no
		data_dict['street_no'] = i.street_no
		data_dict['light_status'] = i.light_status
		led_data.append(data_dict)
	print(f'{led_data}')
	return 'data .......'




if __name__ == '__main__':
   db.create_all()
   flaskAppInstance.run(debug = True)