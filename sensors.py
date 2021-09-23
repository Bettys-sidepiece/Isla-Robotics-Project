#SENSORS CLASS
#Copyright (c) 2021
#Author: K.Mumba for the RP2040 Raspberry Pi Pico

import machine
from utilities import *

class BATTERY():
    """ The Battery Class controls the Battery sensor circuity
        on the ISLA board
    """
    def __init__(self):
        
        self.analog_in = machine.ADC(28) 
        self.conversion_factor = 3.3/(65536) #ADC Conversion factor  for 3.3V
        self.timer = machine.Timer(-1) #Virtual Timer
        self.Shutdown = machine.Pin(22,machine.Pin.OUT) #Unused due to  power circuit planning
        self.low_battery = False
        self.util= UTILITIES()
        self.battery = 0
        self.previousVolt = 0
    
    
    def bat_str(self):
        """Display current Battery value
        """
        if self.battery > 3.5:
            text = str(round(self.battery,2))
        else:
            text = "3.45" #Displays the lowest allowed battery level
        return text+"V"
        
        
    def is_battery_low(self):
        """Enable battery monitering
        """
        if self.low_battery:
            return low_battery
        return False
        
        
    def bat_deinit(self):
        """ Disable battery monitering
        """
        self.util.io.output(1,0)
        self.timer.deinit()
        
        
    def read_level(self,time):
        """ read level, reads the current battery level of the device
            by using the ADC input from the on-board battery sensor, converts
            the input value and disables the battery sensor.
        """
        vdiv = 0
        self.timer.deinit()
        self.util.io.output(1,1)
        if self.is_battery_low():
            self.low_bat()
            
        vdiv = self.analog_in.read_u16()*self.conversion_factor
        self.battery =(vdiv*(10+10)/10)
        self.util.io.output(1,0) # Disable battery sensor
        self.timer.init(period = 1000, mode=machine.Timer.PERIODIC, callback=self.read_level)
        
        
    def bat_sensor_en(self):
        """ Sets pin 1 on the MCP23009 high, and enables a one shot timer to initiate
            battery reading
        """
        self.util.io.output(1,1) # Enable battery sensor
        self.timer.init(mode=machine.Timer.ONE_SHOT, period=100, callback=self.read_level)
        
        
    def low_bat(self):
        """ Low battery indicator
        """
        if self.read_level < 4.2:
            self.util.buzzer() #Annoying Buzzer
            utime.sleep(0.5)
               
class LINE():
    """ The Line Class controls the Line sensor circuity
        on the ISLA board
    """
    def __init__(self):
        """ creates variables and a utilities object"""
        self.ir_CR = None
        self.ir_CL = None
        self.ir_L = None
        self.ir_R = None
        self.util= UTILITIES()
        
        
    def line_enable(self):
        """ Sets the external Pin 3 to high, and initialises the two internal ADC pins
            and two external ADC Channels on the MCP3002
        """
        self.util.io.output(2,1) # Enable line sensor
        self.ir_CR = machine.ADC()
        self.ir_CL = machine.ADC()
        self.ir_L = ch0()
        self.ir_R = ch1()
        
        
    def line_disable(self):
        """ Sets the external Pin 2 to low and deinitilises the ADC input pins on the RP2040"""
        self.util.io.output(2,0) #Disable line sensor
        
        
class PROXIMITY():
    """ The PROXIMITY Class controls the proximity sensor circuity
        on the ISLA board
    """
    def __init__(self, PXR=10, PXL=11, PXCL=12, PXCR=13):
        """ Configures the RP2040 pins to Proximity sensor outputs 
        """
        self.util= UTILITIES() #Create an object of the Utlities class
        self._pxr= PXR
        self._pxl= PXL
        self._pxcl= PXCL
        self._pxcr= PXCR
        
        self.prox_left = None
        self.prox_right = None
        self.prox_cntrR = None
        self.prox_cntrL = None
        
       
    def proximity_enable(self):
        """ Sets the external Pin 3 to high, initialises the RP2040's input pins
            and pull-ups to enable sensor readings
        """
        self.util.io.output(3,1)#Enable proximity sensor
        self.prox_left = machine.Pin(self._pxl, machine.Pin.IN, machine.Pin.PULL_UP)
        self.prox_cntrR = machine.Pin(self._pxcr, machine.Pin.IN, machine.Pin.PULL_UP)
        self.prox_cntrL = machine.Pin(self._pxcl, machine.Pin.IN, machine.Pin.PULL_UP)
        self.prox_right = machine.Pin(self._pxr, machine.Pin.IN, machine.Pin.PULL_UP)
        
        
    def proximity_disable(self):
        """ Sets the external Pin 3 to low and deinitilises the input pins on the RP2040
        """
        self.util.io.output(3,0) #Disable proximity sensor
        self.prox_left = None
        self.prox_cntrR = None
        self.prox_cntrL = None
        self.prox_right = None

