import json
import logging
from functools import lru_cache
from typing import Optional

from fastapi import Depends

from search_api.app.db.elastic import get_elastic
from search_api.app.db.redis import get_redis
from search_api.app.models.person_model import Person
from search_api.app.services.abstract_storage import AsyncCacheStorage, AsyncStorage
from search_api.app.services.base_service import BaseService

LOGGER = logging.getLogger(__name__)


class PersonService(BaseService):

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        return await self.id_logic(person_id, Person, 'person')

    async def get_all_persons(self, limit: int, role: Optional[str] = None, sort_name: Optional[str] = None,
                              sort_role: Optional[str] = None):
        persons_id = f"persons_id_{role}&{sort_name}&{sort_role}&{limit}"
        return await self.get_all_logic(persons_id, Person, limit, role=role, sort_name=sort_name, sort_role=sort_role)


@lru_cache
def get_person_service(cache: AsyncCacheStorage = Depends(get_redis),
                       storage: AsyncStorage = Depends(get_elastic)) -> PersonService:
    return PersonService(cache, storage)
