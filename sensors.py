#SENSORS CLASS
#Copyright (c) 2021
#Author: Kuzipa Mumba for the RP2040 Raspberry Pi Pico

import machine
from utilities import *

class BATTERY():
    """
    """
    def __init__(self):
        """
        """
        self.analog_in = machine.ADC(28)
        self.conversion_factor = 3.3/(65536)
        self.timer = machine.Timer(-1)
        self.Shutdown = machine.Pin(22,machine.Pin.OUT)
        self.low_battery = False
        self.util= UTILITIES()
        self.battery = 0
        self.previousVolt = 0
        self._EWMF = []
    
    
    def bat_str(self):
        """
        """
        if self.battery > 3.5:
            text = str(round(self.battery,2))
        else:
            text = "3.45"
        return text+"V"
        
        
    def is_battery_low(self):
        """
        """
        if self.low_battery:
            return low_battery
        return False
        
        
    def bat_deinit(self):
        """
        """
        self.util.io.output(1,0)
        self.timer.deinit()
        
        
    def read_level(self,time):
        """
        """
        vdiv = 0
        self.timer.deinit()
        self.util.io.output(1,1)
        if self.is_battery_low():
            self.low_bat()
            
        vdiv = self.analog_in.read_u16()*self.conversion_factor
        self.battery =(vdiv*(10+10)/10)
#         self.EWMF()
        self.util.io.output(1,0)
        self.timer.init(period = 1000, mode=machine.Timer.PERIODIC, callback=self.read_level)
        
        
    def bat_sensor_en(self):
        """
        """
        self.util.io.output(1,1)
        self.timer.init(mode=machine.Timer.ONE_SHOT, period=100, callback=self.read_level)
        
        
    def low_bat(self):
        """
        """
        if self.read_level < 4.2:
            self.util.buzzer()
            utime.sleep(0.1)
               
class LINE():
    """
    """
    def __init__(self):
        """
        """
        self.ir_CR = None
        self.ir_CL = None
        self.ir_L = None
        self.ir_R = None
        self.util= UTILITIES()
        
        
    def line_enable(self):
        """
        """
        self.util.io.output(2,1)
        self.ir_CR = machine.ADC()
        self.ir_CL = machine.ADC()
        self.ir_L = ch0()
        self.ir_R = ch1()
        
        
    def line_disable(self):
        """
        """
        self.util.io.output(2,0)
        
        
class PROXIMITY():
    """
    """
    def __init__(self, PXR=10, PXL=11, PXCL=12, PXCR=13):
        """
        """
        self.util= UTILITIES()
        self._pxr= PXR
        self._pxl= PXL
        self._pxcl= PXCL
        self._pxcr= PXCR
        
        self.prox_left = None
        self.prox_right = None
        self.prox_cntrR = None
        self.prox_cntrL = None
        
       
    def proximity_enable(self):
        """
        """
        self.util.io.output(3,1)
        self.prox_left = machine.Pin(self._pxl, machine.Pin.IN, machine.Pin.PULL_UP)
        self.prox_cntrR = machine.Pin(self._pxcr, machine.Pin.IN, machine.Pin.PULL_UP)
        self.prox_cntrL = machine.Pin(self._pxcl, machine.Pin.IN, machine.Pin.PULL_UP)
        self.prox_right = machine.Pin(self._pxr, machine.Pin.IN, machine.Pin.PULL_UP)
        
        
    def proximity_disable(self):
        """
        """
        self.util.io.output(3,0)
        self.prox_left = None
        self.prox_cntrR = None
        self.prox_cntrL = None
        self.prox_right = None

