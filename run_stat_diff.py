import requests, datetime, nicehash

import config, order
from db import db_session
from models import diff
from func import time2int

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
    time = time2int(datetime.datetime.now())
    live_stats = get_api("https://conflux.herominers.com/api/live_stats?address=:wallet", wallet)
    difficulty = int(live_stats["network"]["difficulty"])
    max_price = 3.429604 - 0.00127 * difficulty / 1000000000
    resp = private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 0.001)
    speed = resp["fixedMax"]
    fix_001 = resp["fixedPrice"]
    fix_005 = private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 0.005)["fixedPrice"]
    fix_008 = private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 0.008)["fixedPrice"]
    fix_009 = private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 0.009)["fixedPrice"]
    fix_010 = private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 0.010)["fixedPrice"]
    fix_050 = private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 0.050)["fixedPrice"]
    fix_100 = private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 0.100)["fixedPrice"]
    fix_500 = private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 0.500)["fixedPrice"]
    fix_999 = private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 1.000)["fixedPrice"]

    diff_uno = diff(time = time,
                    difficulty = difficulty,
                    max_price = max_price,
                    speed = speed,
                    fix_001 = fix_001,
                    fix_005 = fix_005,
                    fix_008 = fix_008,
                    fix_009 = fix_009,
                    fix_010 = fix_010,
                    fix_050 = fix_050,
                    fix_100 = fix_100,
                    fix_500 = fix_500,
                    fix_999 = fix_999)
    db_session.add(diff_uno)
    db_session.commit()

            
if __name__ == "__main__":
    while True:
        for wallet in config.wallets:
            difficulty = run_wallet(wallet) 

