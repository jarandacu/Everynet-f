# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, print_function

import numbers
import logging
import traceback
import bottle
import __builtin__


def get_public_methods(obj):
    """Return a dictionary of all public callables in a namespace.
    This can be used for objects, classes and modules.
    """
    methods = {}

    for name in dir(obj):
        method = getattr(obj, name)
        if not name.startswith('_') and callable(method):
            methods[name] = method

    return methods


class JSONRPCError(Exception):
    def __init__(self, id_, code, message, data=None):
        Exception.__init__(self)
        self.code = code
        self.message = message
        self.data = data
        self.id = id_

    def __str__(self):
        return "%s\nJSONRPCError (%d): %s" % (self.data, self.code, self.message)

    def __repr__(self):
        return self.__str__()

    def prepare(self):
        d = {"jsonrpc": "2.0", "id": self.id, "error": {"code": self.code, "message": self.message}}
        if self.data:
            d['error']['data'] = self.data
        return d


class NameSpace:
    def __init__(self, path, obj=None, app=None):
        self.path = path
        self.app = app or bottle.default_app()
        self.methods = {}

        if obj is not None:
            self.add_object(obj)

        self._make_handler()

    def add_object(self, obj):
        """Adds all public methods of the object."""
        self.methods.update(get_public_methods(obj))

    def check_request(self, req):
        if not isinstance(req, dict):
            return False
        id_ = req.get("id", None)
        # TODO check notify
        return  (
                isinstance(id_, basestring) or
                isinstance(id_, numbers.Integral)
            ) and \
            req.get('jsonrpc', None) == u"2.0" and \
            isinstance(req.get("method", None), basestring)

    def handle_request(self):
        request = bottle.request.json

        if not self.check_request(request):
            return JSONRPCError(None, -32600, "Invalid Request", data="The JSON sent is not a valid Request").prepare()

        try:
            if self.methods.has_key(request['method']):
                func = self.methods[request['method']]
            else:
                raise JSONRPCError(request['id'], -32601, "Method not found", data=request['method'])

            try:
                params = request.get('params', list())
                if isinstance(params, dict):
                    result = func(**params)
                elif isinstance(params, list):
                    result = func(*params)
                else:
                    result = func(params)
                return {"jsonrpc": "2.0", "id": request["id"], "result": result}

            except TypeError:
                raise JSONRPCError(request['id'], -32602, 'Invalid params', data=traceback.format_exc())

        except JSONRPCError as err:
            logging.error("JSONRPCError = %s" % err)
            err.id = request['id']
            return err.prepare()

        except Exception:
            data = traceback.format_exc()
            logging.error(data)
            return JSONRPCError(None, -32603, 'Internal error', data=data).prepare()

    def _make_handler(self):
        """Sets up bottle request handler."""
        @self.app.post(self.path)
        def rpc():
            return self.handle_request()

    def __call__(self, func):
        """This is called when the mapper is used as a decorator."""
        self.methods[func.__name__] = func
        return func
