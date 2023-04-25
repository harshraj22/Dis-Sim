FROM python:3.8-slim

# layer caching for faster builds
COPY requirements.txt .
RUN pip install -r requirements.txt

#COPY app.py /app.py
ADD . /app
WORKDIR /app
EXPOSE 8020

# CMD ["python3", "-u", "populate.py"]
CMD ["uvicorn", "populate:app", "--reload", "--host", "0.0.0.0", "--port", "8020"]