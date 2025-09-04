from fastapi import Body
from pydantic import BaseModel
from typing import Optional, Dict


class SingleContainer(BaseModel):
    short_id: str
    state: str
    image: str


class ContainerResponse(BaseModel):
    containers: Dict[str, SingleContainer] | None = None
    error: Optional[str] = None

class ContainerPayload(BaseModel):
    type: str
    ts: str
    data: ContainerResponse