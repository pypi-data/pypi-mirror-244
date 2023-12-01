import json
import os

from stsdk.utils.consul import ConsulClient


class Config:
    def __init__(self, file_path):
        self.file_path = file_path
        self._load_config()
        address, token = self.consul_addr
        self.consul_client = ConsulClient(address, token)
        self._get_config_from_consul()

    def _load_config(self):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                self.api_endpoint = data.get("api_endpoint", {})
                self.env = data.get("env", "")
                self.consul = data.get("consul", {})
                self.log = data.get("log", {})
                self.strategy_module = data.get("strategy_module", {})
                print(f"Load config file success: {self.file_path}")
        except Exception as e:
            raise Exception(f"Error loading config file: {e}")

    def _get_config_from_consul(self):
        # self.consul_client.register_service("at-strategy", "7.7.7.7", 80)
        if self.env in ["test", "pre", "prod"]:
            self.api_endpoint = self.consul_client.get_api_endpoint()

    def __str__(self):
        return (
            f"API Endpoint: {self.api_endpoint}\n"
            f"Environment: {self.env}\n"
            f"Log Path: {self.log}\n"
            f"Strategy Module: {self.strategy_module}\n"
        )

    @property
    def DMS_BASE_HTTP_URL(self):
        return self.api_endpoint.get("http", {}).get("dms_base_url", "")

    @property
    def DMS_BASE_WS_URL(self):
        return self.api_endpoint.get("ws", {}).get("dms_base_ws", "")

    @property
    def OMS_BASE_HTTP_URL(self):
        return self.api_endpoint.get("http", {}).get("oms_base_url", "")

    @property
    def OMS_BASE_WS_URL(self):
        return self.api_endpoint.get("ws", {}).get("oms_base_ws", "")

    @property
    def ENV(self):
        return self.env

    @property
    def LOG_PATH(self):
        return self.log.get("path", "")

    @property
    def strategy_id(self):
        return self.strategy_module.get("strategy_id", "")

    @property
    def account_id(self):
        return self.strategy_module.get("account_id", "")

    @property
    def consul_test_addr(self):
        return self.consul.get("test_addr", "")

    @property
    def consul_pre_addr(self):
        return self.consul.get("pre_addr", "")

    @property
    def consul_prod_addr(self):
        return self.consul.get("prod_addr", "")

    @property
    def consul_prod_token(self):
        return self.consul.get("prod_token", "")

    @property
    def consul_addr(self):
        if self.ENV == "test":
            return self.consul_test_addr, ""
        elif self.ENV == "pre":
            return self.consul_pre_addr, ""
        elif self.ENV == "prod":
            return self.consul_prod_addr, self.consul_prod_token
        else:
            raise Exception("Error ENV")


config_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../config/config.json")
)

config = Config(config_path)
