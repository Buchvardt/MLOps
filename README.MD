# MLOps just got real - one pattern to serve them all

MLOps is the new "black". No doubt about it. REF. The thing is, I can't figure out if MLOps engineer is a role separate from the data scientist just as I cant figure out if a full stack developer is a role separate from a DevOps engineer. Endless discussions fill up my LinkedIn feed with arguments ranging from AutoMLPlatform "one-size-fits-all" and a role granularity where you can stop dreaming of AI in production if you do not have at least one of each of these roles: 

[business analyst, data analyst, citizen data scientist, data scientist, data engineer, ML engineer, AI engineer, MLOps engineer] 

Let's not go further down that rabbithole... 

Who blames who for why they are not succeeding with their AI is not my place to address. Instead I will relay a framework that basically any of the above mentioned roles, as well as all other it-professionals, can implement with a bit of Python knowledge and access to a search engine.

## Whats new?
Nothing! at least not when you look at every component for itself. You will find that you can search the internet and find much more elaborate tutorials on each of the components in the framework I am about to propose. However, as of this day of writing, it is near impossible to find an end-to-end example implementation af an ML application. Almost every time there are a lot of blanks to fill in. That is, if you even get any pieces to the puzzle at all and not just a bunch of arguments digging the aforementioned rabbithole even deeper.

## What happens when your ML model is done?

Taking the ML model from a notebook and making it available to an application is what that last step in our beloved CRISP-DM is all about.

Deployment! 

You are supposed to be finished! That is if, and thats a big IF, you ever reach that infamous deployment stage. Its like completing your favorite video game and just have to enjoy that last bonus stage and receive a bunch of gems you can flash for all your friends in the multiplayer arenas. 

Except that bonus stage turned out to be a completely new game with layers and layers of complexity and a ton of puzzles solve.

As a data scientist at some point early in your career you probably experienced something along the lines of:
```
Me:                 The model is done - look at that amazing accuracy!#¤
                    (Flashing my RMarkdowns and Jupyter Notebooks)

Product Manager:    Wow - nice colors!?
                    (Having never seen a plot made with ggplot or matplotlib)

Me:                 Yes? but have you noticed the AMAZING loss curves!#¤

Product Manager:    So... Lesser is better? Well nice job! Where do we go from here?

Me:                 Thank you - it truly means allot!
                    (Thinking about if now is the time to ask for a raise)

Me:                 Ehm... Go from here?
                    (Thinking about possible exciting projects she has lined up for me)

Product Manager:    Yes. When do you plan to implement it into our solution?

Me:                 Ehm... So you need me to do that? 
                    (Thinking - Don't we have any hmm ML Implementation Engineers in our team?

Product Manager:    I don't see who else it could be.?

Me:                 Well ok then... [long pause] What are you thinking in terms of timeframe here?
                    (Thinking - there goes my raise, and possibly my job)
```


 ## Let's Go
 How hard can it be - we already hold the sexiest title of the 21th century REF. Let's show them that we are not "all show and no go"!

In the following there will be almost no attention to the development of a ML model as it is assumed that you read this far because you want to know what to do with your models, once they are good enough.

 The content will be

 Part one (this part)
 
 * Create a REST API for receiving data
 * Use Docker for the API
 * Why do we need asynchronous functions
 * Use RabbitMQ and Celery
 * Docker-compose for local experimentation
  
Part two
 * Deploy to local Kubernetes cluster
 * Think elasticity and scalability early
 * HPA vs. KEDA
 * Set up monitoring

Part three
 * Set up trail subscription in MS Azure
 * Deploy your app to the cloud
 * Watch those running costs


## Why do we need asynchronous functions

Have you ever wondered if your python application could benefit from using an asynchronous pattern but gave up because of the enormous amount of "hello world" tutorials you needed to dig through?

In the following we will go through the set up af a python application of microservices that:

  * Receives data through a REST API
  * Places data in message queue
  * Computes output based on data from message
  * Sends output to frontend
  * Monitor application health

In order to achieve this we will use the following components

  * Python Flask
  * Celery
  * RabbitMQ
  * Flower
  * Docker-Compose
  * (Kubernetes)
  * (Prometheus + Grafana)
  
The final application will be deployed in a local Kubernetes cluster with autoscaling enabled based on the number of messages in the message queue. Before we get there, there will be some intermediate steps where we will use Docker and Docker-compose to develop and experiment.

## Environment setup
We need to install the following

* Docker https://docs.docker.com/get-docker/
* Anaconda with Python https://docs.anaconda.com/anaconda/install/index.html
* minikube TODO describe minikube installation

## Python Flask REST API
The first microservice we will turn our attention to is the Flask REST API that will handle the task of receiving data and placing them in a message queue.


![REST API, screenshot of the api](img/fullapi.png)


The REST API has the endpoints /comment, /healthcheck, and /hello which are defined in the api.py file. For the sake of overview the api.py file is kept as clean as possible importing most configuration and functionality from the other files in the modules folder.

In the project repository there will be the following file structure. 


```
|--modules
|   |
|   |--api.py
|   |--apifunctions.py
|   |--worker.py
|   |--requirements.txt
|   |--Dockerfile
|
|--docker-compose.yml

```

There is some initial setup in order to get the api working right as we can see in the top of the [api.py](modules/api.py) file.

```
from flask import Flask, Blueprint
from flask_restplus import Resource, Api, fields
from flask import jsonify
from flask import request
from werkzeug.contrib.fixers import ProxyFix
import logging
import time

##### SETUP #####

# Import custom celery configurations
from worker import make_celery

# Import functions to be executed in API routes
from apifunctions import send_comment_to_queue

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

        return jsonify('Hello from DIMA'), 200

# Healthcheck endpoint
@api.route("/healthcheck", endpoint='Health Check')
class HealthCheck(Resource):

        def get(self):

            return {"pong": True}, 200

# Define api model for comment route
api_format = api.model("api_format", {"email": fields.String(description="email", required=True), 
                                      "comment": fields.String(description="comment", required=True),
                                      "content_id": fields.Integer(description="id", required=True)})

# Comment endpoint
@api.route('/comment', endpoint="comment")
class comment(Resource):

    comments = {}
    @api.expect(api_format)
    def post(self):

        # Get request data from post
        request_data = request.get_json()

        # Apply synchronous function
        response = send_comment_to_queue(request_data)

        # Apply asynchronous function
        # Will send message to queue and celery worker will pick it up
        _ = celery_function.apply_async([response["message"]], queue="celery")

        # Return without waiting for asynchronous task
        return response, 201

##### ENDPOINTS #####

##### CELERY FUNCTIONS #####

# Async celery function
@celery.task(ignore_result=True)
def celery_function(message):

    # Simulate long running task
    for i in range(20):

        print(f'Processing msg: {message} - time left: {20-i}')

        time.sleep(1)        

    print(f'DONE')

    return

##### CELERY FUNCTIONS #####
```

The make_celery function imported from [worker.py](modules/worker.py) configures the celery worker. Please note the broker variable that is set to ampq://guest:guest@rabbtmq:6272. This string is possible because we later will link the rabbitmq service via the docker-compose file to the api.

```
from celery import Celery

# Set the connection to rabbitmq
broker = 'amqp://guest:guest@rabbitmq:5672'

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=broker,  #app.config['CELERY_BROKER_URL'],
        backend=broker  #app.config['CELERY_BACKEND_URL']
    )
  
    celery.conf.update(app.config,
                       worker_prefetch_multiplier=1,
                       task_acks_late=False,
                       enable_utc=True,
                       broker_transport_options={'visibility_timeout': 3600},  # 1 hour.
                       broker_pool_limit=None) 

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
```

The functions are imported from [apifunctions.py](modules/apifunctions.py) which as mentioned keeps the coding of the api separate from coding the logic.

```
def send_comment_to_queue(request_data): 

    email = request_data['email']
    comment = request_data['comment']
    content_id = '{}'.format(request_data['content_id'])

    message = 'Comment created and associated with content_id {}'.format(content_id)

    response = {
            'status': 'SUCCESS',
            'message': message
            }

    return response
```
To put the api into docker, the [Dockerfile](modulse/Dockerfile) looks like this.

```
FROM python:3.8-slim-buster
ADD api.py worker.py apifunctions.py requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
```

Now we need to build the docker image and deploy the api, worker and rabbitmq. For this we will initially use docker-compose.

```
version: '3'

services:
  rabbitmq:
    image: rabbitmq:3.7.8-management
    container_name: rabbitmq
    # environment:
    #     RABBITMQ_DEFAULT_USER: AA
    #     RABBITMQ_DEFAULT_PASS: BB
    ports:
      - 15673:15672
    networks:
        - sample_app_net
    healthcheck:
      test: [ "CMD", "nc", "-z", "localhost", "5672" ]
      interval: 5s
      timeout: 15s
      retries: 1
  sample-app:
    container_name: sample-app
    build:
      context: modules.
      dockerfile: Dockerfile
    image: sample-app:latest
    ports:
      - 8000:8000
    command: gunicorn --log-level debug --graceful-timeout 30 --bind 0.0.0.0:8000 api:app
    networks:
      - sample_app_net
  celery-worker:
    container_name: celery_worker
    image: sample-app:latest
    links:
      - rabbitmq
    command: celery -A api.celery worker --concurrency=1 -Ofair -n predict --pool=solo
    networks: 
      - sample_app_net
    restart: on-failure
    depends_on:
      - rabbitmq

networks:
  sample_app_net:
    driver: bridge
```

### Look into rabbitmq

### test application