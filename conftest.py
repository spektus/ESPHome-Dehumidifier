import sys
import unittest.mock

mock_cg = unittest.mock.MagicMock()
mock_cv = unittest.mock.MagicMock()
mock_button = unittest.mock.MagicMock()
mock_uart = unittest.mock.MagicMock()
mock_const = unittest.mock.MagicMock()
mock_const.ENTITY_CATEGORY_CONFIG = "config"
mock_const.CONF_ID = "id"
mock_const.CONF_UART_ID = "uart_id"

sys.modules['esphome'] = unittest.mock.MagicMock()
sys.modules['esphome.codegen'] = mock_cg
sys.modules['esphome.config_validation'] = mock_cv
sys.modules['esphome.components'] = unittest.mock.MagicMock()
sys.modules['esphome.components.button'] = mock_button
sys.modules['esphome.components.uart'] = mock_uart
sys.modules['esphome.const'] = mock_const
