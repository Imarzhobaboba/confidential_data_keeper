# frontend/Dockerfile
FROM node:18.20.3-alpine3.19

WORKDIR /app

# Установка зависимостей
COPY package*.json ./
RUN npm install --force

# Копирование исходников
COPY . .

# Указываем Vite слушать все интерфейсы
ENV HOST=0.0.0.0

# Сборка проекта
RUN npm run build

EXPOSE 4173

CMD ["npm", "run", "preview", "--", "--host"]