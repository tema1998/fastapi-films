from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from api.actions.core import _get_movie_by_id, _get_movies_by_category, _get_movies_by_genre, _get_movies_by_actor
from api.models import ShowMovieSchema, ShowMovieShort
from db.session import connect_db

core_router = APIRouter()


@core_router.get('/movie', response_model=ShowMovieSchema)
async def get_movie_by_id(movie_id: int, db: AsyncSession = Depends(connect_db)):
    film = await _get_movie_by_id(movie_id, db)
    if film is None:
        raise HTTPException(status_code=404, detail=f"Movie with id={movie_id} not found")
    return film


@core_router.get('/')
async def get_movies_by_category(category: str, db: AsyncSession = Depends(connect_db)):
    films = await _get_movies_by_category(category, db)
    if len(films) == 0:
        raise HTTPException(status_code=404, detail=f"There is no movies in category <{category}> or category doesn't "
                                                    f"exist.")
    return films


@core_router.get('/genre')
async def get_movies_by_genre(genre: str, db: AsyncSession = Depends(connect_db)):
    movies = await _get_movies_by_genre(genre, db)
    if len(movies) == 0:
        raise HTTPException(status_code=404, detail=f"There is no movies by <{genre}> genre.")
    return movies


@core_router.get('/actor')
async def get_movies_by_actor(actor_id: int, db: AsyncSession = Depends(connect_db)):
    movies = await _get_movies_by_actor(actor_id, db)
    if len(movies) == 0:
        raise HTTPException(status_code=404, detail=f"There is no movies with this actor.")
    return movies