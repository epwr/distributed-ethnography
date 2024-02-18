from uuid import UUID, uuid4
from pydantic import Field


from .base_data_model import BaseDataModel


class Survey(BaseDataModel):
    uid: UUID = Field(default_factory=uuid4)
    name: str
    is_open: bool
