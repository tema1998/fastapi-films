from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow())


class AuthToken(Base):
    __tablename__ = 'auth_token'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String)
    created_at = Column(String, default=datetime.utcnow())


film_actor = Table(
    'film_actor',
    Base.metadata,
    Column('film_id', Integer, ForeignKey('films.id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
)

series_actor = Table(
    'series_actor',
    Base.metadata,
    Column('series_id', Integer, ForeignKey('series.id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
)

film_director = Table(
    'film_director',
    Base.metadata,
    Column('film_id', Integer, ForeignKey('films.id')),
    Column('director_id', Integer, ForeignKey('directors.id'))
)

series_director = Table(
    'series_director',
    Base.metadata,
    Column('series_id', Integer, ForeignKey('series.id')),
    Column('director_id', Integer, ForeignKey('directors.id'))
)


class Film(Base):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    image = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    censor_age = Column(String)
    actors = relationship('Actor', secondary=film_actor, backref='films_of_actor')
    directors = relationship('Director', secondary=film_director, backref='films_of_director')
    genres = Column(Integer, ForeignKey('genres.id'))
    link = Column(String)


class Series(Base):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    image = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    censor_age = Column(String)
    actors = relationship('Actor', secondary=series_actor, backref='series_of_actor')
    directors = relationship('Director', secondary=series_director, backref='series_of_director')
    genres = Column(Integer, ForeignKey('genres.id'))
    link = Column(String)


class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    starred_in_films = relationship('Film', secondary=film_actor, backref='film_actors')
    starred_in_series = relationship('Series', secondary=series_actor, backref='series_actors')


class Director(Base):
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    made_films = relationship('Film', secondary=film_director, backref='film_directors')
    made_series = relationship('Series', secondary=series_director, backref='series_directors')


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
