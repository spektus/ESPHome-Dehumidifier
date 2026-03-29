import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from components.midea_dehum.number import to_code, CONF_TIMER, CONF_HUMIDITY_SETPOINT
from components.midea_dehum import CONF_MIDEA_DEHUM_ID

@pytest.mark.asyncio
async def test_to_code_timer_limits():
    """Test that configuring the timer number generates the correct code with proper limits."""
    config = {
        CONF_MIDEA_DEHUM_ID: "my_dehum_id",
        CONF_TIMER: {"id": "my_timer_id"}
    }

    mock_parent = MagicMock()

    with patch("components.midea_dehum.number.cg.get_variable", new_callable=AsyncMock) as mock_get_variable, \
         patch("components.midea_dehum.number.cg.add_define") as mock_add_define, \
         patch("components.midea_dehum.number.number.new_number", new_callable=AsyncMock) as mock_new_number, \
         patch("components.midea_dehum.number.cg.add") as mock_add:

        mock_get_variable.return_value = mock_parent
        mock_new_number.return_value = "mock_number_obj"

        await to_code(config)

        mock_get_variable.assert_awaited_once_with("my_dehum_id")
        mock_add_define.assert_any_call("USE_MIDEA_DEHUM_TIMER")

        # Verify the timer limits match the configuration (min: 0, max: 24.0, step: 0.5)
        mock_new_number.assert_awaited_once_with(
            config[CONF_TIMER],
            min_value=0,
            max_value=24.0,
            step=0.5,
        )

        mock_parent.set_timer_number.assert_called_once_with("mock_number_obj")
        mock_add.assert_any_call(mock_parent.set_timer_number.return_value)

@pytest.mark.asyncio
async def test_to_code_humidity_setpoint_limits():
    """Test that configuring the humidity setpoint number generates the correct code with proper limits."""
    config = {
        CONF_MIDEA_DEHUM_ID: "my_dehum_id",
        CONF_HUMIDITY_SETPOINT: {"id": "my_humidity_id"}
    }

    mock_parent = MagicMock()

    with patch("components.midea_dehum.number.cg.get_variable", new_callable=AsyncMock) as mock_get_variable, \
         patch("components.midea_dehum.number.cg.add_define") as mock_add_define, \
         patch("components.midea_dehum.number.number.new_number", new_callable=AsyncMock) as mock_new_number, \
         patch("components.midea_dehum.number.cg.add") as mock_add:

        mock_get_variable.return_value = mock_parent
        mock_new_number.return_value = "mock_number_obj"

        await to_code(config)

        mock_get_variable.assert_awaited_once_with("my_dehum_id")
        mock_add_define.assert_any_call("USE_MIDEA_DEHUM_HUMIDITY_SETPOINT")

        # Verify the humidity setpoint limits match the configuration (min: 35, max: 85, step: 5)
        mock_new_number.assert_awaited_once_with(
            config[CONF_HUMIDITY_SETPOINT],
            min_value=35,
            max_value=85,
            step=5,
        )

        mock_parent.set_humidity_setpoint_number.assert_called_once_with("mock_number_obj")
        mock_add.assert_any_call(mock_parent.set_humidity_setpoint_number.return_value)
