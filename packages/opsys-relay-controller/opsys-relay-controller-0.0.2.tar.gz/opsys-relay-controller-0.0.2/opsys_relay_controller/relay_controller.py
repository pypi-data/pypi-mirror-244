import time
import serial
from serial import SerialException
from .relay_abstract import RelayAbstract
from .relay_types import RelayTypes

# avoild COMs detection at deployment
try:
    from serial.tools.list_ports import comports
except Exception as e:
    print(e)


BAUDRATE = 9600
SLOT_TIMEOUT = 0.5
BUFFER_SIZE = 8  # fixed buffer size


class RelayController(RelayAbstract):
    """
    USB Relay controller
    """

    def __init__(self, relay_type=RelayTypes.KMTRONIC_8):
        """
        Initialize parameters

        Args:
            relay_type (str, optional): Relay device type.
                                        Defaults to 'KMTRONIC_8'.
        """
        self._message_header = bytes.fromhex('FF')
        self._state_off = bytes.fromhex('00')
        self._state_on = bytes.fromhex('01')
        
        self.relay_type = relay_type

    def connect(self, com_port=None):
        """
        Connect to relay

        Args:
            com_port (str, optional): Serial port name.
                                      Defaults to None.
                   
        Returns:
            None
        """
        if com_port is not None:
            self.conn = serial.Serial(com_port, BAUDRATE)
            self.conn.timeout = SLOT_TIMEOUT
            return
        else:  # no com port provided
            for com, _, _ in sorted(comports()):
                self.conn = serial.Serial(com, BAUDRATE)
                self.conn.timeout = SLOT_TIMEOUT
                # try to receive valida data from buffer
                try:
                    self.switch_status(switch_number=1)
                    return
                except:
                    pass

        raise SerialException("No valid COM port found")

    def disconnect(self):
        """
        Disconnect from relay
        """
        self.conn.close()

    def switch_off(self, switch_number):
        """
        Turn off relay switch

        Args:
            switch_number (int): number of relay slot
        """
        message = self._message_header + \
            bytes.fromhex(f'0{switch_number}') + self._state_off
        self.conn.write(message)
        print(f'Relay switch {switch_number} off')

    def switch_on(self, switch_number):
        """
        Turn on relay switch

        Args:
            switch_number (int): number of relay slot
        """
        message = self._message_header + \
            bytes.fromhex(f'0{switch_number}') + self._state_on
        self.conn.write(message)
        print(f'Relay switch {switch_number} on')

    def read_buffer(self):
        """
        Read buffer output

        Returns:
            list: relay switches statuses binary-like integers (0/1)
        """
        output = b""  # init binary string
        for _ in range(BUFFER_SIZE):  # read from buffer
            output += self.conn.read()

        return list(output)

    def switch_status(self, switch_number):
        """
        Read relay switch current status (open/closed)

        Args:
            switch_number (int): number of relay slot

        Return:
            bool: True if relay switch is on, otherwise False
        """
        if self.relay_type == RelayTypes.KMTRONIC_8:
            status_cmd = bytes.fromhex('09')
            message_tail = bytes.fromhex('00')
            
        elif self.relay_type == RelayTypes.KMTRONIC_1:
            status_cmd = bytes.fromhex('01')
            message_tail = bytes.fromhex('03')
        
        message = self._message_header + status_cmd + message_tail
        
        self.conn.write(message)
        reply = self.read_buffer()
        status = reply[switch_number - 1]

        return bool(status)

    def switch_reset(self, switch_number):
        """
        Reset relay switch

        Args:
            switch_number (int): number of relay slot
        """
        print(f'Reset relay switch {switch_number}')
        self.switch_off(switch_number)
        time.sleep(SLOT_TIMEOUT * 2)
        self.switch_on(switch_number)
