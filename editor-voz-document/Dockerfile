# Etapa de desarrollo
FROM node:18-alpine

WORKDIR /app

RUN apk add curl

# Crear directorios necesarios y establecer permisos
RUN mkdir -p /app/src
# Copiar archivos de configuración
COPY package*.json ./
COPY vite.config.ts ./
COPY tsconfig*.json ./
COPY index.html ./

# Instalar dependencias
RUN npm install

# Copiar el código fuente
COPY ./src/ ./src/

# Asegurar permisos después de copiar
RUN chmod -R 777 /app/src && \
    chmod -R 777 /app/node_modules

# Exponer el puerto
EXPOSE 5173

# Comando para desarrollo
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]