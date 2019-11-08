from traffic.logger import Logger
from traffic.configurator import Configurator

import asyncio
import asyncpg

class AbstractDBControl:
    def __init__(self):
        self._logger = Logger('DBControl')


class PgDatabase(AbstractDBControl):

    def __init__(self, **kwargs):
        super().__init__()

        try:
            loop = asyncio.get_event_loop()
            self.pool = loop.run_until_complete(asyncpg.create_pool(**kwargs))
        except Exception as e:
            self._logger.error(f'Failed to create connection-pool to database: {e}', e)


    async def push_stream(self, stream='debug'):
        try:
            async with self.pool.acquire() as conn:
            
                self._logger.debug('Connection to db is established')
                
                stmt = await conn.prepare('''SELECT 2 ^ $1''')
                res = await stmt.fetchval(20)
                
                self._logger.debug(f'Result of "SELECT 2 ^ 20": {res}')

        except Exception as e:
                self._logger.error(f'Got an exception while pushing stream into database: {e}', e)
