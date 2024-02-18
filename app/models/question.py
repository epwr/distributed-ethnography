from uuid import UUID, uuid4
from pydantic import Field

from .base_data_model import BaseDataModel


class Question(BaseDataModel):
    uid: UUID = Field(default_factory=uuid4)
    question: str
