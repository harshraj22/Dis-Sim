FROM python:3.8

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN mkdir -p db

EXPOSE 8501

CMD ["streamlit", "run", "main_page.py"]