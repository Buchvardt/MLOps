FROM python:3.8-slim-buster
ADD . /api/
WORKDIR /api
RUN pip install -r requirements.txt
EXPOSE 8000
#ENTRYPOINT [ "gunicorn", "--log-level", "debug", "--graceful-timeout", "30", "--bind", "0.0.0.0:8000", "api:app" ]