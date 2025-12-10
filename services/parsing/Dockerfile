FROM python:3.13.9

WORKDIR /app

RUN apt-get update && apt-get install -y

RUN pip install playwright

RUN playwright install --with-deps chromium

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

COPY src ./src

CMD ["gunicorn", "src.app:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:9101"]