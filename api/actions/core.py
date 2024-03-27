from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from api.models import ShowMovieSchema, ShowMovieShort, ShowGenres
from db.dals import MoviesDAL


async def _get_movie_by_id(movie_id, session):
    async with session.begin():
        movie_dal = MoviesDAL(session)
        movie = await movie_dal.get_movie_by_id(
            movie_id=movie_id
        )
        if movie is not None:
            return ShowMovieSchema(
                id=movie.id,
                category=movie.category,
                title=movie.title,
                description=movie.description,
                image=movie.image,
                created_at=movie.created_at,
                censor_age=movie.censor_age,
                actors=jsonable_encoder(movie.actors),
                directors=jsonable_encoder(movie.directors),
                genres=movie.genres,
                link=movie.link
            )


async def _get_movies_by_category(category, session):
    async with session.begin():
        movies_dal = MoviesDAL(session)
        movies_by_category = await movies_dal.get_movies_by_category(category=category)
        movies_json = dict()

        if movies_by_category is not None:
            for movie in movies_by_category:
                movie_object = movie[0]
                movies_json[movie_object.id] = ShowMovieShort(
                    id=movie_object.id,
                    title=movie_object.title,
                    image=movie_object.image,
                    censor_age=movie_object.censor_age,
                    link=movie_object.link
                )
            return movies_json


async def _get_movies_by_genre(genre, session):
    async with session.begin():
        movies_dal = MoviesDAL(session)
        movies_all = await movies_dal.get_movies_by_genre(genre=genre)
        movies_json = dict()

        if movies_all is not None:
            for movie in movies_all:
                movie_object = movie[0]
                movies_json[movie_object.id] = ShowMovieShort(
                    id=movie_object.id,
                    title=movie_object.title,
                    image=movie_object.image,
                    censor_age=movie_object.censor_age,
                    link=movie_object.link
                )
            return movies_json


async def _get_movies_by_actor(actor_id, session):
    async with session.begin():
        movies_dal = MoviesDAL(session)
        movies_all = await movies_dal.get_movies_by_actor(actor_id=actor_id)
        movies_json = dict()

        if movies_all is not None:
            for movie in movies_all:
                movie_object = movie[0]
                movies_json[movie_object.id] = ShowMovieShort(
                    id=movie_object.id,
                    title=movie_object.title,
                    image=movie_object.image,
                    censor_age=movie_object.censor_age,
                    link=movie_object.link
                )
            return movies_json


async def _get_genres(session):
    async with session.begin():
        movies_dal = MoviesDAL(session)
        genres_all = await movies_dal.get_genres()
        genres_json = dict()

        if genres_all is not None:
            for genre in genres_all:
                genre_object = genre[0]
                genres_json[genre_object.id] = ShowGenres(
                    id=genre_object.id,
                    title=genre_object.title,
                    description=genre_object.description,
                )
            return genres_json
