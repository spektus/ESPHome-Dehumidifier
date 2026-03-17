import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from components.midea_dehum.text_sensor import to_code, CONF_CAPABILITIES, CONF_MIDEA_DEHUM_ID
from esphome.const import CONF_ID

@pytest.mark.asyncio
async def test_to_code_with_capabilities():
    # Setup mocks
    mock_cg = MagicMock()
    mock_cg.get_variable = AsyncMock()
    mock_parent = MagicMock()
    mock_cg.get_variable.return_value = mock_parent

    mock_sens = MagicMock()
    mock_cg.new_Pvariable.return_value = mock_sens

    mock_text_sensor = MagicMock()
    mock_text_sensor.register_text_sensor = AsyncMock()

    config = {
        CONF_MIDEA_DEHUM_ID: "my_dehum_id",
        CONF_CAPABILITIES: {
            CONF_ID: "my_cap_id"
        }
    }

    with patch('components.midea_dehum.text_sensor.cg', mock_cg), \
         patch('components.midea_dehum.text_sensor.text_sensor', mock_text_sensor):

        await to_code(config)

        # Verify
        mock_cg.get_variable.assert_called_once_with("my_dehum_id")
        mock_cg.add_define.assert_called_with("USE_MIDEA_DEHUM_CAPABILITIES")
        mock_cg.new_Pvariable.assert_called_once_with("my_cap_id")
        mock_text_sensor.register_text_sensor.assert_called_once_with(mock_sens, config[CONF_CAPABILITIES])

        # Check add calls
        assert mock_cg.add.call_count == 2
        mock_sens.set_parent.assert_called_once_with(mock_parent)
        mock_parent.set_capabilities_text_sensor.assert_called_once_with(mock_sens)

@pytest.mark.asyncio
async def test_to_code_without_capabilities():
    # Setup mocks
    mock_cg = MagicMock()
    mock_cg.get_variable = AsyncMock()
    mock_parent = MagicMock()
    mock_cg.get_variable.return_value = mock_parent

    config = {
        CONF_MIDEA_DEHUM_ID: "my_dehum_id"
    }

    with patch('components.midea_dehum.text_sensor.cg', mock_cg):
        await to_code(config)

        # Verify
        mock_cg.get_variable.assert_called_once_with("my_dehum_id")
        # add_define shouldn't be called for USE_MIDEA_DEHUM_CAPABILITIES
        mock_cg.add_define.assert_not_called()
        mock_cg.new_Pvariable.assert_not_called()
        mock_cg.add.assert_not_called()
