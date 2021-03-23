import datetime
from sqlalchemy import Column, Integer, String, BigInteger, Float, DateTime
from db import Base, engine

class herro(Base):
    __tablename__ = 'herro'
    block_hash = Column(String(70), primary_key=True)
    height = Column(Integer)
    wallet = Column(String(50), primary_key=True)
    difficulty = Column(BigInteger)
    time_found = Column(Integer)
    region = Column(String(10))
    block_reward = Column(Float)
    reward = Column(Float)
    hash_rate = Column(BigInteger)

    def __repr__(self):
        return f'<wallet {self.wallet}>'

class diff(Base):
    __tablename__ = 'diff'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    difficulty = Column(BigInteger)
    max_price = Column(Float)

    EU_005 = Column(Float)
    EU_N_005 = Column(Float)
    USA_005 = Column(Float)
    USA_E_005 = Column(Float)

    EU_010 = Column(Float)
    EU_N_010 = Column(Float)
    USA_010 = Column(Float)
    USA_E_010 = Column(Float)

    EU_050 = Column(Float)
    EU_N_050 = Column(Float)
    USA_050 = Column(Float)
    USA_E_050 = Column(Float)

    EU_100 = Column(Float)
    EU_N_100 = Column(Float)
    USA_100 = Column(Float)
    USA_E_100 = Column(Float)

    EU_p = Column(Float)
    EU_N_p = Column(Float)
    USA_p = Column(Float)
    USA_E_p = Column(Float)

    def __repr__(self):
        return f'<time {self.time}>'

#Нужна таблица
# 1. time - Время
# 1. difficulty - Текущая сложнось
# 2. max_price - Максимальная цена профитности. 
# 3. speed_XXX - Доступная скорость по каждомц рынку "EU", "USA", "EU_N", "USA_E"
# 3. fix_0_001 - Цена фиксированого ордера при мощьности 0.001,0.008,0.009,0.01,0.05,0.1,0.5,1.0 


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)