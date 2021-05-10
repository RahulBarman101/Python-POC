from api.Products import Products
from flask_restful import Api
from app import app
from .Task import Task
from .Products import Products

restServer = Api(app)

restServer.add_resource(Task,"/api/task")
restServer.add_resource(Products,"/api/products","/api/products/<id>")