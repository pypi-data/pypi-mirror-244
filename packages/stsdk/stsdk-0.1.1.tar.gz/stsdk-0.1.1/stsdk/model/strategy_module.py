import threading
from typing import Dict, List

from stsdk.common.key import (
    ORDER_STATUS_CANCELED,
    ORDER_STATUS_EXPIRED,
    ORDER_STATUS_FILLED,
    ORDER_STATUS_NEW,
    ORDER_STATUS_OMS_PLACE_ORDER_FAILED,
    ORDER_STATUS_PARTIALLY_FILLED,
    ORDER_STATUS_REJECTED,
)
from stsdk.common.signal_key import CANCEL_ORDER_SIGNAL, PLACE_ORDER_SIGNAL
from stsdk.model.order_manager import OrderManager
from stsdk.model.position_manager import PositionManager
from stsdk.model.strategy_base import StrategyBaseModule
from stsdk.utils.log import log


class StrategyModule(StrategyBaseModule):
    def __init__(self, strategy_id, account_id):
        super().__init__(strategy_id, account_id)
        self.orderManager = OrderManager(strategy_id, account_id)
        self.positionManager = PositionManager()
        self.init_order_thread()
        log.info("StrategyModule init")

    def init_order_thread(self):
        threading.Thread(target=self.consumer_with_signal).start()

    def place_order_signal(self, instrumentId, price, size, side, offset, **kwargs):
        message = {
            "instrumentId": instrumentId,
            "price": price,
            "size": size,
            "side": side,
            "offset": offset,
            **kwargs,
        }
        PLACE_ORDER_SIGNAL.send(message)

    def cancel_order_signal(self, instrumentId, orderId):
        message = {
            "instrumentId": instrumentId,
            "orderId": orderId,
        }
        CANCEL_ORDER_SIGNAL.send(message)

    def place_order_handle(self, message):
        instrumentId, price, size, side, offset = message.values()
        self.place_order(instrumentId, price, size, side, offset)

    def cancel_order_handle(self, message):
        instrumentId, orderId = message.values()
        self.cancel_order(instrumentId, orderId)

    def consumer_with_signal(self):
        PLACE_ORDER_SIGNAL.connect(self.place_order_handle)
        CANCEL_ORDER_SIGNAL.connect(self.cancel_order_handle)

    def place_order(self, instrumentId, price, size, side, offset, **kwargs):
        resp = self.orderManager.place_order(
            instrumentId, price, size, side, offset, **kwargs
        )
        log.info("place_order resp: %s" % resp)
        if "orderId" in resp:
            resp["OriginQuantity"] = resp["originQuantity"]
            resp["OrderDirection"] = resp["orderDirection"]
            self.positionManager.update_position(
                resp["instrumentId"], self.positionManager.update_new_position(resp)
            )
            log.info(self.positionManager.get_position(resp["instrumentId"]))
        return resp

    def place_batch_orders(self, orders: List[Dict]):
        resps = []
        for o in orders:
            resps.append(self.place_order(**o))
        return resps

    def cancel_order(self, instrumentId, orderId):
        return self.orderManager.cancel_order(instrumentId, orderId)

    def cancel_batch_orders(self, orders):
        resps = []
        for o in orders:
            resps.append(self.cancel_order(o.instrumentId, o.orderId))
        return resps

    def cancel_best_price_order(self, instrumentId, side):
        return self.orderManager.cancel_best_price_order(instrumentId, side)

    def cancel_worst_price_order(self, instrumentId, side):
        return self.orderManager.cancel_worst_price_order(instrumentId, side)

    def cancel_instrument_orders(self, instrumentId):
        return self.orderManager.cancel_instrument_orders(instrumentId)

    def cancel_all_orders(self):
        return self.orderManager.cancel_all_orders()

    def get_position(self, instrumentId):
        return self.positionManager.get_position(instrumentId)

    def get_open_orders(self, instrumentId):
        return self.orderManager.get_open_orders(instrumentId)

    def get_all_open_orders(self):
        return self.orderManager.get_all_open_orders()

    def get_all_positions(self):
        return self.positionManager.get_all_positions()

    def get_order_by_id(self, instrumentId, orderId):
        return self.orderManager.get_order_by_id(instrumentId, orderId)

    def handle_order_update(self, message):
        if "body" in message:
            order_id = message["body"]["OrderId"]
            order_status = message["body"]["OrderStatus"]
            log.info(
                "receive order update: OrderId: %s, OrderStatus: %s"
                % (order_id, order_status)
            )
            if order_status in [ORDER_STATUS_NEW, ORDER_STATUS_PARTIALLY_FILLED]:
                self.orderManager.append_order(
                    message["body"]["InstrumentId"], message["body"]
                )
            if order_status == ORDER_STATUS_FILLED:
                if self.orderManager.remove_order(
                    message["body"]["InstrumentId"], message["body"]["OrderId"]
                ):
                    self.positionManager.update_position(
                        message["body"]["InstrumentId"],
                        self.positionManager.update_filled_position(message["body"]),
                    )
            if order_status in [
                ORDER_STATUS_CANCELED,
                ORDER_STATUS_REJECTED,
                ORDER_STATUS_EXPIRED,
                ORDER_STATUS_OMS_PLACE_ORDER_FAILED,
            ]:
                if self.orderManager.remove_order(
                    message["body"]["InstrumentId"], message["body"]["OrderId"]
                ):
                    self.positionManager.update_position(
                        message["body"]["InstrumentId"],
                        self.positionManager.update_canceled_position(message["body"]),
                    )
        else:
            log.error("message: %s" % message)
