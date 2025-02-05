#!/bin/bash

# Esperar a que la base de datos esté lista
echo "Waiting for database to be ready..."
sleep 30

# Inicializar la base de datos
echo "Initializing database..."
python -m app.scripts.init_db

# Verificar si la inicialización fue exitosa
if [ $? -eq 0 ]; then
    echo "Database initialization successful"
    # Iniciar la aplicación
    echo "Starting application..."
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Database initialization failed"
    exit 1
fi 