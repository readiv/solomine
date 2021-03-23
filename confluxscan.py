# Список блоков
# https://www.confluxscan.io/v1/block?limit=1&skip=0
# {
#     "total": 26291540,
#     "list": [
#         {
#             "epochNumber": 10846654,
#             "hash": "0xf5d0f41c210132a81185ef956519f0e7674da239d2b60de8bd600ddb2b00e9c7",
#             "miner": "CFX:TYPE.USER:AAPKCJR28DG976FZR43C5HF1RWN5XV8T1UY4R2YYEU",
#             "gasLimit": "30000000",
#             "difficulty": "2229128559967",
#             "timestamp": 1616515868,
#             "transactionCount": 1,
#             "avgGasPrice": "100",
#             "blockIndex": 1,
#             "pivotHash": "0xf5d0f41c210132a81185ef956519f0e7674da239d2b60de8bd600ddb2b00e9c7",
#             "syncTimestamp": 1616515868,
#             "gasUsed": "434834"
#         }
#     ]
# }
# https://www.confluxscan.io/v1/plot?interval=1&limit=20
# {
#     "total": 2,
#     "list": [
#         {
#             "timestamp": "1616516113",
#             "tps": "0",
#             "difficulty": "2229128559967",
#             "blockTime": "0.3333333333333333",
#             "hashRate": "6687385679901.0000003625239041198558"
#         },
#         {
#             "timestamp": "1616516114",
#             "tps": "1",
#             "difficulty": "2229128559967",
#             "blockTime": "0.3333333333333333",
#             "hashRate": "6687385679901.0000003625239041198558"
#         }
#     ]
# }

import requests, random

import logger
log = logger.get_logger(__name__)

def get_difficulty_hash(n_for_avg:int = 20):
    """ Получает значения сложности и последнего и среднего хэшрейта для 
        n_for_avg блоков сети. Либо None, если что то пошло не так
    """
    if n_for_avg > 100 or n_for_avg < 1:
        n_for_avg = 100

    n_for_req = random.randint(60,100)
    if n_for_avg > n_for_req:
        n_for_avg = n_for_req

    try:
        url = "https://www.confluxscan.io/v1/plot?interval=1&limit=:n_for_req"
        url = url.replace(":n_for_req",str(n_for_req))
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"server error. response.status_code = {response.status_code}")
        tjson = response.json()["list"]
        # Определяем hash_last
        for item in reversed(tjson):
            hash_last = int(str(tjson[-1]["hashRate"]).split(".")[0])
            if hash_last != 0:
                break
        if hash_last == 0:
            raise Exception(f"Error. hash_last = {hash_last}")
        # Считаем средний хэшрейт
        n = 0
        sum_h = 0
        for item in tjson:
            hash = int(str(item["hashRate"]).split(".")[0])
            if hash != 0:
                n += 1
                sum_h += hash
            if n == n_for_avg:
                break
        if n == 0:
            raise Exception("All hashes are 0")
        hash_avg = int(sum_h/n)
        if hash_avg == 0:
            raise Exception(f"Error. hash_avg = {hash_avg}")
        # Получаем сложность из последнего блока
        difficulty = 0
        url = "https://www.confluxscan.io/v1/block?limit=3&skip=1"
        for _ in range(5): 
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"server error. difficulty request. response.status_code = {response.status_code}")
            tjson = response.json()["list"]        
            for item in tjson:
                difficulty = int(str(item["difficulty"]).split(".")[0])
                if difficulty != 0:
                    break
            if difficulty != 0:
                break
        if difficulty == 0:
            raise Exception(f"Error. difficulty = {difficulty}")

        # print(tjson, difficulty, hash_last, hash_avg)
        return difficulty,hash_last,hash_avg
    except Exception as e:
        log.error(str(e))
        return None, None, None

if __name__ == "__main__":
    with logger.Profiler() as p:
        difficulty, hash_last, hash_avg = get_difficulty_hash()
        print(difficulty, hash_last, hash_avg)