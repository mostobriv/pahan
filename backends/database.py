from backends.logger import Logger

import asyncio
import asyncpg

class AbstractDBControl:
    def __init__(self):
        self._logger = Logger('DBControl')

    async def push_stream(self, stream):
        raise NotImplementedError()


class PgDatabase(AbstractDBControl):

    def __init__(self, settings: dict):
        super().__init__()

        try:
            loop = asyncio.get_event_loop()
            self.pool = loop.run_until_complete(asyncpg.create_pool(**settings))
            loop.run_until_complete(self._create_tables())
        except Exception as e:
            self._logger.error(f'Failed to create connection-pool to database: {e}', e)


    async def _create_tables(self):
        q = '''CREATE TABLE IF NOT EXISTS streams (
                    id      SERIAL PRIMARY KEY,
                    data    JSON NOT NULL,
                    port    INTEGER NOT NULL
                )
        '''
        try:
            async with self.pool.acquire() as conn:
                self._logger.debug('Creating tables')
                
                _ = await conn.execute(q)

        except Exception as e:
                self._logger.error(f'Got an exception while creating a tables inside database: {e}', e)


    async def push_streams(self, streams):
        async with self.pool.acquire() as conn:
            try:
                q = '''INSERT INTO streams (data, port) VALUES ($1, 1337)'''

                self._logger.debug(f'query = {q}')

                _ = await conn.executemany(q, map(lambda x: (x, ), streams))

            except Exception as e:
                    self._logger.error(f'Got an exception while pushing stream into database: {e}', e)


    async def get_stream(self, index: int):
        async with self.pool.acquire() as conn:
            try:
                q = '''SELECT (data, port) FROM STREAMS WHERE id = $1'''
                stmt = await conn.prepare(q)
                return await stmt.fetchval(index)
                
            except Exception as e:
                self._logger.error(f'Got an exception while trying to get stream from database: {e}', e)