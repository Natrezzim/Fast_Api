import asyncio
import logging
import aioredis
import backoff

from tests.functional.settings import REDIS_HOST, REDIS_PORT

logging.getLogger('backoff').addHandler(logging.StreamHandler())

red = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}', encoding="utf-8", decode_responses=True)


@backoff.on_exception(wait_gen=backoff.expo, exception=aioredis.exceptions.ConnectionError)
async def redis():
    await red.ping()
    await red.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(redis())
    loop.close()

