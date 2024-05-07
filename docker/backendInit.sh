#!/bin/bash

python3 -m venv ./venv
source venv/bin/activate
python3 -m pip install --no-cache-dir -r requirements.txt

# Configurar PostgreSQL y Redis
sudo service postgresql start
sudo su - postgres -c "psql -c \"CREATE USER aparking WITH PASSWORD 'aparking';\""
sudo su - postgres -c "psql -c \"CREATE DATABASE aparking_db OWNER aparking;\""
sudo su - postgres -c "psql -d aparking_db -c \"CREATE EXTENSION postgis;\""

# Esperar hasta que PostgreSQL esté disponible
echo 'Waiting for PostgreSQL database to become available...'
while ! nc -z localhost 5432; do
    sleep 1
done
echo 'Database is available.'

# Desactivar Transparent Huge Pages para Redis
echo madvise | sudo tee /sys/kernel/mm/transparent_hugepage/enabled

# Iniciar Redis sin contraseña
sudo redis-server --port 6379 --protected-mode no &

# Esperar hasta que Redis esté disponible
echo 'Waiting for Redis to become available...'
while ! nc -z localhost 6379; do
    sleep 1
done
echo 'Redis is available.'

echo 'Verifying Redis functionality...'
redis-cli set testkey "testvalue"
if [ "$(redis-cli get testkey)" = "testvalue" ]; then
    echo "Redis is functioning properly."
else
    echo "Failed to verify Redis functionality."
    exit 1
fi

# Ejecutar migraciones y otros comandos de inicio de Django
python3 manage.py makemigrations
python3 manage.py migrate --noinput
python3 importCSV.py

# Cargar datos desde populate.json
echo 'Loading data...'
python3 manage.py loaddata Populate.json

# Iniciar el servidor de Django en modo producción recomendado
echo 'Starting backend...'
daphne -b 0.0.0.0 -p $PORT AparKing_Backend.asgi:application

# python3 manage.py runserver 0.0.0.0:$PORT &
