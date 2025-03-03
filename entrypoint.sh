#!/bin/sh
mkdir -p /app/mediafiles

if [ "$DATABASE" = "postgres" ]
then
    echo "Wait for PostgreSQL..."
    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started.."
fi

python manage.py migrate --noinput

exec "$@"