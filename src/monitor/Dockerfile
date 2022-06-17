FROM python:3.8-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

ADD . /app
WORKDIR /app

RUN mkdir -p db
# RUN python3 -u database.py

CMD ["python3", "-u", "database.py"]
# https://stackoverflow.com/a/51362306/10127204
CMD ["python3", "-u", "main.py"]