from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.exc.declarative import declarative_base

from config import DATABASE_URL

Base = declarative_base()


def connect_db():
    engine = create_engine(DATABASE_URL, connect_args={})
    session = Session(bind=engine.connect())
    return session


class User:
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    nickname = Column(String)
    created_at = Column(String, default=datetime.utcnow())


class Film(Base):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    title = Column(String)
    description = Column(String)
    created_at = Column(String, default=datetime.utcnow())


class AuthToken(Base):
    __tablename__ = 'auth.token'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    token = Column(String)
    created_at = Column(String, default=datetime.utcnow())
