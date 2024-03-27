from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, func, Float
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


movie_actor = Table(
    'movie_actor',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
)


movie_director = Table(
    'movie_director',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('director_id', Integer, ForeignKey('directors.id'))
)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    title = Column(String)


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    category = Column(Integer, ForeignKey('categories.id'))
    title = Column(String)
    image = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    imdb_rating = Column(Float)
    censor_age = Column(String)
    actors = relationship('Actor', secondary=movie_actor, backref='movies_of_actor')
    directors = relationship('Director', secondary=movie_director, backref='movies_of_director')
    genres = Column(Integer, ForeignKey('genres.id'))
    link = Column(String)


class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    starred_in_movies = relationship('Movie', secondary=movie_actor, backref='movie_actors')


class Director(Base):
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    made_movies = relationship('Movie', secondary=movie_director, backref='movie_directors')


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
