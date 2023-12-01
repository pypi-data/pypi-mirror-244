import requests

from loguru import logger

create_account_end_points = "http://{host}:6002/account/new".format(host="47.91.25.224")
get_account_end_points = "http://{host}:6002/account/account_id".format(host="47.91.25.224")

post_strategy_end_points = "http://{host}:6002/strategy/new".format(host="47.91.25.224")
get_strategy_end_points = "http://{host}:6002/strategy/strategy_id".format(host="47.91.25.224")

if __name__ == "__main__":

    account_info = {
        "account_id":"aris_lingxiao_test", 
        "exchange":1,           
        "security_type":[1,2,3],
        "contract_type":[1,2],   
        "balance":"500",
        "dual_size_position":"",
        "multi_asset_margin":False,
        "api_key":"",
        "api_secret":"",
        "ip_white_list":[]
    }

    r = requests.post(url=create_account_end_points, data=account_info)
    logger.info(r.text)

    param = {"account_id": "aris_lingxiao_test"}
    r = requests.get(get_account_end_points, params=param)
    logger.info(r.json())

    strategy_info = {
    "strategy_id": "test_sdk",
    "symbol_list": [
        "ETHUSDTPERP",
        "BTCUSDTPERP",
        "INCHUSDTPERP",
        "ALGOUSDTPERP",
        "ARUSDTPERP",
        "ATOMUSDTPERP",
        "BATUSDTPERP",
        "BCHUSDTPERP",
        "CELOUSDTPERP",
        "COMPUSDTPERP",
        "EGLDUSDTPERP",
        "ENJUSDTPERP",
        "EOSUSDTPERP",
        "ETCUSDTPERP",
        "FLOWUSDTPERP",
        "HOTUSDTPERP",
        "LINKUSDTPERP",
        "LTCUSDTPERP",
        "NEARUSDTPERP",
        "NEOUSDTPERP",
        "THETAUSDTPERP",
        "VETUSDTPERP",
        "XEMUSDTPERP",
        "XLMUSDTPERP",
        "XMRUSDTPERP",
        "XTZUSDTPERP",
        "ZECUSDTPERP",
        "ZILUSDTPERP"
        ],
        "name": "test_data_strategy",
        "is_both": False,
        "account_ids": [
            "aris_lingxiao_test"
        ],
        "create_time": "1700120046222",
        "update_time": "1700120046222",
        "status": 1,
        "initial_balance": "",
        "balance": "",
        "pnl_ratio": "",
        "total_pnl": "",
        "open_pnl": "",
        "trade_pnl": "",
        "leverage": "",
        "total_cash_exposure": "",
        "total_position_value": ""
    }

    r = requests.post(url=post_strategy_end_points, data=strategy_info)
    logger.info(r.text)

    param = {"strategy_id": "4"}
    r = requests.get(get_strategy_end_points, params=param)
    logger.info(r.json())