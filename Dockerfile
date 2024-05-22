FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV API_URL="http://localhost:3000"
ENV MEASUREMENT_DELAY=3
ENV DISCOVER_DELAY=15

CMD ["python", "-u", "main.py"]