from abc import ABC
from dataclasses import asdict, dataclass
import os


class CfgBase(ABC):
    dict: callable = asdict


@dataclass
class UvicornCfg(CfgBase):
    host: str = os.getenv("UVICORN_HOST")
    port: int = os.getenv("UVICORN_PORT")


uvicorn = UvicornCfg()
