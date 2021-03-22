import requests

import config, order
from db import db_session
from models import herro
from func import reward2float


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

#Нужна таблица
# 1. time - Время
# 1. difficulty - Текущая сложнось
# 2. max_price - Максимальная цена профитности. 
# 3. speed_XXX - Доступная скорость по каждомц рынку "EU", "USA", "EU_N", "USA_E"
# 3. fix_0_001 - Цена фиксированого ордера при мощьности 0.001,0.008,0.009,0.01,0.05,0.1,0.5,1.0 

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
    live_stats = get_api("https://conflux.herominers.com/api/live_stats?address=:wallet", wallet)
    return int(live_stats["network"]["difficulty"])
            

if __name__ == "__main__":
    while True:
        for wallet in config.wallets:
            difficulty = run_wallet(wallet) 
            if difficulty < config.limit_difficulty:
                order.start()
            else:
                order.stop()
            log.info(f"difficulty = {difficulty}")

