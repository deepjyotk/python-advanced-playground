from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text
import redis.asyncio as aioredis
from containers import Container

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"} 


@router.get("/sample")
@inject
async def sample(
    db: AsyncEngine = Depends(Provide[Container.db_engine]),
    redis: aioredis.Redis = Depends(Provide[Container.redis]),
):
    # 1. Use Redis to increment a counter
    count = await redis.incr("sample_counter")

    # 2. Run a simple SELECT 1 query against the DB
    async with db.connect() as conn: 
        result = await conn.execute(text("SELECT 1"))
        db_value = result.scalar()

    return {
        "status": "ok",
        "redis_count": count,
        "db_value": db_value,
    }