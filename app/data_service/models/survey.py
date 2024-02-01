from pydantic import BaseModel
from uuid import UUID


class Survey(BaseModel):
    uid: UUID
    name: str
    is_open: bool
