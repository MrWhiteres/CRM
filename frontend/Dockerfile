FROM node:lts-alpine as build-stage
WORKDIR /frontend
COPY package*.json ./
RUN yarn install
COPY . .
RUN yarn build


FROM nginx:stable-alpine as production-stage
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build-stage /frontend/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]