FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
RUN apt install -y curl
COPY ./nginx.conf /etc/nginx/conf.d/