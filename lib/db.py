# -*- encoding: utf-8 -*-

from werkzeug.local import LocalProxy
from bottle import request, local
from orator import DatabaseManager

db = LocalProxy(lambda: request.environ.get("orator.db", None))


class OratorMySQLPlugin(object):
    name = "OratorMySQLPlugin"
    api  = 2

    def __init__(self, **kwargs):
        kwargs["driver"] = "mysql"
        self.settings = dict(mysql=kwargs)

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            db = DatabaseManager(self.settings)
            request.environ["orator.db"] = db
            rv = callback(*args, **kwargs)
            return rv
        return wrapper