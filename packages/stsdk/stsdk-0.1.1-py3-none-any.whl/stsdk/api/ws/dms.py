import json

from stsdk.common.key import (
    DMS_BBO,
    DMS_KLINE,
    DMS_LOB,
    DMS_TRADE,
)
from stsdk.utils.config import config
from stsdk.utils.websocket import Websocket


class DMSWS:
    DMS_BASE_WS_URL = config.DMS_BASE_WS_URL
    ws = None
    queue = None

    def __init__(self):
        self.ws = Websocket(self.DMS_BASE_WS_URL + "/ws/dms")

    def run(self, queue):
        self.ws.run(queue)

    def bbo(self, instrument_id):
        req = {
            "event": "sub",
            "topic": f"{DMS_BBO}.{instrument_id}",
        }
        self.ws.register(json.dumps(req))

    def lob(self, instrument_id):
        req = {
            "event": "sub",
            "topic": f"{DMS_LOB}.{instrument_id}",
        }
        self.ws.register(json.dumps(req))

    def kline(self, instrument_id):
        req = {
            "event": "sub",
            "topic": f"{DMS_KLINE}.{instrument_id}",
        }
        self.ws.register(json.dumps(req))

    def trade(self, instrument_id):
        req = {
            "event": "sub",
            "topic": f"{DMS_TRADE}.{instrument_id}",
        }
        self.ws.register(json.dumps(req))
