FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

RUN chmod +x /app/entrypoint.sh

RUN mkdir -p /app/mediafiles
RUN chmod -R 755 /app/mediafiles


ENTRYPOINT ["/app/entrypoint.sh"]