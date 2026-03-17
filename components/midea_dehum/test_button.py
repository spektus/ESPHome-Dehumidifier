import sys
import unittest.mock
import pytest

# A unified mock mechanism.
# Since esphome is normally not available, we mock it out globally BEFORE importing components.
mock_cg = unittest.mock.MagicMock()
mock_cg.get_variable = unittest.mock.AsyncMock()
mock_cg.Component = unittest.mock.MagicMock()

mock_cv = unittest.mock.MagicMock()

mock_button = unittest.mock.MagicMock()
mock_button.Button = unittest.mock.MagicMock()
mock_button.new_button = unittest.mock.AsyncMock()

mock_uart = unittest.mock.MagicMock()
mock_const = unittest.mock.MagicMock()
mock_const.ENTITY_CATEGORY_CONFIG = "config"

sys.modules['esphome'] = unittest.mock.MagicMock()
sys.modules['esphome.codegen'] = mock_cg
sys.modules['esphome.config_validation'] = mock_cv
sys.modules['esphome.components'] = unittest.mock.MagicMock()
sys.modules['esphome.components.button'] = mock_button
sys.modules['esphome.components.uart'] = mock_uart
sys.modules['esphome.const'] = mock_const

# Now it is safe to import button
from components.midea_dehum import button

@pytest.fixture(autouse=True)
def reset_mocks():
    mock_cg.reset_mock()
    mock_button.reset_mock()

    # In esphome.codegen, get_variable is an async function returning a variable
    # We must mock it specifically in the button module
    button.cg.get_variable = unittest.mock.AsyncMock()
    # In esphome.components.button, new_button is an async function returning a button
    # We must mock it specifically in the button module
    button.button.new_button = unittest.mock.AsyncMock()
    # Mock button.cg.add_define and add to track calls
    button.cg.add_define = unittest.mock.MagicMock()
    button.cg.add = unittest.mock.MagicMock()

@pytest.mark.asyncio
async def test_to_code_no_filter_cleaned():
    config = {
        button.CONF_MIDEA_DEHUM_ID: 'my_dehum'
    }
    parent_mock = unittest.mock.MagicMock()
    button.cg.get_variable.return_value = parent_mock

    await button.to_code(config)

    button.cg.get_variable.assert_called_once_with('my_dehum')

    # Check that new_button was not called
    button.button.new_button.assert_not_called()
    # Check that add_define was not called with USE_MIDEA_DEHUM_FILTER_BUTTON
    calls = button.cg.add_define.call_args_list
    for call in calls:
        assert call[0][0] != "USE_MIDEA_DEHUM_FILTER_BUTTON"

@pytest.mark.asyncio
async def test_to_code_with_filter_cleaned():
    config = {
        button.CONF_MIDEA_DEHUM_ID: 'my_dehum',
        button.CONF_FILTER_CLEANED: 'my_button_config'
    }
    parent_mock = unittest.mock.MagicMock()
    button.cg.get_variable.return_value = parent_mock

    btn_mock = unittest.mock.MagicMock()
    button.button.new_button.return_value = btn_mock

    await button.to_code(config)

    button.cg.get_variable.assert_called_once_with('my_dehum')
    button.cg.add_define.assert_any_call("USE_MIDEA_DEHUM_FILTER_BUTTON")
    button.button.new_button.assert_called_once_with('my_button_config')

    parent_mock.set_filter_cleaned_button.assert_called_once_with(btn_mock)
    button.cg.add.assert_called_once_with(parent_mock.set_filter_cleaned_button.return_value)
