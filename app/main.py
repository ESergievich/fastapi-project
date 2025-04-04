import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI

from core import db_helper, settings
from api import router as api_router
from rabbit import RabbitEmailProcessor


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with RabbitEmailProcessor() as rabbit_processor:
        task = asyncio.create_task(rabbit_processor.consume_message())
        yield
        await db_helper.dispose()
        task.cancel()


app = FastAPI(lifespan=lifespan)

app.include_router(router=api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
