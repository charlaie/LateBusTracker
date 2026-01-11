import asyncio
from app.settings import get_settings
from app.db import get_db_session

settings = get_settings()

print(settings.database_url)
print(settings.redis_url)
