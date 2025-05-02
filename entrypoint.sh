#!/bin/bash

echo "Menunggu database siap..."
sleep 2

# Jalankan makemigrations dan migrate
echo "Menjalankan makemigrations dan migrate..."
python src/manage.py makemigrations
python src/manage.py migrate

# Jalankan server
echo "Menjalankan server Django..."
exec "$@"