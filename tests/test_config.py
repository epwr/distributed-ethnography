import pytest
import os


from app.config import settings, AppSettings



def test_config_exports_a_settings_var_with_appropriate_structure():

    assert isinstance(settings.test_value, int)
    assert settings.test_value == 0


def test_settings_will_not_be_created_if_env_vars_are_not_set():

    stored_host_value = os.environ.get('TEST_VALUE')
    del os.environ['TEST_VALUE']

    with pytest.raises(KeyError):
        AppSettings()

    os.environ['TEST_VALUE'] = stored_host_value

def test_settings_will_not_be_created_if_env_vars_can_not_be_parsed_to_appropriate_types():

    stored_port_value = os.environ.get('TEST_VALUE')
    os.environ['TEST_VALUE'] = 'dd3k'
    
    with pytest.raises(ValueError):
        AppSettings()

    os.environ['TEST_VALUE'] = stored_port_value
