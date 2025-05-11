from sqlalchemy import Column, String, BigInteger, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Schedule(Base):
    __tablename__ = 'schedules'
    
    schedule_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    name = Column(String(255))
    frequency = Column(String(255))
    duration = Column(String(255))
    start_time = Column(Time)
    end_time = Column(Time)
