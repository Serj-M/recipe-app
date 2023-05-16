# Установка базового образа Node.js
FROM node:14 AS build-stage

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Копирование зависимостей в контейнер
COPY vue-project/package*.json ./

# Установка зависимостей
RUN npm install

# Копирование исходных файлов в контейнер
COPY . .

# Сборка статических файлов
RUN npm run dev

# Второй этап для контейнера хостинга
FROM nginx:stable-alpine as production-stage

# Копирование собранных статических файлов в контейнер хостинга
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Копирование конфигурации Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Открытие порта для внешнего доступа
EXPOSE 8080

# Команда для запуска Nginx сервера
CMD ["nginx", "-g", "daemon off;"]