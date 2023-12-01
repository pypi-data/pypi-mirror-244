from stsdk.api.http.oms import OMSApi
from stsdk.common.key import (
    CONTRACT_TYPE_LINEAR,
    ORDER_DIRECTION_BUY,
    ORDER_DIRECTION_SELL,
    ORDER_TYPE_LIMIT,
    POSITION_SIDE_NOTBOTH,
    TIME_IN_FORCE_GTC,
)


class OrderManager:
    def __init__(self, strategy_id, account_id):
        self.omsApi = OMSApi()
        self.openOrders = dict()
        self.strategy_id = strategy_id
        self.account_id = account_id

    def place_order(self, instrumentId, price, size, side, offset, **kwargs):
        data = {
            "strategy_id": self.strategy_id,
            "account_id": self.account_id,
            "quantity": size,
            "price": price,
            "instrument_id": instrumentId,
            "position_side": POSITION_SIDE_NOTBOTH,
            "contract_type": CONTRACT_TYPE_LINEAR,
            "order_type": ORDER_TYPE_LIMIT,
            "order_direction": ORDER_DIRECTION_BUY
            if side == "buy"
            else ORDER_DIRECTION_SELL,
            "time_in_force": TIME_IN_FORCE_GTC,
            "leverage": 2,
        }
        resp = self.omsApi.place_order(data)
        if "orderId" in resp:
            resp["OrderId"] = resp["orderId"]
        self.append_order(instrumentId, resp)
        return resp

    def cancel_order(self, instrumentId, orderId):
        data = {
            "order_id": orderId,
        }
        resp = self.omsApi.cancel_order(data)
        self.remove_order(instrumentId, orderId)
        return resp

    def cancel_best_price_order(self, instrumentId, side):
        orders = {
            order_id: order_details["price"]
            for order_id, order_details in self.openOrders[instrumentId].items()
            if order_details["side"] == side
        }
        return self.cancel_order(instrumentId, max(orders, key=orders.get))

    def cancel_worst_price_order(self, instrumentId, side):
        orders = {
            order_id: order_details["price"]
            for order_id, order_details in self.openOrders[instrumentId].items()
            if order_details["side"] == side
        }
        return self.cancel_order(instrumentId, min(orders, key=orders.get))

    def cancel_instrument_orders(self, instrumentId):
        resps = []
        instrument_orders = self.openOrders[instrumentId]
        for order_id in instrument_orders:
            resps.append(self.cancel_order(instrumentId, order_id))
        return resps

    def cancel_all_orders(self):
        # await self.omsApi.cancel_all_orders()
        resps = []
        for instrument_id, orders in self.openOrders.items():
            for order_id in orders.keys():
                resps.append(self.cancel_order(instrument_id, order_id))
        return resps

    def append_order(self, instrumentId, data):
        if instrumentId not in self.openOrders:
            self.openOrders[instrumentId] = {}
        if "OrderId" in data:
            self.openOrders[instrumentId][data["OrderId"]] = data

    def remove_order(self, instrumentId, orderId):
        if instrumentId in self.openOrders and orderId in self.openOrders[instrumentId]:
            del self.openOrders[instrumentId][orderId]
            if len(self.openOrders[instrumentId]) == 0:
                del self.openOrders[instrumentId]
            return True

    def remove_instrumentId(self, instrumentId):
        if instrumentId in self.openOrders:
            del self.openOrders[instrumentId]

    def get_open_orders(self, instrumentId):
        return self.openOrders.get(instrumentId, {})

    def get_all_open_orders(self):
        return self.openOrders

    def get_order_by_id(self, instrumentId, orderId):
        return self.openOrders.get(instrumentId, {}).get(orderId, None)
