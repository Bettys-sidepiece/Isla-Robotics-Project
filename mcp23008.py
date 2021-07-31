"""
MCP23008 8-Bit I/O Expander (I2C)
2021 Kuzipa Mumba

Mircopython derivative of Adafruit Circuit Python mcp230xx, mcp23008 and DigitalIO modules designed for the MCP230xx 
Family of I/O Expanders.

https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx/tree/main/adafruit_mcp230xx 

"""
__version__= "0.1"

from micropython import const
from machine import I2C

IODIR   = const(0x00)       # R/W I/O Direction Register
IPOL    = const(0x01)       # R/W Input Polarity Port Register
GPINTEN = const(0x02)       # R/W Interrupt-on-Change Pins
DEFVAL  = const(0x03)       # Default Value Register
INTCON  = const(0x04)       # Interrupt Control Register
IOCON   = const(0x05)       # Configuration Register
GPPU    = const(0x06)       # Pull-Up Resistor Register
INTF    = const(0x07)       # Interrupt Flag Register (read clears)
INTCAP  = const(0x08)       # Interrupt Captured Value For Port Register (READ ONLY)
GPIO    = const(0x09)       # General Purpose I/O Port Register
ADDR    = const(0x20)       # Device Address

BUF = bytearray(3)


def _get_bit(val, bit):
    return val & (1 << bit) > 0


def _enable_bit(val, bit):
    return val | (1 << bit)


def _clear_bit(val, bit):
    return val & ~(1 << bit)


class DEVICE:

    def __init__(self, i2c, address):
        self._device = i2c
        self._addr = address
    
    
    def writeto_then_readfrom(
        self,
        address,
        buffer_out,
        buffer_in,
        *,
        out_start=0,
        out_end=None,
        in_start=0,
        in_end=None,
        stop=False
    ):
        """Write data from buffer_out to an address and then
        read data from an address and into buffer_in
        """
        if out_end:
            self._device.writeto(address, buffer_out[out_start:out_end], stop)
        else:
            self._device.writeto(address, buffer_out[out_start:], stop)

        if not in_end:
            in_end = len(buffer_in)
        read_buffer = memoryview(buffer_in)[in_start:in_end]
        self._device.readfrom_into(address, read_buffer, stop)
        
        
    def write_then_readinto(self,out_buffer,in_buffer,*,out_start=0,out_end=None,in_start=0,in_end=None):

        if out_end is None:
            out_end = len(out_buffer)
        if in_end is None:
            in_end = len(in_buffer)

        self.writeto_then_readfrom(
            self._addr,
            out_buffer,
            in_buffer,
            out_start=out_start,
            out_end=out_end,
            in_start=in_start,
            in_end=in_end,
        )


    def read_8(self, reg):
        # Read an unsigned 8 bit value from the specified 8-bit register.

        BUF[0] = reg & 0xFF
        self.write_then_readinto(BUF, BUF, out_end=1, in_start=1, in_end=2)
        return BUF[1]


    def write_8(self,reg,val):
        # Write an 8 bit value to the specified 8-bit register.

        BUF[0] = reg & 0xFF
        BUF[1] = val & 0xFF
        self._device.writeto(self._addr,BUF,2)


class MCP23008(DEVICE):
    
    def __init__(self,i2c, address=ADDR, reset=True):
        super().__init__(i2c, address)
        if self._device.scan().count(self._addr) == 0:
            raise OSError('MCP23008 not found at I2C address {:#x}'.format(address))

        if reset:
            self.iodir = 0xFF
            self.gppu = 0x00
            self.gpio = 0x00
            self.write_8(IPOL, 0x00)

    @property
    def gpio(self):
        """The raw GPIO output register.  Each bit represents the
        output value of the associated pin (0 = low, 1 = high), assuming that
        pin has been configured as an output previously.
        """
        return self.read_8(GPIO)
    
    @gpio.setter
    def gpio(self, val):
        self.write_8(GPIO,val)
    
    @property
    def iodir(self):
        """The raw IODIR direction register.  Each bit represents
        direction of a pin, either 1 for an input or 0 for an output mode.
        """
        return self.read_8(IODIR)

    @iodir.setter
    def iodir(self, val):
        self.write_8(IODIR,val)

    @property
    def gppu(self):
        """The raw GPPU pull-up register.  Each bit represents
        if a pull-up is enabled on the specified pin (1 = pull-up enabled,
        0 = pull-up disabled).  Note pull-down resistors are NOT supported!
        """
        return self.read_8(GPPU)
    
    @gppu.setter
    def gppu(self, val):
        self.write_8(GPPU,val)

    
    @property
    def ipol(self):
        """The raw IPOL output register.  Each bit represents the
        polarity value of the associated pin (0 = normal, 1 = inverted), assuming that
        pin has been configured as an input previously.
        """
        return self.read_8(IPOL)

    @ipol.setter
    def ipol(self, val):
        self.write_8(IPOL,val)

    def get_pin(self, pin):
        """Convenience function to create an instance of the DigitalInOut class
        pointing at the specified pin of this MCP23008 device.
        """
        if not 0<=pin<=7:
            raise ValueError("Pin out of range. Pin range is 0-7")
        return ExternalIO(pin,self)



class ExternalIO:
    """External input/output of the MCP23008.
      * MCP23008 family does not support pull-down resistors;

    Exceptions will be thrown when attempting to set unsupported pull
    configurations.
    """
    def __init__(self, pin, mcp23008):
        self._pin = pin
        self._device = mcp23008

    
    def IN_OUT(self, value=False):
        self.set_direction(0)
        self.value = value

    def OUT_IN(self, pullup=None, invert_polarity=False):
        self.set_direction(1)
        self.set.pullup(pullup)
        self.invert_polarity = invert_polarity

    def value(self):
        """The value of the pin, either True for high or False for
        low.  Note you must configure as an output or input appropriately
        before reading and writing this value.
        """
        return _get_bit(self._device.gpio, self._pin)
    

    def set_value(self, val):
        if val == 1:
            self._device.gpio = _enable_bit(self._device.gpio, self._pin)
        elif val == 0:
            self._device.gpio = _clear_bit(self._device.gpio, self._pin)
        else:
            raise ValueError("Expected 1 (Input) or 0 (Output)")

    def direction(self):
        """The direction of the pin, either 1 for an input or
        0 for an output.
        """
        if _get_bit(self._device.iodir, self._pin):
            return 1
        return 0
    
    def set_direction(self, val):
        if val == 1:
            self._device.iodir = _enable_bit(self._device.iodir,self._pin)
        elif val == 0:
            self._device.iodir = _clear_bit(self._device.iodir, self._pin)
        else:
            raise ValueError("Expected 1 (Input) or 0 (Output)")

    def pullup(self):
        """Enable or disable internal pull-up resistors for this pin.  A
        value of 1 will enable a pull-up resistor, and None will
        disable it.  Pull-down resistors are NOT supported!
        """
        try:
            if _get_bit(self._device.gppu,self._pin):
                return 1
        except AttributeError as error:
            raise ValueError("Pull-Down resistors are not supported!") from error
        return None

    def set_pullup(self, val):
        try:
            if val is None:
                self._device.gppu = _clear_bit(self._device.gppu, self._pin)
                
            elif val == 1:
            
                self._device.gppu = _enable_bit(self._device.gppu, self._pin)
                
            elif val == 0:
                raise ValueError("Pull-down resistors are not supported!")
            
            else:
                raise ValueError("Expected 1,0, or None states!")
            
        except AttributeError as error:
            raise ValueError("Pull-up/pull-down resistor not supported.") from error

    @property
    def invert_polarity(self):
        """The polarity of the pin, either True for an Inverted or
        False for an normal.
        """
        if _get_bit(self._device.ipol, self._pin):
            return True
        return False
    
    @invert_polarity.setter
    def invert_polarity(self, val):
        if val:
            self._device.ipol = _enable_bit(self._device.ipol, self._pin)
        else:
            self._device.ipol = _clear_bit(self._device.ipol, self._pin)

