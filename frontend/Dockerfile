# Node.js base image installation
FROM node:18.16 AS build-stage

# Set up a working directory inside the container
WORKDIR /app

# Copying the dependencies into the container
COPY vue-project/package*.json ./

# Dependency installation
RUN npm install

# Copying source files into a container
COPY . .

WORKDIR /app/vue-project
# Build static files
RUN npm run build

# second step for hosting container
FROM nginx:stable-alpine as production-stage

# Copying the assembled static files into the hosting container
COPY --from=build-stage /app/vue-project/dist /usr/share/nginx/html

# Command to start the Nginx server
CMD ["nginx", "-g", "daemon off;"]