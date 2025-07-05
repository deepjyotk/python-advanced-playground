# settings.py
from uuid import uuid4
from typing import Optional
from pydantic import AnyUrl, SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 1️⃣ Required
    database_url: AnyUrl = Field(..., alias="DB_URL")

    # 2️⃣ Optional with string default
    redis_url: str = Field("redis://localhost:6379/0", alias="REDIS_URL")

    # 3️⃣ Required secret (no default ⇢ error if missing)
    jwt_secret: SecretStr = Field(..., alias="JWT_SECRET")

    # 4️⃣ Optional nullable
    sentry_dsn: Optional[AnyUrl] = Field(None, alias="SENTRY_DSN")

    # 5️⃣ Optional with computed default
    run_id: str = Field(default_factory=lambda: uuid4().hex)

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        populate_by_name=True,   # allows env var *or* field name at runtime
    )
