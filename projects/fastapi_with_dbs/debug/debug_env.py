import os
from settings import Settings

print("=== Environment Variables ===")
print(f"DB_URL: {os.getenv('DB_URL', 'NOT SET')}")
print(f"REDIS_URL: {os.getenv('REDIS_URL', 'NOT SET')}")
print(f"JWT_SECRET: {os.getenv('JWT_SECRET', 'NOT SET')}")

print("\n=== Settings Object ===")
try:
    settings = Settings()
    print(f"database_url: {settings.database_url}")
    print(f"redis_url: {settings.redis_url}")
    print(f"jwt_secret: {'SET' if settings.jwt_secret else 'NOT SET'}")
except Exception as e:
    print(f"Error loading settings: {e}") 