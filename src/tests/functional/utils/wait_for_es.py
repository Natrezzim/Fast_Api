import asyncio
import logging
import backoff
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import ELASTIC_HOST, ELASTIC_PORT

es = AsyncElasticsearch([f'{ELASTIC_HOST}: {ELASTIC_PORT}'], verify_certs=False)

logging.getLogger('backoff').addHandler(logging.StreamHandler())


@backoff.on_exception(wait_gen=backoff.expo, exception=ConnectionError)
async def elastic():
    response = await es.ping()
    if response is False:
        raise ConnectionError
    await es.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(elastic())
    loop.stop()
    loop.close()
