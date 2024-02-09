import pytest
import os


from app.config import settings, AppSettings


@pytest.mark.parametrize(
    "key, value_type",
    [[key, value_type] for key, value_type in AppSettings.__annotations__.items()],
)
def test_config_exports_a_settings_var_with_appropriate_structure(key, value_type):
    assert isinstance(settings.__getattribute__(key), value_type)
    assert settings.__getattribute__(key) == value_type(os.environ[key.upper()])


def test_settings_will_not_be_created_if_env_vars_are_not_set():
    str_env_var = "SQLITE_FILE"

    stored_value = os.environ.get(str_env_var)
    del os.environ[str_env_var]

    with pytest.raises(KeyError):
        AppSettings()

    os.environ[str_env_var] = stored_value


@pytest.mark.skip("Do not currently have a non-string value in AppSettings")
def test_settings_will_raise_error_if_env_vars_cannot_be_type_cast():
    int_env_var = ""

    stored_port_value = os.environ.get(int_env_var)
    os.environ[int_env_var] = "dd3k"

    with pytest.raises(ValueError):
        AppSettings()

    os.environ[int_env_var] = stored_port_value
