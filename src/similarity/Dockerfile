# https://github.com/soumilshah1995/Python-Flask-Redis-Celery-Docker/blob/main/Part1/simple_worker/Dockerfile 
FROM python:3.8-slim

RUN apt-get update
# https://stackoverflow.com/a/63377623/10127204
RUN apt-get install ffmpeg libsm6 libxext6  -y

# layer caching for faster builds
COPY requirements.txt .
RUN pip3 install -r requirements.txt

ADD . /similarity
WORKDIR /similarity

ENTRYPOINT celery -A models worker --loglevel=info