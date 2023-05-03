# https://github.com/soumilshah1995/Python-Flask-Redis-Celery-Docker/blob/main/Part1/simple_worker/Dockerfile 

# Build stage
FROM python:3.8-slim as builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
        python3-dev \
        python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Final stage
FROM python:3.8-slim

# https://stackoverflow.com/a/63377623/10127204
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        libsm6 \
        libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip3 install --no-cache /wheels/*

ADD . /similarity
WORKDIR /similarity

ENTRYPOINT celery -A models worker --loglevel=info