import datetime, config
import requests, datetime

import logger
log = logger.get_logger(__name__)

def get_difficulty_test():

    m = (datetime.datetime.now().minute + 0) // 3 #Период минут
    if m % 2 == 0:
        return 2487270397017
    else:
        return 3205210279056
        
def get_difficulty_production():
    """ Получает значения сложности и последнего и среднего хэшрейта для 
        n_for_avg блоков сети. Либо None, если что то пошло не так
    """
    try:
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
        return difficulty
    except Exception as e:
        log.error(str(e))
        return 0

def get_difficulty():
    if not config.diff_real:
        return get_difficulty_test()
    else:
        return get_difficulty_production()


if __name__ == "__main__":
    with logger.Profiler() as p:
        difficulty = get_difficulty()
        print(difficulty)