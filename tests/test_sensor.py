import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import sys
import os

# Ensure the root directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module to ensure it's loaded before we patch
import components.midea_dehum.sensor

@pytest.fixture
def mock_cg():
    with patch("components.midea_dehum.sensor.cg") as mock:
        mock_parent = MagicMock()
        mock.get_variable = AsyncMock(return_value=mock_parent)
        yield mock

@pytest.fixture
def mock_sensor():
    with patch("components.midea_dehum.sensor.sensor") as mock:
        mock_sens = MagicMock()
        mock.new_sensor = AsyncMock(return_value=mock_sens)
        yield mock

@pytest.mark.asyncio
async def test_to_code_empty_config(mock_cg, mock_sensor):
    from components.midea_dehum.sensor import to_code, CONF_MIDEA_DEHUM_ID

    config = {
        CONF_MIDEA_DEHUM_ID: "my_dehum"
    }

    await to_code(config)

    mock_cg.get_variable.assert_awaited_once_with("my_dehum")
    mock_cg.add_define.assert_not_called()
    mock_cg.add.assert_not_called()

@pytest.mark.asyncio
async def test_to_code_all_sensors(mock_cg, mock_sensor):
    from components.midea_dehum.sensor import (
        to_code,
        CONF_MIDEA_DEHUM_ID,
        CONF_ERROR,
        CONF_TANK_LEVEL,
        CONF_PM25,
        CONF_CURRENT_HUMIDITY,
        CONF_CURRENT_TEMPERATURE
    )

    config = {
        CONF_MIDEA_DEHUM_ID: "my_dehum",
        CONF_ERROR: "error_config",
        CONF_TANK_LEVEL: "tank_config",
        CONF_PM25: "pm25_config",
        CONF_CURRENT_HUMIDITY: "humidity_config",
        CONF_CURRENT_TEMPERATURE: "temp_config"
    }

    await to_code(config)

    mock_cg.get_variable.assert_awaited_once_with("my_dehum")
    parent = mock_cg.get_variable.return_value

    assert mock_sensor.new_sensor.await_count == 5
    mock_sensor.new_sensor.assert_any_await("error_config")
    mock_sensor.new_sensor.assert_any_await("tank_config")
    mock_sensor.new_sensor.assert_any_await("pm25_config")
    mock_sensor.new_sensor.assert_any_await("humidity_config")
    mock_sensor.new_sensor.assert_any_await("temp_config")

    mock_cg.add_define.assert_any_call("USE_MIDEA_DEHUM_ERROR")
    mock_cg.add_define.assert_any_call("USE_MIDEA_DEHUM_TANK_LEVEL")
    mock_cg.add_define.assert_any_call("USE_MIDEA_DEHUM_PM25")
    mock_cg.add_define.assert_any_call("USE_MIDEA_DEHUM_CURRENT_HUMIDITY")
    mock_cg.add_define.assert_any_call("USE_MIDEA_DEHUM_CURRENT_TEMPERATURE")

    sens_mock = mock_sensor.new_sensor.return_value
    assert mock_cg.add.call_count == 5
    mock_cg.add.assert_any_call(parent.set_error_sensor(sens_mock))
    mock_cg.add.assert_any_call(parent.set_tank_level_sensor(sens_mock))
    mock_cg.add.assert_any_call(parent.set_pm25_sensor(sens_mock))
    mock_cg.add.assert_any_call(parent.set_current_humidity_sensor(sens_mock))
    mock_cg.add.assert_any_call(parent.set_current_temperature_sensor(sens_mock))

@pytest.mark.asyncio
async def test_to_code_partial_config(mock_cg, mock_sensor):
    from components.midea_dehum.sensor import (
        to_code,
        CONF_MIDEA_DEHUM_ID,
        CONF_ERROR,
        CONF_TANK_LEVEL
    )

    config = {
        CONF_MIDEA_DEHUM_ID: "my_dehum",
        CONF_ERROR: "error_config",
        CONF_TANK_LEVEL: "tank_config",
    }

    await to_code(config)

    parent = mock_cg.get_variable.return_value

    assert mock_sensor.new_sensor.await_count == 2

    mock_cg.add_define.assert_any_call("USE_MIDEA_DEHUM_ERROR")
    mock_cg.add_define.assert_any_call("USE_MIDEA_DEHUM_TANK_LEVEL")
    assert mock_cg.add_define.call_count == 2

    sens_mock = mock_sensor.new_sensor.return_value
    assert mock_cg.add.call_count == 2
    mock_cg.add.assert_any_call(parent.set_error_sensor(sens_mock))
    mock_cg.add.assert_any_call(parent.set_tank_level_sensor(sens_mock))
