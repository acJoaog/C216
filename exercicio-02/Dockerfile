from python:3.10-slim

WORKDIR /app

copy . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]