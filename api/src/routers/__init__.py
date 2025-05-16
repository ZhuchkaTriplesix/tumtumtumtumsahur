from dataclasses import dataclass

from src.routers.mongo.router import router as mongo_router


@dataclass(frozen=True)
class Router:
    routers = [
        (mongo_router, "/api/mongo", ["mongo"]),
    ]
