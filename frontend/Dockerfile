# Используем Node.js для сборки
FROM node:22 AS build

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json для установки зависимостей
COPY package.json package-lock.json ./

# Устанавливаем все зависимости, включая devDependencies, для сборки
RUN npm install

# Копируем весь исходный код фронтенда
COPY . .

# Собираем проект (предполагается, что используется Vite)
RUN npm run build

# Стадия 2: Раздача статики через Nginx
FROM nginx:alpine

# Копируем собранные файлы в директорию Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Копируем конфигурацию Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Открываем порт
EXPOSE 80

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]