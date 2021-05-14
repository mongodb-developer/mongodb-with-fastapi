FROM tiangolo/uvicorn-gunicorn-fastapi

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
RUN mkdir -p /app
COPY app.py /app/main.py
