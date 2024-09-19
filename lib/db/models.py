# db/models.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date)
    amount = Column(Float)
    category = Column(String)

class Budget(Base):
    __tablename__ = 'budgets'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category = Column(String)
    limit = Column(Float)

# Database setup
db_path = os.path.join(os.path.dirname(__file__), 'finance_tracker.db')
engine = create_engine(f'sqlite:///{db_path}')
Base.metadata.create_all(engine)  # Create tables if they don't exist

Session = sessionmaker(bind=engine)  # This should be correct
