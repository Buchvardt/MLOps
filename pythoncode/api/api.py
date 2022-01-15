from flask import Flask, Blueprint
from flask_restplus import Resource, Api, fields
from flask import jsonify
from flask import request
from werkzeug.contrib.fixers import ProxyFix
import logging

##### SETUP #####

# Import custom celery configurations
from worker import make_celery

# Import functions to be executed in API routes
from celeryfunctions import long_running_function

# Name of the app
app_name = 'comments-api'

# Create Flask instance
app = Flask(app_name)

# Set debugger for use later in Docker logs
app.debug = True

# Flask_restpluss instance to create swagger
api = Api()

# Flask Blueprint instance to hold API configuration
blueprint = Blueprint('api', __name__, url_prefix='/api')  

# Set api details
api.init_app(blueprint,
                endpoint='api',
                version='0.0.1',
                title='Python Flask REST API',
                description='Application Demo for using RabbitMQ',
                contact='DIMA',
                contact_email='mbb@kmd.dk',
                default_label='RESTful Web Api')

# Register blueprint
app.register_blueprint(blueprint)

# Fixes HTTP/HTTPS issues.
app.wsgi_app = ProxyFix(app.wsgi_app)

# Create celery object
celery = make_celery(app)

##### SETUP #####

##### ENDPOINTS #####

# Hello world endpoint
@api.route("/hello", endpoint='Test Connection')
class HelloWorld(Resource):

    def get(self):

        return {'reply':'Hello from DIMA'}, 200

# Healthcheck endpoint
@api.route("/healthcheck", endpoint='Health Check')
class HealthCheck(Resource):

        def get(self):

            return {"pong": True}, 200

# Define api model for comment route
api_format = api.model("api_format", {"Title": fields.String(description="Title", required=True), 
                                      "content": fields.String(description="content", required=True)})

# Comment endpoint
@api.route('/comment', endpoint="comment")
class comment(Resource):

    comments = {}
    @api.expect(api_format)
    def post(self):

        # Get request data from post
        request_data = request.get_json()

        content = request_data['content']

        # Apply asynchronous function
        # Will send message to queue and celery worker will pick it up
        _ = celery_function.apply_async([{"content":content}], queue="celery")

        # Return without waiting for asynchronous task
        return {"Status": "Success"}, 201

##### ENDPOINTS #####

# Async celery function
@celery.task(ignore_result=True)
def celery_function(message):

    long_running_function(message)