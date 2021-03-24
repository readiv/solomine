# Считываем баланс.
# Если меньше 0,001 то пауза одна минута
# Считываем начальную сложность и ставим её в deff_prev
# Ставим таймер в прошлое

# while True:
#     Считываем сложность. 
#     Если повысилась от deff_prev на 10%
#         Стоп все ордера
#     Если понизилась, 
#         Запоминаем значения цен на рынке
#         Ставим таймер на 75 минут
#     Если сработал таймер.
#         Ставим фикс ордера если цена на рынке отличаеться не больше 10 процентов от запомненой вначале и рассчетной
#         Мощьность в фикс ордере увеличиваем, пока условие выше не перестанет выполняться. И не должно 
#         превышать 5 процентов от цены при минимальной мощьности.
#         Обьем ордера ставим, что бы хватило на 3 часа

from func import get_api

import logger, nicehash, config, confluxscan, time, order
log = logger.get_logger(__name__)

from order import private_api, public_api

markets = ["EU","EU_N","USA","USA_E"]

if __name__ == "__main__":
    price_BTC = float(get_api("https://conflux.herominers.com/api/get_market?tickers%5B%5D=CFX-BTC")[0]["price"])
    deff_prev = confluxscan.get_difficulty()
    deadline = 0
    while True:
        balance_available = float(private_api.get_accounts_for_currency("BTC")["available"])
        if balance_available < 0.001:
            time.sleep(10)
            continue

        deff = confluxscan.get_difficulty()
        # log.info(f"deff_prev = {deff_prev} deff = {deff}")
        if deff > 1.1 * deff_prev: #Сложность повысилась. Стоп все ордера.
            log.info(f"deff > 1.1 * deff_prev deff_prev = {deff_prev} deff = {deff}")
            order.stop_all()
            deadline = 0

        if deff < 0.9 * deff_prev: #Сложность Понизилась
            power = {} #Запоминаем значения цен на рынке при 0.001
            for market in markets:
                power[market] = float(private_api.get_hashpower_fixedprice(market, "OCTOPUS", 0.001)["fixedPrice"])
            log.info(f"deff < 0.9 * deff_prev deff_prev = {deff_prev} deff = {deff}")
            deadline = time.monotonic() + 75*60     #Ставим таймер на 75 минут

        if (deadline != 0) and (time.monotonic()>deadline): #сработал таймер
            log.info(f"time.monotonic() = {time.monotonic()} deadline = {deadline}")
            # for market in markets:
            #     power_test = 0.001
            #     hashpower_fixedprice = private_api.get_hashpower_fixedprice(market, "OCTOPUS", 0.001)
            #     fixedPrice = float(hashpower_fixedprice["fixedPrice"])
            #     fixedMax = float(hashpower_fixedprice["fixedMax"])
            #     while (fixedPrice != 0) and (power_test < fixedMax):
            #         power_test += 0.001 
        time.sleep(1)





    