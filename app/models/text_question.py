from uuid import UUID, uuid4
from pydantic import Field

from .base_data_model import BaseDataModel


class TextQuestion(BaseDataModel):
    uid: UUID = Field(default_factory=uuid4)
    survey_uid: UUID
    question: str
