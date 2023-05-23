from uvicorn import run
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.config as config
from app.routes import HeadRouter
from app.db.redis_helper import ClientCache

app = FastAPI(
    title='Recipe book',
    description='API for Recipe book application.',
    version=config.VERSION_APP,
    contact={
        "name": "Sergey Makshakov",
        "email": "sejey44@gmail.com"
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,)

app.include_router(HeadRouter().router)


@app.on_event('startup')
async def startup_event():
    """ API start """
    app.include_router(HeadRouter().router)
    app.state.cache = ClientCache(config.REDIS_PARAMS)         # Add client redis for cache
    app.state.config = config


@app.on_event('shutdown')
async def shutdown_event():
    """  API stop """
    await app.state.cache.close_client()                      # Close client redis


if __name__ == "__main__":
    run(
        'app.main:app',
        host='127.0.0.1',
        port=int(config.PORT),
        reload=True
    )
