import websocket


class Websocket:
    url = None
    ws = None
    sub_keys = set()
    handle_message = None

    def __init__(self, url):
        self.url = url

    def register(self, sub_key):
        self.sub_keys.add(sub_key)

    def run(self, consumer):
        print("Websocket connecting...")

        def handle_message(ws, message):
            consumer(message)

        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=handle_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

        self.ws.run_forever(reconnect=5)

    def on_open(self, ws):
        print("Websocket connection opened")
        for payload in self.sub_keys:
            self.ws.send(payload)

    def on_close(self, ws, close_status_code, close_msg):
        print("Websocket connection closed")
        ws.close()

    def on_error(self, ws, error):
        print("Websocket error received: %s" % error)
