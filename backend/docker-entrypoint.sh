#!/bin/sh

# Генерация .env
if [ ! -f .env ]; then
  echo "Generating .env file..."
  python -c "from cryptography.fernet import Fernet; print(f'FERNET_ENCRYPTION_KEY={Fernet.generate_key().decode()}')" > .env
  echo "DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}" >> .env
  echo "REDIS_HOST=redis" >> .env
  echo "REDIS_PORT=6379" >> .env
  echo "REDIS_DB=0" >> .env
fi

# Ожидание PostgreSQL (альтернатива без nc)
echo "Waiting for PostgreSQL..."
while ! python -c "import socket; socket.create_connection(('db', 5432), timeout=1)" 2>/dev/null; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Запуск сервера
uvicorn main:app --host 0.0.0.0 --port 8000