#!/bin/sh

# Генерация .env если отсутствует
if [ ! -f .env ]; then
  echo "Generating .env file..."
  python -c "from cryptography.fernet import Fernet; print(f'FERNET_ENCRYPTION_KEY={Fernet.generate_key().decode()}')" > .env
  echo "DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}" >> .env
  echo "REDIS_HOST=redis" >> .env
  echo "REDIS_PORT=6379" >> .env
  echo "REDIS_DB=0" >> .env
fi


# Запуск сервера
uvicorn main:app --host 0.0.0.0 --port 8000