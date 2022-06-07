# https://github.com/soumilshah1995/Python-Flask-Redis-Celery-Docker/blob/main/Part1/simple_worker/Dockerfile 
FROM python:3.8-slim

# layer caching for faster builds
COPY requirements.txt /
RUN pip install -r /requirements.txt

ADD . /similarity
WORKDIR /similarity

ENTRYPOINT celery -A models worker --loglevel=info