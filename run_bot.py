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

import logger, nicehash, config, confluxscan, time
log = logger.get_logger(__name__)

public_api = nicehash.public_api(config.host, False)
private_api = nicehash.private_api(config.host, config.organisation_id, config.key, config.secret, False)

if __name__ == "__main__":
    price_BTC = float(get_api("https://conflux.herominers.com/api/get_market?tickers%5B%5D=CFX-BTC")[0]["price"])
    deff_prev = confluxscan.get_difficulty()
    deadline = time.monotonic() - 60
    while True:
        balance_available = float(private_api.get_accounts_for_currency("BTC")["available"])
        if balance_available < 0.001:
            time.sleep(10)
            continue

        print(balance_available, deff_prev)
        break


    