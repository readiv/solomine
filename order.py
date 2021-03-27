import config
from requests.models import Response
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
        if config.no_order:
            return True
        response = private_api.create_hashpower_order(market, type_order, algorithm, price, limit, amount, pool_id, algo_response)
        if response is None:
            new_price = float(private_api.get_hashpower_fixedprice(market, algorithm, limit)["fixedPrice"])
            if 100 * abs(new_price/new_price -1) <=5: #Цена изменилась не более чем на 5 процентов
                response = private_api.create_hashpower_order(market, type_order, algorithm, new_price, limit, amount, pool_id, algo_response)

        return response
    except Exception as e:
        log.error(str(e))
        return None


def stop_all(algorithm:str = "", max_price = 0):
    log.info("Stop all orders")
    try:
        active_orders = private_api.get_my_active_orders(algorithm,"ACTIVE","","100")["list"]
        for order in active_orders:
            if float(order["price"]) > max_price:
                if not config.no_order:
                    private_api.cancel_hashpower_order(order["id"])
                log.info(f"order id = {order['id']} stoped")
        active_orders = private_api.get_my_active_orders(algorithm,"ACTIVE","","100")["list"]
        if len(active_orders) > 0:
            return True
        else:
            return None
        # return True
    except Exception as e:
        log.error(str(e))
        return None

if __name__ == "__main__":
    # pass
    print(start("EU","STANDARD", config.algorithm, 1, 0.001, 0.001))
    # stop_all()
    # get_pool_id("EU_N",config.algorithm)