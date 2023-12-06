import unittest
from unittest.mock import patch, MagicMock
from opsys_relay_controller.relay_controller import RelayController


class Test(unittest.TestCase):
    @ classmethod
    def setUp(self):
        pass

    @ classmethod
    def setUpClass(cls):
        pass

    @ classmethod
    def tearDownClass(cls):
        pass

    @ patch.object(RelayController, 'connect')
    def test_connect(self, relay_mock: MagicMock):
        port = 'COM3'
        relay_conn = RelayController()
        relay_conn.connect(port)
        relay_mock.assert_called_once_with('COM3')

    @ patch.object(RelayController, 'disconnect')
    def test_disconnect(self, relay_mock: MagicMock):
        relay_conn = RelayController()
        relay_conn.disconnect()
        relay_mock.assert_called_once_with()

    @ patch.object(RelayController, 'switch_off')
    def test_switch_off(self, relay_mock: MagicMock):
        switch = 1
        relay_conn = RelayController()
        relay_conn.switch_off(switch)
        relay_mock.assert_called_once_with(switch)

    @ patch.object(RelayController, 'switch_on')
    def test_switch_on(self, relay_mock: MagicMock):
        switch = 1
        relay_conn = RelayController()
        relay_conn.switch_on(switch)
        relay_mock.assert_called_once_with(switch)

    @ patch.object(RelayController, 'switch_status')
    def test_switch_status(self, relay_mock: MagicMock):
        switch = 1
        relay_conn = RelayController()
        relay_conn.switch_status(switch)
        relay_mock.assert_called_once_with(switch)

    @ patch.object(RelayController, 'switch_reset')
    def test_switch_reset(self, relay_mock: MagicMock):
        switch = 1
        relay_conn = RelayController()
        relay_conn.switch_reset(switch)
        relay_mock.assert_called_once_with(switch)


if __name__ == '__main__':
    unittest.main()
