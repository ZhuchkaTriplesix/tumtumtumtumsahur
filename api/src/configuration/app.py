import logging
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from faststream.kafka import KafkaBroker
from routers import Router
import os
from typing import AsyncIterator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class App:
    def __init__(self):
        self._kafka_broker: KafkaBroker | None = None
        self._mongo_client: AsyncIOMotorClient | None = None

        self._app: FastAPI = FastAPI(
            title="API",
            description="API",
            docs_url=None,
            redoc_url=None,
            openapi_url="/api/openapi.json",
            lifespan=self.lifespan
        )

        self._configure_middleware()
        self._register_routers()

    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncIterator[None]:
        self._kafka_broker = KafkaBroker(os.getenv("KAFKA_BROKERS", "localhost:9092"))
        self._mongo_client = AsyncIOMotorClient(os.getenv("MONGODB_URI", "mongodb://root:example@mongodb:27017"))

        try:
            await self._kafka_broker.start()
            logger.info("Services started")
            yield
        finally:
            await self._kafka_broker.close()
            self._mongo_client.close()
            logger.info("Services stopped")

    def _configure_middleware(self) -> None:
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "DELETE", "PATCH"],
            allow_headers=["*"]
        )

    def _register_routers(self) -> None:
        for router, prefix, tags in Router.routers:
            self._app.include_router(
                router=router,
                prefix=prefix,
                tags=tags
            )

    async def get_kafka_broker(self) -> KafkaBroker:
        if not self._kafka_broker:
            raise RuntimeError("Kafka broker not initialized")
        return self._kafka_broker

    async def get_mongo_client(self) -> AsyncIOMotorClient:
        if not self._mongo_client:
            raise RuntimeError("MongoDB client not initialized")
        return self._mongo_client

    @property
    def app(self) -> FastAPI:
        return self._app
