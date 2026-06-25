# ESTÁGIO 1: Build do React com Vite
FROM node:18-alpine AS build
WORKDIR /app
# Copia dependências
COPY package*.json ./
RUN npm install
# Copia o código e o arquivo .env do frontend
COPY . .
# Gera a pasta dist/
RUN npm run build

# ESTÁGIO 2: Servir com Nginx
FROM nginx:alpine
# Remove a página padrão do Nginx
RUN rm -rf /usr/share/nginx/html/*
# Copia os arquivos compilados do Estágio 1
COPY --from=build /app/dist /usr/share/nginx/html
# Configuração simples para o React Router funcionar sem dar erro 404
RUN echo 'server { listen 80; location / { root /usr/share/nginx/html; index index.html; try_files $uri $uri/ /index.html; } }' > /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]