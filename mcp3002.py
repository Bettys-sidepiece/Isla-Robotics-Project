import machine
import utime

class MCP3002():
    def __init__(self,cs=17,spi_rx=16,spi_tx=19,spi_sck=18,reset = True):
        
        self.spi=machine.SPI(0,
                             firstbit = machine.SPI.MSB,
                             baudrate=1000000,
                             sck=machine.Pin(spi_sck),
                             mosi=machine.Pin(spi_tx),
                             miso=machine.Pin(spi_rx),
                             polarity=0,
                             phase=0)
        
        self._cs = machine.Pin(cs, machine.Pin.OUT)
        
        if reset:
            self._cs.value(0)
            self._cs.value(1)
            reset = False
    
    def adc_read(self,channel):
        cmd = 0xC0
        if channel != 0:
            channel = 1
            cmd = 0xE0
            
    #  First bit (Start): Logic high (1)
    #  Second bit (SGL/DIFF): 1 to select single mode
    #  Third bit (ODD/SIGN): Select channel (0 or 1)
    #  Fourth bit (MSFB): 0 for LSB first
    #  Next 12 bits: 0 (don't care)
        data = bytearray(2)
        filler = bytearray([0b00])
        buf = bytearray([cmd, 0x00])
        
        self._cs.value(0)
        self.spi.write(filler)
        self.spi.write(buf)
        self.spi.write_readinto(buf,data)
        self._cs.value(1)

        # Construct single integer out of the data (2 bytes)
        adc = 0
        for n in data:
            adc = (adc << 8) + n

        # Last bit (0) is not part of ADC value, shift to remove it
        adc = adc >> 1

        # Calculate voltage form ADC value
        voltage = (3.3 * adc) / 1024

        return voltage
       
       
        

