#MCP3002 CLASS
#Copyright (c) 2021
#Author: Kuzipa Mumba for the RP2040 Raspberry Pi Pico

import machine
import utime

class MCP3002():
    def __init__(self,cs=17,spi_rx=16,spi_tx=19,spi_sck=18,reset = True):
        
        self.spi=machine.SPI(0,
                             firstbit = machine.SPI.MSB,
                             baudrate=1200000,
                             sck=machine.Pin(spi_sck),
                             mosi=machine.Pin(spi_tx),
                             miso=machine.Pin(spi_rx),
                             polarity=0,
                             phase=0)
        
        self._cs = machine.Pin(cs, machine.Pin.OUT)
        
        if reset:
            reset = False
            
    def adc_init(self):
        self._cs.value(1)
        self.spi.init()
        
    def adc_deinit(self):
        self.spi.deinit()
        
    def adc_read(self,channel):
        
        if channel != 0:
            channel = 1
   
    #  First bit (Start): Logic high (1)
    #  Second bit (SGL/DIFF): 1 to select single mode
    #  Third bit (ODD/SIGN): Select channel (0 or 1)
    #  Fourth bit (MSFB): 0 for LSB first
    #  Next 12 bits: 0 (don't care)
        data = bytearray(2)
        cmd = 0b11
        cmd = ((cmd<<1) + channel) << 5
        
        print("byte:",str(cmd))
        cmd = bytearray([cmd])
        blank = bytearray(0x00)
        print("bytearray")
        
        self._cs.value(0)
        self.spi.write(cmd)
        data = self.spi.read(2)
        self._cs.value(1)
        
        print("Data In:",str(data),"\n")

        # Construct single integer out of the data (2 bytes)
        adc = 0
        for n in data:
            adc = (adc << 8) + n

        # Last bit (0) is not part of ADC value, shift to remove it
        adc = adc >> 1

        # Calculate voltage form ADC value
        voltage = (adc) / 10240

        return voltage
       
       
        



       
       
        

