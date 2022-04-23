import json
from functools import lru_cache
from typing import Optional

from fastapi import Depends

from search_api.app.db.elastic import get_elastic
from search_api.app.db.redis import get_redis
from search_api.app.models.genre_model import Genre
from search_api.app.services.abstract_storage import AsyncCacheStorage, AsyncStorage
from search_api.app.services.base_service import BaseService


class GenreService(BaseService):

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        return await self.id_logic(genre_id, Genre, 'genre')

    async def get_all_genres(self, limit: int, sort_name: Optional[str] = None):
        genres_id = f"genres_id_{sort_name}&{limit}"
        return await self.get_all_logic(genres_id, Genre, limit, sort_name=sort_name)


@lru_cache
def get_genre_service(cache: AsyncCacheStorage = Depends(get_redis),
                      storage: AsyncStorage = Depends(get_elastic)) -> GenreService:
    return GenreService(cache, storage)
