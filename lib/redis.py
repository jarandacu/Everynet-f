# -*- encoding: utf-8 -*-

# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from redis import StrictRedis
from werkzeug.local import LocalProxy
from bottle import request, local


redis = LocalProxy(lambda: request.environ.get("redis.connection", None))


class RedisPlugin(object):
    name = "RedisPlugin"
    api  = 2

    def __init__(self, **kwrag):
        self.port = 6379
        self.db   = kwrag.get("db", None)

        host  = kwrag.get("host", "") + ":"
        parts = host.split(':')
        host, port = parts[0], parts[1]
        self.host  = host
        if port:
            self.port = int(port)

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            connection = StrictRedis(host=self.host, db=self.db)
            request.environ["redis.connection"] = connection
            local.redis = connection
            rv = callback(*args, **kwargs)
            return rv
        return wrapper
