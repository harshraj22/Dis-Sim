FROM python:3.8

WORKDIR /app
COPY . .

EXPOSE 8501
RUN pip install -r requirements.txt

CMD ["streamlit", "run", "frontend.py"]