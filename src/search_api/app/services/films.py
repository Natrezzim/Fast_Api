import json
import logging
from functools import lru_cache
from typing import Optional

from fastapi import Depends

from search_api.app.db.elastic import get_elastic
from search_api.app.db.redis import get_redis
from search_api.app.models.film_model import Film
from search_api.app.services.abstract_storage import AsyncCacheStorage, AsyncStorage
from search_api.app.services.base_service import BaseService

LOGGER = logging.getLogger(__name__)


class FilmService(BaseService):

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        return await self.id_logic(film_id, Film, 'movies')

    async def get_all_films(self, limit: int, genre: Optional[str] = None, actor: Optional[str] = None,
                            sort: Optional[str] = None):
        films_id = f"films_id_{genre}&{actor}&{sort}&{limit}"
        return await self.get_all_logic(films_id, Film, limit, genre, actor, sort)


@lru_cache
def get_film_service(cache: AsyncCacheStorage = Depends(get_redis),
                     storage: AsyncStorage = Depends(get_elastic)) -> FilmService:
    return FilmService(cache, storage)
