# -*- encoding: utf-8 -*-

import re
import base64
import json
import binascii
import logging
from lib import jsonrpc
from lib.db import db
from lib.redis import redis
from bottle import request

class LaceAPIHandler(object):
    def _get_group(self):
        res = re.search("^/([0-9a-z]{16})$", request.path)
        return res.group(1) if res else None

    def uplink(self, dev_eui, dev_addr, rx_time, counter_up, port, encrypted_payload=None, payload=None, radio=None):
        radio = radio or dict()
        data  = base64.b64decode(payload or "")
        logging.info('Received [deveui=%s. message="%s"]' % (dev_eui, binascii.hexlify(data)))
        
        # Formating packet
        packet = dict(
            dev_eui=dev_eui, dev_addr=dev_addr, rx_time=int(rx_time), port=port,
            counter_up=counter_up, payload=payload, encrypted_payload=encrypted_payload,
            lsnr=radio.get("lsnr", None), rssi=radio.get("rssi", None),
            group=self._get_group()
        )
        
        # Insert packet to database
        packet_id = db.table("packets").insert_get_id(packet)
        packet["packet_id"] = packet_id

        # Send packet subscribers
        redis.publish("packets", json.dumps(packet))

    def downlink(self, dev_eui, dev_addr, counter_down, tx_time, max_size=51):
        return None


handler = jsonrpc.NameSpace("/rpc", obj=LaceAPIHandler())