import os
from pathlib import Path


class BaseSettings:
    def __init__(self) -> None:
        for key, value_type in self.__annotations__.items():
            env_value = os.environ[key.upper()]

            settings_value = value_type(env_value)
            self.__setattr__(key, settings_value)

    def __str__(self) -> str:
        string = f"{self.__class__}("

        for key in self.__annotations__.keys():
            value = self.__getattribute__(key)
            string += f"{key}: {value}, "

        return string + " )"


class AppSettings(BaseSettings):
    sqlite_file: Path


settings = AppSettings()
