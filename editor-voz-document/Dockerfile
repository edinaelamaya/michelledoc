# Etapa de desarrollo
FROM node:18-alpine AS development

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apk add --no-cache curl

# Primero copiamos package.json y package-lock.json (si existe)
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Crear directorios necesarios
RUN mkdir -p /app/src && \
    mkdir -p /app/node_modules && \
    chmod -R 777 /app

# Copiar todo el contenido del proyecto
COPY . .

# Exponer el puerto
EXPOSE 6800

# Comando para desarrollo
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]