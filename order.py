#Запуск ордера
# 1. Считать баланс и зафиксировать его. Сумма на ордер 0,005
# 2. Определить максимальную цену от текущей сложности. Бот превышать её не должен. 
# 3. Определить начальную цену по рынку.
#      Идем снизу. И фиксируем цену, где больше 100 майнеров.
#      Запуск на этой цене и максимальной мощьностью. Фиксируем число майнеров в 0  

# #Задача добиться число майнеров
# 4. Каждые 60 секунд.
#      а. Проверяем число майнеров. Если упало больше чем на 50 процентов, 
#         то смотрим у кого выше больше 100 майнеров и ставим такую же цену. 
#      б. Идем снизу. И фиксируем цену, где больше 100 майнеров.
#         Если эта цена на 20 процентов меньше текущей цены ордера.
#         То отменяем его и делаем с этой ценой. 
          

import logger
log = logger.get_logger(__name__)

def start():
    # 
    # create_hashpower_order(self, market, type, algorithm, price, limit, amount, pool_id, algo_response):
    pass

def stop():
    pass