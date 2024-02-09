# Use Alpine Linux as base image
FROM alpine:latest AS builder

# Install necessary packages
RUN apk update && apk add --no-cache \
    nginx \
    gettext \
    && rm -rf /var/cache/apk/*

# Create nginx directories
RUN mkdir -p /run/nginx

# Copy nginx configuration files
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

# Copy HTML files to be served
COPY index.html /usr/share/nginx/html/index.html

# Expose the port nginx will listen on
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]

