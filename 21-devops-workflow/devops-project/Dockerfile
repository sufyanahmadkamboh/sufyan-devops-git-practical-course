# The cafe menu: a static site served by nginx (unprivileged image: runs as a non-root user, listens on 8080)
FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY application/ /usr/share/nginx/html/
EXPOSE 8080
