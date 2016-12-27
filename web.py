# -*- encoding: utf-8 -*-

import functools
import base64
import logging
import json
import api
from time import time, sleep, mktime
from bottle import route, static_file, Jinja2Template, template, request, response, redirect
from lib.db import db
from lib.redis import redis



@route('/static/<filename>')
def static(filename):
    return static_file(filename, root='static/')


@route('/', method=["POST", "GET"])
@route('/<group:re:[0-9a-z]{16}>', method=["POST", "GET"])
def index(group=None):
    if not request.json:
        return template("index.html", template_adapter=Jinja2Template, template_lookup=['templates'], group=group)
    return api.handler.handle_request()


def get_printable_paylod(payload):
    data = base64.b64decode(payload)
    
    # Check for Microchip dev. board sensor data
    if len(data) == 8 and data.isdigit():
        lux  = int(data[0:5])
        temp = int(data[5:])
        return "Light=%d. Temp=%d" % (lux, temp)
    
    try:
        json.dumps(data)
        return data
    except Exception, e:
        return "HEX(0x%s)" % data.encode("hex").upper()
    

@route('/stream')
def stream():
    # Set SSE response
    response.content_type  = 'text/event-stream'
    response.cache_control = 'no-cache'
    
    # Set client-side auto-reconnect timeout, ms.
    yield 'retry: 5000\n\n'

    # Get group from request
    group = request.params.get("group") or None

    last_packet_id = request.params.get("last_packet_id", type=int)
    if last_packet_id:
        packets = db.table('packets')
        if not group:
            packets = packets.where_null("group")
        else:
            packets = packets.where("group", "=", group)
        packets = packets.where("packet_id", ">", last_packet_id).order_by("packet_id", "desc").get()
        for packet in packets:
            packet["payload"] = get_printable_paylod(packet["payload"])
            yield 'data: %s\n\n' % json.dumps(packet)

    # Subscribe to new packets
    pubsub = redis.pubsub()
    pubsub.subscribe("packets")

    last_ping     = time()
    ping_interval = 15

    # Main loop
    while True:
        message = pubsub.get_message()
        if message and message["type"] == "message":
            data = json.loads(message["data"])
            if data["group"] == group:
                data["payload"] = get_printable_paylod(data["payload"])
                yield 'data: %s\n\n' % json.dumps(data)
                continue
        
        if time() - last_ping > ping_interval:
            yield 'data: ping\n\n'
            last_ping = time()
            continue
        
        sleep(0.01)
