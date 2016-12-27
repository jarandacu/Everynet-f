#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import gevent.monkey; gevent.monkey.patch_all()
import logging
from os import environ
from bottle import run, load, install
from lib import db, redis


def main():
    # Configure logging
    logging.basicConfig(level=logging.DEBUG, format="[%(name)s] [%(levelname)s] [%(asctime)s] - %(message)s")
    logger = logging.getLogger()

    # Get settings
    redis_host = environ.get("REDIS_HOST", "localhost")
    mysql_host = environ.get("MYSQL_HOST", "localhost")
    mysql_db   = environ.get("MYSQL_DB", "lora")
    mysql_user = environ.get("MYSQL_USER", "root")
    mysql_pwd  = environ.get("MYSQL_PWD", "")
    
    # Install mysql and redis plugin
    install(redis.RedisPlugin(host=redis_host))
    install(db.OratorMySQLPlugin(host=mysql_host, user=mysql_user, password=mysql_pwd, database=mysql_db))
    
    # Run web server
    load("api")
    load("web")
    run(host="", port=8080, server="gevent", debug=True, quiet=True)


if __name__ == "__main__":
    main()