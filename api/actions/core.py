from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from api.models import ShowFilmOrSeriesSchema, ShowFilmOrSeriesShort
from db.dals import FilmDAL, SeriesDAL, AllFilmsDAL, AllSeriesDAL


async def _get_film_by_id(film_id, session):
    async with session.begin():
        film_dal = FilmDAL(session)
        film = await film_dal.get_film_by_id(
            film_id=film_id
        )
        if film is not None:
            return ShowFilmOrSeriesSchema(
                id=film.id,
                title=film.title,
                description=film.description,
                image=film.image,
                created_at=film.created_at,
                censor_age=film.censor_age,
                actors=jsonable_encoder(film.actors),
                directors=jsonable_encoder(film.directors),
                genres=film.genres,
                link=film.link
            )


async def _get_series_by_id(series_id, session):
    async with session.begin():
        series_dal = SeriesDAL(session)
        series = await series_dal.get_series_by_id(
            series_id=series_id
        )
        if series is not None:
            return ShowFilmOrSeriesSchema(
                id=series.id,
                title=series.title,
                description=series.description,
                image=series.image,
                created_at=series.created_at,
                censor_age=series.censor_age,
                actors=jsonable_encoder(series.actors),
                directors=jsonable_encoder(series.directors),
                genres=series.genres,
                link=series.link
            )


async def _get_all_films(session):
    async with session.begin():
        films_dal = AllFilmsDAL(session)
        films_all = await films_dal.get_films()
        films_json = dict()

        if films_all is not None:
            for film in films_all:
                film_object = film[0]
                films_json[film_object.id] = ShowFilmOrSeriesShort(
                    id=film_object.id,
                    title=film_object.title,
                    image=film_object.image,
                    censor_age=film_object.censor_age,
                    link=film_object.link
                )
            return films_json


async def _get_all_series(session):
    async with session.begin():
        series_dal = AllSeriesDAL(session)
        series_all = await series_dal.get_series()
        series_json = dict()

        if series_all is not None:
            for series in series_all:
                series_object = series[0]
                series_json[series_object.id] = ShowFilmOrSeriesShort(
                    id=series_object.id,
                    title=series_object.title,
                    image=series_object.image,
                    censor_age=series_object.censor_age,
                    link=series_object.link
                )
            return series_json
