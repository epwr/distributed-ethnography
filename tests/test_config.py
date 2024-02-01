import pytest
import os


from app.config import settings, AppSettings



def test_config_exports_a_settings_var_with_appropriate_structure():

    assert isinstance(settings.host, str)
    assert settings.host == os.environ.get('HOST')
    
    assert isinstance(settings.port, int)
    assert settings.port == int(os.environ.get('PORT'))


def test_settings_will_not_be_created_if_env_vars_are_not_set():

    stored_host_value = os.environ.get('HOST')
    del os.environ['HOST']

    with pytest.raises(KeyError):
        AppSettings()

    os.environ['HOST'] = stored_host_value

def test_settings_will_not_be_created_if_env_vars_can_not_be_parsed_to_appropriate_types():

    stored_port_value = os.environ.get('PORT')
    os.environ['PORT'] = 'dd3k'
    
    with pytest.raises(ValueError):
        AppSettings()

    os.environ['PORT'] = stored_port_value
