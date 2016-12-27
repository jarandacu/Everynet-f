FROM alpine:3.3

ENV APP_DIR "/app"
ENV APP "$APP_DIR/main.py"

# Database hosts settings
ENV MYSQL_HOST "mysql"
ENV MYSQL_USER "root"
ENV MYSQL_DB "lora"
ENV MYSQL_PWD ""
ENV REDIS_HOST "redis"

ADD . /app

WORKDIR /app

EXPOSE 8080

RUN \
  build_pkgs="gcc linux-headers musl-dev python-dev py-pip make" && \
  runtime_pkgs="python mysql-client" && \
  apk --update add ${build_pkgs} ${runtime_pkgs} && \
  python -m pip install -U pip && \
  pip install -r requirements.txt && \
  chmod +x docker-entrypoint.sh && \
  apk del ${build_pkgs} && \
  rm -rf /var/cache/apk/*

CMD /app/docker-entrypoint.sh

