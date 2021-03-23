import requests, datetime, nicehash, confluxscan

import config, order
from db import db_session
from models import diff
from func import time2int

import logger
log = logger.get_logger(__name__)

public_api = nicehash.public_api(config.host, False)
private_api = nicehash.private_api(config.host, config.organisation_id, config.key, config.secret, False)

hash_avg_arr = [0,0,0,0,0]

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

def parser():
    global hash_avg_arr
    time = time2int(datetime.datetime.now())
    # time = time2float(datetime.datetime.now())
    # print(time)
    # live_stats = get_api("https://conflux.herominers.com/api/live_stats?address=:wallet", wallet)
    # difficulty = int(live_stats["network"]["difficulty"])
    # hash = 2 * difficulty

    difficulty, hash_last, hash_avg = confluxscan.get_difficulty_hash(75)
    hash_avg_arr[-1] = hash_avg
    hash_avg3 = int(sum(hash_avg_arr)/len(hash_avg_arr))
    max_price = 2 * 1000000000000 * 172800 * 0.00001798 / hash_avg3
    # print(difficulty, hash_last, hash_avg, max_price)

    EU=  private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 0.005)
    EU_N =  private_api.get_hashpower_fixedprice("EU_N", "OCTOPUS", 0.005)
    USA =  private_api.get_hashpower_fixedprice("USA", "OCTOPUS", 0.005)
    USA_E =  private_api.get_hashpower_fixedprice("USA_E", "OCTOPUS", 0.005)

    if hash_avg_arr[0] != 0:
        diff_uno = diff(difficulty = difficulty,
                        hash_last = hash_last,
                        hash_avg = hash_avg3,
                        max_price = max_price,
                        EU_005 = EU["fixedPrice"],
                        EU_010 = private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 0.010)["fixedPrice"],
                        EU_050 = private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 0.050)["fixedPrice"],
                        EU_100 = private_api.get_hashpower_fixedprice("EU", "OCTOPUS", 0.100)["fixedPrice"],
                        EU_N_005 = EU_N["fixedPrice"],
                        EU_N_010 = private_api.get_hashpower_fixedprice("EU_N", "OCTOPUS", 0.010)["fixedPrice"],
                        EU_N_050 = private_api.get_hashpower_fixedprice("EU_N", "OCTOPUS", 0.050)["fixedPrice"],
                        EU_N_100 = private_api.get_hashpower_fixedprice("EU_N", "OCTOPUS", 0.100)["fixedPrice"],
                        USA_005 = USA["fixedPrice"],
                        USA_010 = private_api.get_hashpower_fixedprice("USA", "OCTOPUS", 0.010)["fixedPrice"],
                        USA_050 = private_api.get_hashpower_fixedprice("USA", "OCTOPUS", 0.050)["fixedPrice"],
                        USA_100 = private_api.get_hashpower_fixedprice("USA", "OCTOPUS", 0.100)["fixedPrice"],
                        USA_E_005 = USA_E["fixedPrice"],
                        USA_E_010 =  private_api.get_hashpower_fixedprice("USA_E", "OCTOPUS", 0.010)["fixedPrice"],
                        USA_E_050 =  private_api.get_hashpower_fixedprice("USA_E", "OCTOPUS", 0.050)["fixedPrice"],
                        USA_E_100 =  private_api.get_hashpower_fixedprice("USA_E", "OCTOPUS", 0.100)["fixedPrice"],
                        EU_N_p = EU_N["fixedMax"],
                        USA_p = USA["fixedMax"],
                        USA_E_p = USA_E["fixedMax"],
                        EU_p = EU["fixedMax"])
        db_session.add(diff_uno)
        db_session.commit()
    
    hash_avg_arr = hash_avg_arr[1:]+hash_avg_arr[:1]

           
if __name__ == "__main__":
    while True:
        with logger.Profiler() as p:
            parser()
