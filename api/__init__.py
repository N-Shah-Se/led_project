from flask_restful import Api
from app import flaskAppInstance
from .apis import LED
# from .TaskByIDAPI import TaskByID


restServerInstance = Api(flaskAppInstance)

restServerInstance.add_resource(Task,"/api/v1.0/task")
# restServerInstance.add_resource(TaskByID,"/api/v1.0/task/id/<string:taskId>")