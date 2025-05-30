import asyncio
import logging
import sys

from database.db_users import init_db
from loader import dp, bot
import handlers

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())