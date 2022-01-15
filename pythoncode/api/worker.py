from celery import Celery
from config import api_config

# Set the connection to rabbitmq
broker = api_config["broker"]

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=broker,  #app.config['CELERY_BROKER_URL'],
        backend=broker  #app.config['CELERY_BACKEND_URL']
    )
    # https://docs.celeryproject.org/en/latest/userguide/configuration.html#example-configuration-file
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