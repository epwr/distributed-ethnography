from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Survey(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    name: str
    is_open: bool
