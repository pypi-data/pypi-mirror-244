def generator_instrument_id(
    exchange, symbol, security_type, contract_type, settle_ccy, expiry_date
):
    instrument_id = f"{exchange}.{symbol}.{security_type}.{contract_type}.{settle_ccy}.{expiry_date}"
    return instrument_id


def expand_instrument_id(instrument_id):
    (
        exchange,
        symbol,
        security_type,
        contract_type,
        settle_ccy,
        expiry_date,
    ) = instrument_id.split(".")
    return {exchange, symbol, security_type, contract_type, settle_ccy, expiry_date}


def expand_topic(topic):
    topic_type = topic.split(".")[0]
    return topic_type
