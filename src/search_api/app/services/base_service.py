import json
from typing import Optional

from search_api.app.models.film_model import Film
from search_api.app.models.genre_model import Genre
from search_api.app.models.person_model import Person
from search_api.app.services.cache import CacheService
from search_api.app.services.elastic import ElasticService


class BaseService(CacheService, ElasticService):

    async def id_logic(self, search_id: str, model: [Film, Genre, Person], index: str) -> Optional:
        data = await self._film_from_cache(search_id, model)
        if not data:
            data = await self._get_one_from_elastic(search_id, model, index)
            if not data:
                return None
            await self._put_to_cache(key=search_id, value=data.json())
        return data

    async def get_all_logic(self, search_id, model: [Film, Genre, Person], limit: int, genre: Optional[str] = None,
                            actor: Optional[str] = None,
                            sort: Optional[str] = None, sort_name: Optional[str] = None, role: Optional[str] = None,
                            sort_role: Optional[str] = None):
        data = await self._get_all_from_cache(search_id, model)
        if not data:
            if model == Film:
                data = await self._get_all_film_from_elastic(limit=limit, genre=genre, actor=actor, sort=sort)
            if model == Genre:
                data = await self._get_all_genre_from_elastic(limit=limit, sort_name=sort_name)
            if model == Person:
                data = await self._get_all_person_from_elastic(limit=limit, role=role, sort_name=sort_name,
                                                               sort_role=sort_role)
            if not data:
                return None
            await self._put_to_cache(key=search_id, value=json.dumps({"items": [i.json() for i in data]}))
        return data
