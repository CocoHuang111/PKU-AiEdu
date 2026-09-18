"""Independent, single-concurrency archiver; terminal DB tasks are the durable queue."""
import asyncio
from sqlalchemy import text

from ..core.database import get_sync_engine
from ..core.material_storage import archive_pending_eval_materials, purge_deleted_oss_files


async def main():
    retry_after = {}
    while True:
        try:
            # Session advisory lock prevents duplicate work even if the service is scaled.
            with get_sync_engine().connect() as connection:
                locked = connection.scalar(text('SELECT pg_try_advisory_lock(734120, 1)'))
                try:
                    if locked:
                        await archive_pending_eval_materials(limit=1, retry_after=retry_after)
                        await purge_deleted_oss_files()
                finally:
                    if locked:
                        connection.execute(text('SELECT pg_advisory_unlock(734120, 1)'))
        except Exception as exc:
            print(f'[archive] queue check failed: {type(exc).__name__}; retrying', flush=True)
        await asyncio.sleep(10)


if __name__ == '__main__':
    asyncio.run(main())
