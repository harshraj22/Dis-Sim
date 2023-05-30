FROM python:3.8-slim

# layer caching for faster builds
COPY requirements.txt .
RUN pip install -r requirements.txt

#COPY app.py /app.py
ADD . /app
WORKDIR /app

ENTRYPOINT celery -A feedback worker --loglevel=info