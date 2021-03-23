import requests, datetime, nicehash

import config, order
from db import db_session
from models import diff_new
from func import time2float

import logger
log = logger.get_logger(__name__)

public_api = nicehash.public_api(config.host, False)
private_api = nicehash.private_api(config.host, config.organisation_id, config.key, config.secret, False)

def get_api(url:str, wallet:str):
    url = url.replace(":wallet",wallet)

    response = requests.get(url, params={"format":"json"})

    if response.status_code != 200:
        log.info(f"Error. response.status_code = {response.status_code}")
        return None

    try:
        result = response.json()
        return result
    except:
        log.info(f"Error convert json. response.text = {response.text}")
        return None

def run_wallet(wallet):
    # time = time2int(datetime.datetime.now())
    time = time2float(datetime.datetime.now())
    print(time)
    live_stats = get_api("https://conflux.herominers.com/api/live_stats?address=:wallet", wallet)
    difficulty = int(live_stats["network"]["difficulty"])
    hash = 2 * difficulty
    max_price = 3.429604 - 0.00127 * difficulty / 1000000000
    diff_uno = diff_new(time = time,
                    difficulty = difficulty,
                    hash = hash,
                    max_price = max_price,
                    fix_EU_005 = private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 0.005)["fixedPrice"],
                    fix_EU_010 = private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 0.010)["fixedPrice"],
                    fix_EU_050 = private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 0.050)["fixedPrice"],
                    fix_EU_100 = private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 0.100)["fixedPrice"],
                    fix_EU_N_005 = private_api.get_hashpower_fixedprice("EU_N", "OCTOPUS", 0.005)["fixedPrice"],
                    fix_EU_N_010 = private_api.get_hashpower_fixedprice("EU_N", "OCTOPUS", 0.010)["fixedPrice"],
                    fix_EU_N_050 = private_api.get_hashpower_fixedprice("EU_N", "OCTOPUS", 0.050)["fixedPrice"],
                    fix_EU_N_100 = private_api.get_hashpower_fixedprice("EU_N", "OCTOPUS", 0.100)["fixedPrice"],
                    fix_USA_005 = private_api.get_hashpower_fixedprice("USA", "OCTOPUS", 0.005)["fixedPrice"],
                    fix_USA_010 = private_api.get_hashpower_fixedprice("USA", "OCTOPUS", 0.010)["fixedPrice"],
                    fix_USA_050 = private_api.get_hashpower_fixedprice("USA", "OCTOPUS", 0.050)["fixedPrice"],
                    fix_USA_100 = private_api.get_hashpower_fixedprice("USA", "OCTOPUS", 0.100)["fixedPrice"],
                    fix_USA_E_005 = private_api.get_hashpower_fixedprice("USA_E", "OCTOPUS", 0.005)["fixedPrice"],
                    fix_USA_E_010 =  private_api.get_hashpower_fixedprice("USA_E", "OCTOPUS", 0.010)["fixedPrice"],
                    fix_USA_E_050 =  private_api.get_hashpower_fixedprice("USA_E", "OCTOPUS", 0.050)["fixedPrice"],
                    fix_USA_E_100 =  private_api.get_hashpower_fixedprice("USA_E", "OCTOPUS", 0.100)["fixedPrice"])
    db_session.add(diff_uno)
    db_session.commit()
           
if __name__ == "__main__":
    while True:
        for wallet in config.wallets:
            run_wallet(wallet)
