# frontend/Dockerfile
FROM node:18.20.3-alpine3.19

WORKDIR /app

# Установка зависимостей
COPY package*.json ./
RUN npm install --force

# Копирование исходников
COPY . .

# Сборка проекта
RUN npm run build

EXPOSE 5173

CMD ["npm", "run", "preview"]