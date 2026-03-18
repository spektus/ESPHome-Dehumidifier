import sys
import os
import unittest
from unittest.mock import AsyncMock, patch, MagicMock

sys.modules['esphome'] = MagicMock()
sys.modules['esphome.codegen'] = MagicMock()
sys.modules['esphome.config_validation'] = MagicMock()
sys.modules['esphome.components'] = MagicMock()
sys.modules['esphome.const'] = MagicMock()
sys.modules['esphome.const'].CONF_ID = "id"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestClimate(unittest.IsolatedAsyncioTestCase):
    @patch('components.midea_dehum.climate.cg')
    @patch('components.midea_dehum.climate.climate')
    async def test_to_code_with_swing(self, mock_climate, mock_cg):
        mock_cg.get_variable = AsyncMock(return_value="mock_parent")
        mock_climate.register_climate = AsyncMock()
        mock_cg.add_define = MagicMock()

        from components.midea_dehum.climate import to_code, CONF_MIDEA_DEHUM_ID, CONF_SWING

        config = {
            CONF_MIDEA_DEHUM_ID: "mock_id",
            CONF_SWING: True
        }

        await to_code(config)

        mock_cg.get_variable.assert_called_once_with("mock_id")
        mock_climate.register_climate.assert_called_once_with("mock_parent", config)
        mock_cg.add_define.assert_called_once_with("USE_MIDEA_DEHUM_SWING")

    @patch('components.midea_dehum.climate.cg')
    @patch('components.midea_dehum.climate.climate')
    async def test_to_code_no_swing(self, mock_climate, mock_cg):
        mock_cg.get_variable = AsyncMock(return_value="mock_parent")
        mock_climate.register_climate = AsyncMock()
        mock_cg.add_define = MagicMock()

        from components.midea_dehum.climate import to_code, CONF_MIDEA_DEHUM_ID, CONF_SWING

        config = {
            CONF_MIDEA_DEHUM_ID: "mock_id",
            CONF_SWING: False
        }

        await to_code(config)

        mock_cg.get_variable.assert_called_once_with("mock_id")
        mock_climate.register_climate.assert_called_once_with("mock_parent", config)
        mock_cg.add_define.assert_not_called()

if __name__ == '__main__':
    unittest.main()
