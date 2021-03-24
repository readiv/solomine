import logger, nicehash, config
log = logger.get_logger(__name__)

public_api = nicehash.public_api(config.host, False)
private_api = nicehash.private_api(config.host, config.organisation_id, config.key, config.secret, False)

def start(market, type, algorithm, price, limit, amount, pool_id, algo_response):
    # 
    # create_hashpower_order(self, market, type, algorithm, price, limit, amount, pool_id, algo_response):
    pass

def stop_all():
    log.info("Stop all orders")
    active_orders = private_api.get_my_active_orders("OCTOPUS","ACTIVE","","100")["list"]
    for order in active_orders:
        private_api.cancel_hashpower_order(order["id"])
        log.info(f"order id = {order['id']} stoped")


if __name__ == "__main__":
    # pass
    start("EU","")