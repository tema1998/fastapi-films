from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from api.models import ShowFilmSchema, ShowSeriesSchema
from db.dals import FilmDAL, SeriesDAL


async def _get_film_by_id(film_id, session):
    async with session.begin():
        film_dal = FilmDAL(session)
        film = await film_dal.get_film_by_id(
            film_id=film_id
        )
        if film is not None:
            return ShowFilmSchema(
                id=film.id,
                title=film.title,
                description=film.description,
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
            return ShowSeriesSchema(
                id=series.id,
                title=series.title,
                description=series.description,
                created_at=series.created_at,
                censor_age=series.censor_age,
                actors=jsonable_encoder(series.actors),
                directors=jsonable_encoder(series.directors),
                genres=series.genres,
                link=series.link
            )
