from dependency_injector import containers, providers
from settings import Settings
from sqlalchemy.ext.asyncio import create_async_engine
import redis.asyncio as aioredis

"""
- we create async db engine. (no sockets yet, this defines the pool size)
- now for each request, we create a new session using factory.
(NOTE: we will avoid using singleton session, because of following reason:

| Time | User A (browser tab 1)                                                 | User B (tab 2)                                                         | User C (tab 3)     | What the singleton session is doing                                                                                                                                                        |
| ---- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| T0   | —                                                                      | —                                                                      | —                  | `session` is idle.                                                                                                                                                                         |
| T1   | `SELECT * FROM seats WHERE id=42` <br>→ returns **available**          | —                                                                      | —                  | Seat row 42 is now in the session’s identity-map: `status="available"`.                                                                                                                    |
| T2   | —                                                                      | `SELECT * FROM seats WHERE id=42`                                      | —                  | **Hits cache**, *still sees* `status="available"` – never queries DB because the row is already in the identity-map.                                                                       |
| T3   | —                                                                      | —                                                                      | `SELECT … seat 42` | Same story → “available”.                                                                                                                                                                  |
| T4   | `UPDATE seat 42 SET status='booked', user_id=A` <br>`session.commit()` | —                                                                      | —                  | Flush writes change **and commits the transaction for *all three* users!** Session is now clean. DB row is booked.                                                                         |
| T5   | —                                                                      | `UPDATE seat 42 SET status='booked', user_id=B` <br>`session.commit()` | —                  | Fails with **`IntegrityError` / deadlock** or silently overwrites User A, depending on constraints + isolation level. Session enters “rollback-only” state.                                |
| T6   | —                                                                      | —                                                                      | Any DB call        | Raises `PendingRollbackError` because the shared session is now poisoned. Every request after this point returns 500 until the process restarts or you manually call `session.rollback()`. |

Though DB is thread safe, but sharing the same session across threads will lead to cascading errors.

What went wrong
1. Identity-map caching – After User A’s first query, seat 42 stayed in memory as “available”. Users B and C never re-checked the database.

2. Single transaction scope – commit() committed everyone’s unflushed work, not just the caller’s.

3. Error isolation – When User B’s commit failed, the session locked into “failed” state, cascading errors to all subsequent requests.

"""
class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["routes"])

    # Settings provider (loads env only once, when first used)
    _settings = providers.Singleton(Settings)

    config = providers.Configuration()
    config.from_pydantic((_settings()))

    db_engine = providers.Resource(
        lambda url, echo: create_async_engine(str(url), echo=echo),
        url=config.database_url,
        echo=False,
    )

    redis = providers.Resource(
        aioredis.from_url,
        url=config.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )