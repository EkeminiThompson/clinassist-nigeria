from slowapi import Limiter
from slowapi.util import get_remote_address
from backend.app.core.config import settings
# Memory storage is for local development only. Production config enforces Redis.
limiter=Limiter(key_func=get_remote_address,storage_uri=settings.rate_limit_storage_uri,default_limits=[])
