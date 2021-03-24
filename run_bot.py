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

def get_power(x1,y1,x2,y2,max_price,market,depth):
    x = (x1 + x2) / 2
    y = float(private_api.get_hashpower_fixedprice(market, "OCTOPUS", x )["fixedPrice"])
    if y == 0:
        return 0
    if depth == 6:
        return x
    if y <= max_price:
        return get_power(x,y,x2,y2,max_price,market,depth + 1)
    else:
        return get_power(x1,y1,x,y,max_price,market,depth + 1)

if __name__ == "__main__":
    
    deff_prev = confluxscan.get_difficulty()
    deadline = 0
    while True:
        balance_available = float(private_api.get_accounts_for_currency("BTC")["available"])
        if balance_available < 0.001:
            time.sleep(10)
            continue

        deff = confluxscan.get_difficulty()
        # print(f"deff_prev = {deff_prev} deff = {deff}")
        if deff > 1.1 * deff_prev: #Сложность повысилась. Стоп все ордера.
            log.info(f"deff > 1.1 * deff_prev deff_prev = {deff_prev} deff = {deff}")
            order.stop_all()
            markets = ["EU","EU_N","USA","USA_E"]
            deadline = 0

        # if deff < 0.9 * deff_prev: #Сложность Понизилась
        if (deadline == 0):
            markets = ["EU","EU_N","USA","USA_E"] #хз. На всякий случай
            price_001 = {} #Запоминаем значения цен на рынке при 0.001
            for market in markets:
                price_001[market] = float(private_api.get_hashpower_fixedprice(market, "OCTOPUS", 0.001)["fixedPrice"])
            log.info(f"deff < 0.9 * deff_prev deff_prev = {deff_prev} deff = {deff}")
            print(price_001)
            deadline = time.monotonic() + 15 #75*60     #Ставим таймер на 75 минут

        if (deadline != 0) and (time.monotonic()>deadline): #сработал таймер
            log.info(f"time.monotonic() = {time.monotonic()} deadline = {deadline}")
            price = {}
            price_BTC = float(get_api("https://conflux.herominers.com/api/get_market?tickers%5B%5D=CFX-BTC")[0]["price"])
            for market in markets: #Определяем максимальную цену для каждого маркета
                price[market] = (100 + config.extra_charge_price_power) * price_001[market] / 100                
                max_price = (100 + config.extra_charge_price_estimated) * 1000000000000 * 172800 * price_BTC / deff / 100
                if max_price < price[market]:
                    price[market] = max_price
            print(f"максимальные цены {price}")
            #Максимальная цена определена. Теперь нужно определить мощьность.
            markets_w = markets.copy()
            for market in markets_w:
                temp = private_api.get_hashpower_fixedprice(market, "OCTOPUS", 0.001) 
                x1 = 0.001
                x2 = 0.95 * float(temp["fixedMax"])
                y1 = float(temp["fixedPrice"])
                y2 = float(private_api.get_hashpower_fixedprice(market, "OCTOPUS", x2)["fixedPrice"])
                if x2 == 0 or y1 == 0 or y2 == 0 or y1 > price[market]:
                    continue
                if y2 < price[market]:
                    power = x2
                else:
                    power = round(get_power(x1,y1,x2,y2,price[market],market,1),3)
                if power == 0:
                    continue
                price_power = float(private_api.get_hashpower_fixedprice(market, "OCTOPUS", power)["fixedPrice"])
                print(f"Выставляем ордер {market}: power = {power} price_power = {price_power}")
                markets.remove(market) #Удаляем этот рынок, т.к. ордер для него выставили
            deadline = 0

        deff_prev = deff
        time.sleep(1)






    