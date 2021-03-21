from sqlalchemy import Column, Integer, String, BigInteger, Float
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
        return f'<User {self.name} {self.email}>'

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)