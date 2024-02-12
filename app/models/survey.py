from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Survey(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    name: str
    is_open: bool

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Survey):
            return NotImplemented
        return all(
            (
                self.uid == other.uid,
                self.name == other.name,
                self.is_open == other.is_open,
            )
        )
