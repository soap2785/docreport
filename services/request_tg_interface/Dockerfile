FROM python:3.13.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

COPY src ./src

WORKDIR /app/src

CMD ["python", "/app/src/app/bot/__init__.py"]