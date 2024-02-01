import os


class BaseSettings():

    def __init__(self):

        for key, value_type in self.__annotations__.items():

            env_value = os.environ[key.upper()]

            print(f"{key = }, {env_value = }")
            settings_value = value_type(env_value)
            self.__setattr__(key, settings_value)



class AppSettings(BaseSettings):
    test_value: int

settings = AppSettings()
