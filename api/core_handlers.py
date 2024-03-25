from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from api.actions.core import _get_series_by_id, _get_film_by_id, _get_all_films, _get_all_series
from api.models import ShowFilmSchema, ShowSeriesSchema
from db.session import connect_db

core_router = APIRouter()


@core_router.get('/films', response_model=ShowFilmSchema)
async def get_film_by_id(film_id: int, db: AsyncSession = Depends(connect_db)):
    film = await _get_film_by_id(film_id, db)
    if film is None:
        raise HTTPException(status_code=404, detail=f"Film with id={film_id} not found")
    return film


@core_router.get('/series', response_model=ShowSeriesSchema)
async def get_series_by_id(series_id: int, db: AsyncSession = Depends(connect_db)):
    series = await _get_series_by_id(series_id, db)
    if series is None:
        raise HTTPException(status_code=404, detail=f"Film with id={series_id} not found")
    return series


@core_router.get('/all_films')
async def get_films(db: AsyncSession = Depends(connect_db)):
    films = await _get_all_films(db)
    if films is None:
        raise HTTPException(status_code=404, detail=f"There is no films yet.")
    return films


@core_router.get('/all_series')
async def get_series(db: AsyncSession = Depends(connect_db)):
    series = await _get_all_series(db)
    if series is None:
        raise HTTPException(status_code=404, detail=f"There is no series yet.")
    return series