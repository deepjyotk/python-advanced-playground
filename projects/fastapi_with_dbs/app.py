# app.py
from fastapi import FastAPI
from containers import Container
from routes import router   # your API module(s)
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    container = Container()
    app.state.container = container
    container.wire(packages=["routes"])
    container.init_resources()
    yield
    container.shutdown_resources()

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    return app
