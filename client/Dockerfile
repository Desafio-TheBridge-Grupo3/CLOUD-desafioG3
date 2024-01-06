# Utilizar la imagen base de Node.js 14
FROM node:14

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el código del cliente al directorio de trabajo
COPY . ./client

# Instalar las dependencias del cliente
RUN cd client && npm install
RUN docker login -u juantesttoken -p EUAl/ktFDQU4wfxvkri8o9S1x1OQuv5Psi9hctttOR+ACRCK3Ue+ dockerjuanadevesat.azurecr.io

# Exponer el puerto utilizado por el cliente
EXPOSE 5173

# Iniciar el cliente
CMD ["sh", "-c", "cd client && npm run dev -- --port 5173 --host 0.0.0.0"]
