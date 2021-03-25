import requests, confluxscan

import config, order
from db import db_session
from models import herro
from func import reward2float, get_api


import logger
log = logger.get_logger(__name__)


def add_db(block_hash:str, height:int, wallet:str, difficulty:int, time_found:int, region:str, block_reward:float, reward:float, hash_rate:int):
    rec_exists = herro.query.filter(herro.block_hash == block_hash and herro.wallet == wallet).count()
    if not rec_exists:
        stat = herro(block_hash=block_hash,
                     height = height, 
                     wallet = wallet, 
                     difficulty = difficulty, 
                     time_found = time_found,
                     region = region, 
                     block_reward = block_reward, 
                     reward = reward, 
                     hash_rate = hash_rate)
        db_session.add(stat)
        db_session.commit()
    return rec_exists


def run_wallet(wallet):
    stats_address = get_api("https://conflux.herominers.com/api/stats_address?address=:wallet&recentBlocksAmount=20&longpoll=true", wallet)
    if stats_address is None:
        return
    hash_rate = stats_address["stats"]["hashrate"]
    unlockeds = stats_address["unlocked"]

    for unlocked in unlockeds:
        text = unlocked.split(":")
        if len(text) != 1:
            block_hash = text[1]
            height = int(text[0])
            difficulty = int(text[2])
            region = text[10]
            block_reward = reward2float(text[3])
            reward = reward2float(text[4])
        else:
            time_found = int(unlocked)
            rec_exists = add_db(block_hash, height, wallet, difficulty, time_found, region, block_reward, reward, hash_rate)
            if rec_exists == 0:
                log.info(f"{wallet} {time_found} {height} {difficulty} {region} {block_reward} {reward}")
    difficulty = confluxscan.get_difficulty()
    # live_stats = get_api("https://conflux.herominers.com/api/live_stats?address=:wallet", wallet)
    return difficulty
            

if __name__ == "__main__":
    while True:
        for wallet in config.wallets:
            difficulty = run_wallet(wallet) 
            # log.info(f"difficulty = {difficulty}")

