import logger, nicehash, config
log = logger.get_logger(__name__,"z.log")

public_api = nicehash.public_api(config.host, False)
private_api = nicehash.private_api(config.host, config.organisation_id, config.key, config.secret, False)

def get_pool_id(market, algorithm):
    try:
        pools = private_api.get_my_pools("page", 100)["list"]
        for pool in pools:
            if pool["algorithm"] == algorithm:
                if pool["name"].split(":")[0] == market:
                    return pool["id"]
    except Exception as e:
        log.error(str(e))
    return None

def start(market, type_order, algorithm, price, limit, amount):
    try:
        algo_response = public_api.get_algorithms()
        pool_id = get_pool_id(market, algorithm)
        log.info(f"market={market}, pool_id={pool_id}")
        return private_api.create_hashpower_order(market, type_order, algorithm, price, limit, amount, pool_id, algo_response)
        # return True
    except Exception as e:
        log.error(str(e))
        return None


def stop_all(algorithm:str = ""):
    log.info("Stop all orders")
    try:
        active_orders = private_api.get_my_active_orders(algorithm,"ACTIVE","","100")["list"]
        for order in active_orders:
            # print(private_api.cancel_hashpower_order(order["id"]))
            log.info(f"order id = {order['id']} stoped")
        return True
    except Exception as e:
        log.error(str(e))
        return None

if __name__ == "__main__":
    # pass
    # print(start("EU","STANDARD", "SCRYPT", 1, 0.01, 0.001, "cfcfee1e-dd9a-4d4f-9859-5be0a9ccfa6c"))
    # stop_all()
    get_pool_id("EU_N","OCTOPUS")