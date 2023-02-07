FROM python:3.8 as compile-image


RUN python3 -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.8-slim AS build-image
COPY --from=compile-image /opt/venv/ /opt/venv/

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app 
# https://github.com/streamlit/streamlit/issues/4842#issuecomment-1198455834
COPY . .
RUN mkdir -p db

EXPOSE 8501

CMD ["streamlit", "run", "main_page.py"]