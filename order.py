import logger, nicehash, config
log = logger.get_logger(__name__)

public_api = nicehash.public_api(config.host, False)
private_api = nicehash.private_api(config.host, config.organisation_id, config.key, config.secret, False)

# req: [94b48f86 - 80a6 - 4290 - 9751 - cbf615f5af98 1616632387279 c6cb3fd2 - e19d - 421a - 9c7f - 1424b25ac77e 18669311 - 1e7c - 43c9 - 9d4d - 96ec60c62b22 POST / main / api / v2 / hashpower / order
#     {
#         "algorithm": "SCRYPT",
#         "amount": "0.001",
#         "`displayMarketFactor`": "TH",
#         "limit": "0.01",
#         "market": "EU",
#         "marketFactor": "1000000000000",
#         "poolId": "cfcfee1e-dd9a-4d4f-9859-5be0a9ccfa6c",
#         "price": "1",
#         "type": "STANDARD"
#     }

def get_pool_id():
    pass

def start(market, type_order, algorithm, price, limit, amount):
    try:
        algo_response = public_api.get_algorithms()
        # pool_id = get_pool_id(market, algorithm)
        # return private_api.create_hashpower_order(market, type_order, algorithm, price, limit, amount, pool_id, algo_response)
    except Exception as e:
        log.error(str(e))
        return None


def stop_all(algorithm:str = ""):
    log.info("Stop all orders")
    try:
        active_orders = private_api.get_my_active_orders(algorithm,"ACTIVE","","100")["list"]
        for order in active_orders:
            print(private_api.cancel_hashpower_order(order["id"]))
            log.info(f"order id = {order['id']} stoped")
        return True
    except Exception as e:
        log.error(str(e))
        return None


if __name__ == "__main__":
    # pass
    # print(start("EU","STANDARD", "SCRYPT", 1, 0.01, 0.001, "cfcfee1e-dd9a-4d4f-9859-5be0a9ccfa6c"))
    stop_all()