import requests, sys, datetime

from db import db_session
from models import herro

import logger
log = logger.get_logger(__name__)

# https://conflux.herominers.com/api/live_stats?address=cfx%3Aaaj1mzzem5cvefbxfb724x1rss70r9dd4ydwkt3zya
# https://conflux.herominers.com/api/stats_address?address=cfx%3Aaaj1mzzem5cvefbxfb724x1rss70r9dd4ydwkt3zya&recentBlocksAmount=20&longpoll=true

# Поля для сохранения
# 1. Time Found - Время
# 2. Height - Высота блока
# 3. Difficulty - Сложность	
# 3. Region - Регион
# 6. Block Reward - Награда за блок
# 7. Reward - Награда за минусом комиссии
# 8. Hash Rate - текущий хэшь-рейт
# https://conflux.herominers.com/api/stats_address?address=:wallet&recentBlocksAmount=20&longpoll=true

def get_stat(wallet:str):
    url = "https://conflux.herominers.com/api/stats_address?address=:wallet&recentBlocksAmount=20&longpoll=true"
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

def int2time(time:int):
    time_since = datetime.datetime(1970, 1, 1, 1) + datetime.timedelta(seconds=time)
    return time_since

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

def reward2float(reward:str):
    while len(reward)<19:
        reward = "0" + reward
    reward = reward[:1] + "." + reward[1:9]
    return float(reward)

def run_wallet(wallet):
    s_json = get_stat(wallet)
    if s_json is None:
        return
    hash_rate = s_json["stats"]["hashrate"]
    unlockeds = s_json["unlocked"]

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
            # else:
            #      print("===", rec_exists, wallet, time_found, height, difficulty, region, block_reward, reward)
            

if __name__ == "__main__":
    while True:
        run_wallet("cfx:aaj1mzzem5cvefbxfb724x1rss70r9dd4ydwkt3zya") 
        # run_wallet("cfx:aaphu29ca7d77t09u84nwhhdrc3wa6uv1u8u96nsk3")
        # run_wallet("0x14946738c0fdce02e089448d6aa2e5ae1e931fc4")
        # run_wallet("cfx:aapf4ckvkjyxxbfyxsrbjpf1j1z1v1m52eghv468zx")
        # run_wallet("0x1a2a96b3166c51B216321CBEf0E266Ff67986162")
        # run_wallet("cfx:aapt5t080rafg7cky09tn73wc5wnnszv8a566uwunk")
        # run_wallet("0x11efed3847b7a2c081432a28fbfbe7d28e7b3b24")
        # run_wallet("cfx:aak1cvc55r8w9p7c5x3ywdrmf4advdw6uuky0u75z6")
        # run_wallet("0x1AcdD76Fe6B3bF5629726F9D5416Fe68032eC91b")
        # run_wallet("0x1282201025212947e1bff605b0d0d7846c49dbe9")
