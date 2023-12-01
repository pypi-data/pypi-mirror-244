import asyncio
import time

# sys.path.append("/root/lingxiao/st-sdk/")
# sys.path.append("/root/lingxiao/st-sdk/stsdk")
from stsdk.common.key import DMS_BBO
from stsdk.model.strategy_module import StrategyModule
from stsdk.utils.config import config
from stsdk.utils.log import log


class ST1(StrategyModule):
    name = "ST1"

    def init_params(self):
        log.info("ST1 init_params")
        self.register(
            DMS_BBO,
            self.handle_bbo,
            instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
        )
        self.register(
            DMS_BBO,
            self.handle_btc_bbo,
            instrument_id="EXCHANGE_BINANCE.BTC-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
        )
        # self.register(
        #     OMS_ORDER_UPDATE,
        #     self.handle_order_update,
        #     strategy_id=self.strategy_id,
        #     account_id=self.account_id,
        # )
        log.info("ST1 init_params")
        log.error("ST1 init_params")
        log.warning("ST1 init_params")
        log.debug("ST1 init_params")

    def start_trading_session(self):
        pass

    def run_on_data_feed(self, *args):
        pass

    def handle_error(self, error):
        print("error", error)
        # print("hello")
        pass

    def handle_bbo(self, message):
        # print("bbo", message)
        print("bbo", self.name)

    def handle_bbo(self, message):
        print(message)
        # log.info("bbo: %s" % message)
        # resp = self.place_order(
        #     "EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
        #     "1000",
        #     "1",
        #     "buy",
        #     "OPEN",
        # )
        # print(resp)

    def handle_btc_bbo(self, message):
        self.name = "btc update"
        print("btc bbo", self.name)
        # print("btc bbo", message)

    def handle_order_update(self, message):
        log.info(message)


async def main():
    st = ST1(config.strategy_id, config.account_id)
    time.sleep(1)
    # if __name__ == '__main__':
    # st = ST1("17", "test-future")
    # ST1("4", "aris_lingxiao_test")
    # resp = st.place_order(
    #     "EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
    #     "1000",
    #     "1",
    #     "buy",
    #     "OPEN",
    # )
    # if "orderId" in resp:
    #     print("success place order, order id is", resp["orderId"])
    # else:
    #     print("fail to place order, resp is", resp)
    # # print(st.get_all_open_orders())
    # time.sleep(30)
    # print("main --------------------------------------")
    # resp = st.cancel_order(resp["instrumentId"], resp["orderId"])
    # if "orderId" in resp:
    #     print("success cancel order, order id is", resp["orderId"])
    # else:
    #     print("fail to cancel order, resp is", resp)
    # print(st.get_all_open_orders())
    # print("main --------------------------------------")
    # print(st.get_all_positions())


if __name__ == "__main__":
    asyncio.run(main())
