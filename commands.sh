
# Build docker
docker-compose build

# Run docker
docker-compose up

# Simulate 30 msgs in anaconda terminal
python post-test.py

# Look in rabbitmq management
localhost:15673 # portbinding 15673:15672 in docker-compose

# lok into celery logs
docker logs celery_worker -f

# Simulate k8s SIGTERM in another terminal
docker kill --signal="SIGTERM" sample-app

# Se in the rabbitmq queue that
# the number remaining + the last nuber from the celery_worker logs = 30

# Start worker and kill agin a few times to se it workes
docker start celery_worker