from func import get_api

import logger, config, confluxscan, time, order
log = logger.get_logger(__name__,"z.log")

from order import private_api, public_api

markets = ["EU","EU_N","USA","USA_E"]

def get_power(x1,y1,x2,y2,max_price,market,depth):
    x = (x1 + x2) / 2
    y = float(private_api.get_hashpower_fixedprice(market, "OCTOPUS", x )["fixedPrice"])
    if y == 0:
        return 0
    if depth == 0:
        return x
    if y <= max_price:
        return get_power(x,y,x2,y2,max_price,market,depth - 1)
    else:
        return get_power(x1,y1,x,y,max_price,market,depth - 1)

if __name__ == "__main__":
    log.info("======================== Start =========================")
    while True:
        deff_prev = confluxscan.get_difficulty()
        if deff_prev != 0:
            break
    deadline_order = deadline_price = 0
    deff_prev = 5951776704553

    while True:
        n = 0
        balance_available = float(private_api.get_accounts_for_currency("BTC")["available"])
        while balance_available < 0.001:
            if n % 30 == 0:
                log.info(f"Balance is close to zero. balance_available = {balance_available}")
            time.sleep(10)
            balance_available = float(private_api.get_accounts_for_currency("BTC")["available"])
            n += 1
        if n != 0:
            log.info(f"balance_available = {balance_available} BTC")

        deff = confluxscan.get_difficulty()
        if deff == 0:
            log.error(f"difficulty = 0")
            continue

        if deff > 1.20 * deff_prev: #Сложность повысилась очень значительно. Стоп все ордера.
            log.info(f"The difficulty has increased. Stop all orders. deff = {deff} deff_prev = {deff_prev}")
            order.stop_all("OCTOPUS")
            markets = ["EU","EU_N","USA","USA_E"]           #Восстанавливаем список рынков
            deadline_order = time.monotonic() + 60*75     #Ставим таймер на 75 минут
            deadline_price = time.monotonic() + 60*5    #Ставим таймер на  минут
            deff_prev = deff

        if deadline_price != 0 and (time.monotonic()>deadline_price) and len(markets) > 0: #Запоминаем цены.
            price_001 = {} #Запоминаем значения цен на рынке при 0.001. Среднее арифметическое 4-х цен с интервалом 3 минуты 
            for market in markets:
                price_001[market] = 0.0
            n = 1
            flag_err = False
            for i in range(n):
                print(f"i = {i}")
                for market in markets:
                    for _ in range(5): #5 попыток запроса
                        price_temp = float(private_api.get_hashpower_fixedprice(market, "OCTOPUS", 0.001)["fixedPrice"])
                        if price_temp != 0:
                            break
                        # time.sleep(30)
                    if price_temp == 0:
                        log.error(f"Initial price request error: fixedprice = 0")
                        flag_err = True
                        break
                    # print(f"price_001[market] = {price_001[market]} price_temp = {price_temp}")
                    price_001[market] = price_001[market] + price_temp
                if flag_err:
                    break
                # time.sleep(150)
            if flag_err:
                continue
            for market in markets:
                price_001[market] = price_001[market] / n
            log.info(f"price_001 = {price_001}") 
            deadline_price = 0
                            
        if deff < 0.9 * deff_prev: #Сложность Понизилась
            log.info(f"Difficulty has dropped. deff = {deff} deff_prev = {deff_prev}")
            deadline_order = 0 #Если какие то ордера выставить не удалось, то прекращаем эти попытки

        if (deadline_order != 0) and (deadline_price == 0) and (time.monotonic() > deadline_order) and len(markets) > 0: #сработал таймер, выставляем ордера
            log.info("************************* deadline ***************************")
            price = {}
            for _ in range(5): #5 попыток запроса c паузой 30 сек
                price_BTC = float(get_api("https://conflux.herominers.com/api/get_market?tickers%5B%5D=CFX-BTC")[0]["price"])
                if price_BTC != 0:
                    break
                time.sleep(30)
            if (price_BTC is None) or (price_BTC == 0):
                log.error(f"price_BTC = 0")
                continue 
            for market in markets: #Определяем максимальную цену для каждого маркета
                price[market] = (100 + config.extra_charge_price_power) * price_001[market] / 100                
                max_price = (100 + config.extra_charge_price_estimated) * 1000000000000 * 172800 * price_BTC / deff / 100
                if max_price < price[market]:
                    price[market] = max_price
            # print(f"максимальные цены {price}")
            #Максимальная цена определена. Теперь нужно определить мощьность.
            markets_w = markets.copy()
            for market in markets_w:
                log.info(f"*** An attempt to place an order on the market {market}")
                temp = private_api.get_hashpower_fixedprice(market, "OCTOPUS", 0.001) 
                x1 = 0.001
                x2 = 0.95*float(temp["fixedMax"])
                y1 = float(temp["fixedPrice"])
                y2 = float(private_api.get_hashpower_fixedprice(market, "OCTOPUS", x2)["fixedPrice"])
                if x2 == 0 or y1 == 0 or y2 == 0 or y1 > price[market]:
                    log.error(f"Error: x2:{x2} == 0 or y1:{y1} == 0 or y2:{y2} == 0 or y1:{y1} > price[market]:{price[market]}")
                    continue
                if y2 < price[market]:
                    power = 2 * x2 / 3
                else:
                    power = round(2*get_power(x1,y1,x2,y2,price[market],market,5)/3,3)
                if power == 0:
                    log.error(f"power:{power} == 0")
                    continue

                price_power = float(private_api.get_hashpower_fixedprice(market, "OCTOPUS", power)["fixedPrice"])

                # log.info(f"it should be: power={power}. price_power={price_power} amount{power * price_power * 3 / 24}")
                # power = 0.001 #пока ограничим мощьность
                # price_power = float(private_api.get_hashpower_fixedprice(market, "OCTOPUS", power)["fixedPrice"])
                
                amount = power * price_power * 3 / 24 #Из рассчета что бы хватило на 3 часа
                balance_available = float(private_api.get_accounts_for_currency("BTC")["available"])
                if amount<0.001:
                    amount = 0.001
                if balance_available < 0.001: 
                    log.error(f"Balance is close to zero. amount= {amount} balance_available = {balance_available}")
                    break
                if amount > balance_available:
                    power = 0.99 * power * balance_available / amount
                    price_power = float(private_api.get_hashpower_fixedprice(market, "OCTOPUS", power)["fixedPrice"])

                if order.start(market, "FIXED", "OCTOPUS", price_power, power, amount) is not None:
                    log.info(f"Order create: {market}: power = {power} price_power = {price_power} amount ={amount}")
                    markets.remove(market) #Удаляем этот рынок, т.к. ордер для него выставили
                
            if len(markets) == 0: 
                deadline_order = 0

        deff_prev = deff
        time.sleep(1)






    