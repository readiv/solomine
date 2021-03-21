import csv
import datetime
import random

cfx_btc = 0.00000782
precio = 2.2235 #Цена за гигахэшь в сутки
Límite = 0.002 
monto = 0.004 #Максимальная трата. 
comision = 3.388 #Комиссия найсхэш Примерно 3 процента
velocidad_BTC_s = precio / 86400 * Límite
max_count_s = int( monto * (100 - comision) / 100/ velocidad_BTC_s)

random.seed()

solo = [] 
with open('solo.csv', newline='') as File:  
    reader = csv.reader(File, delimiter='\t')
    for row in reader:
        if row[0][2] != '.':
            continue

        dt = datetime.datetime.strptime(row[0],'%d.%m.%Y, %H:%M:%S')
        pais = row[3]
        cfx = float(row[6][:8])

        solo.append([dt, pais, cfx])

solo.sort(key=lambda x: x[0])
dt = solo[0][0]

for row in solo:
    row[0] = (row[0] - dt).seconds + 120

# for row in solo:
#     print(row)

balans = - monto * comision / 100
ts = random.randint(0, solo[-1][0] - 1)
te = ts + max_count_s
if te>solo[-1][0]:
    te = solo[-1][0]

print(ts,te)

balans = - monto * comision / 100
gasto =  balans
print(f"balans = {balans:2.8f}")
for t in range(ts,te):
    change_balance = 0
    for row in solo:
        if t == row[0]:
            change_balance = cfx_btc * row[2]
    balans = balans - velocidad_BTC_s + change_balance
    gasto = gasto - velocidad_BTC_s
    if change_balance != 0:
        print(f"balans = {balans:2.8f} gasto = {- gasto:2.8f} percent = {- int(100*balans/gasto)}")
        


