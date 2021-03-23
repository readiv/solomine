import datetime

def int2time(time:int):
    time_since = datetime.datetime(1970, 1, 1, 1) + datetime.timedelta(seconds=time)
    return time_since

def time2int(time: datetime):
    return int((time - datetime.datetime(1970, 1, 1, 1)).total_seconds())

def time2float(time: datetime):
    return float((time - datetime.datetime(1970, 1, 1, 1)).total_seconds())

def reward2float(reward:str):
    while len(reward)<19:
        reward = "0" + reward
    reward = reward[:1] + "." + reward[1:9]
    return float(reward)
