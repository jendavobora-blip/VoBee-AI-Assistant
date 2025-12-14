FROM nginx:alpine

WORKDIR /app

COPY nginx.conf /etc/nginx/nginx.conf
COPY . .

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
