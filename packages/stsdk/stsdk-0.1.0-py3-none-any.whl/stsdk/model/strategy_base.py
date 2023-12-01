import json
import threading
import types

from stsdk.api.ws.dms import DMSWS
from stsdk.api.ws.oms import OMSWS
from stsdk.common.key import DMS_SIGNAL_MAP, GLOBAL_SIGNAL, OMS_SIGNAL_MAP
from stsdk.utils.cache_manager import cache_manager
from stsdk.utils.instrument_id import expand_topic


class StrategyBaseModule:
    dms_ws = None
    oms_ws = None
    queue = None
    func_map = {}

    def __init__(self, strategy_id, account_id):
        self.strategy_id = strategy_id
        self.account_id = account_id
        self.exec_init_params()

    def exec_init_params(self):
        self.dms_ws = DMSWS()
        self.oms_ws = OMSWS()
        if self.dms_ws is None or self.oms_ws is None:
            raise Exception("ws not ready")
        if self.init_params is not None and isinstance(
            self.init_params, types.MethodType
        ):
            # init_params中注册数据流
            self.init_params()
            self.exec_start_trading_session()

    # 策略启动
    def exec_start_trading_session(self):
        if self.start_trading_session is not None and isinstance(
            self.start_trading_session, types.MethodType
        ):
            self.start_trading_session()
            self.exec_on_data_feed()
            threading.Thread(target=self.dms_ws.run, args=(self.consumer,)).start()
            threading.Thread(target=self.oms_ws.run, args=(self.consumer,)).start()

    # 持续数据流,提供总的数据开关
    def exec_on_data_feed(self):
        if self.run_on_data_feed is not None and isinstance(
            self.run_on_data_feed, types.MethodType
        ):
            GLOBAL_SIGNAL.connect(self.run_on_data_feed)

    def consumer(self, msg):
        self.publish_message(msg)

    def publish_message(self, message):
        msg = json.loads(message, parse_constant=True)
        GLOBAL_SIGNAL.send(msg)
        topic = msg.get("topic")
        topic_type = expand_topic(topic)
        dms_signal = DMS_SIGNAL_MAP.get(topic_type)

        if dms_signal is not None:
            dms_signal.send(msg)
        oms_signal = OMS_SIGNAL_MAP.get(topic_type)
        if oms_signal is not None:
            oms_signal.send(msg)

    def handle_dms_message(self, func, topic):
        def _handle_message(message):
            _topic = message.get("topic")
            if _topic == topic:
                cache_manager.set_cache_queue(topic, message)
                func(message)

        return _handle_message

    def handle_oms_message(self, func, topic):
        def _handle_message(message):
            _topic = message.get("topic")
            if _topic == topic:
                cache_manager.set_cache_queue(topic, message)
                func(message)

        return _handle_message

    def register(self, event, func, **kwargs):
        dms_signal = DMS_SIGNAL_MAP.get(event)
        oms_signal = OMS_SIGNAL_MAP.get(event)
        # 使用topic替代event作为function的connect参数逻辑，这样避免了重复注册，后置函数的注册会覆盖前置函数的注册
        if dms_signal is not None:
            instrument_id = kwargs["instrument_id"]
            topic = f"{event}.{instrument_id}"
            self.func_map[topic] = self.handle_dms_message(func, topic)
            dms_signal.connect(self.func_map[topic])
            method = getattr(self.dms_ws, event)
            method(instrument_id)

        # oms里面也会有一些事件，比如order的事件，这些事件也需要注册，但是需要的唯一id维度需要是其他的
        if oms_signal is not None:
            strategy_id = kwargs["strategy_id"]
            account_id = kwargs["account_id"]
            topic = f"{event}.{strategy_id}.{account_id}"
            self.func_map[event] = self.handle_oms_message(func, topic)
            oms_signal.connect(self.func_map[event])
            method = getattr(self.oms_ws, event)
            method(strategy_id, account_id)
