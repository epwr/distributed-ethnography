from pydantic import BaseModel


class BaseDataModel(BaseModel):
    """ """

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return all(
            self.__getattribute__(field) == other.__getattribute__(field)
            for field in self.__annotations__.keys()
        )
