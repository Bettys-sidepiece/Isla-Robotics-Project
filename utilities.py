#UTILITIES CLASS
#Copyright (c) 2021
#Author: K.Mumba for the RP2040 Raspberry Pi Pico

import machine
import utime
from ssd1306 import SSD1306_I2C
import mcp23008


class UTILITIES():
    """ Utilities is used to control the OLED display, On-board buzzer and external GPIO pins
        On the ISLA PROJECT
    """
    def __init__(self,setup = True):
        """ Initialise the external devices, and control variables"""
        i2c = machine.I2C(0,scl = machine.Pin(21), sda= machine.Pin(20), freq = 400000)
        self.oled = SSD1306_I2C(128,64,i2c)
        self.io = mcp23008.MCP23008()
        
        self.prev_pos = 20   #Cursor position default
        self.prev_display = None #Variable default
         
        if setup:
            """ System set up to initialise the external GPIO pins on the MCP23008"""
            outPins = list(range(0,4)) #Generate a list of ints from 0 - 3
            for pinNum in outPins:
                self.io.setup(pinNum, mcp23008.OUT) #Set pins 0-3 of the MCP23008 to outputs 
                
            inPins = list(range(4,8)) #Generate a list of ints from 4 - 7
            for pinNum in inPins:
                self.io.setup(pinNum,mcp23008.IN) #Set pins 4-7 of the MCP23008 to inputs 
                self.io.pullup(pinNum,True)  #Use the internal pull-ups on the MCP23008 on each input
              
              
    def buzzer(self):
        """ Generate a tone from the on board buzzer"""
        utime.sleep(0.1)
        for i in range(50):
            for j in range(1):
                self.io.output(0,1)
            for k in range(1):
                self.io.output(0,0)
        self.io.output(0,0)
        utime.sleep(0.2)
        
        
    def start_up(self):
        """ System start up screen sequence"""
        self.buzzer()
        self.oled.contrast(15)
        self.oled.fill(0)
        self.oled.fill_rect(45, 0, 32, 32, 1)
        self.oled.fill_rect(47, 2, 28, 28, 0)
        self.oled.vline(53, 8, 22, 1)
        self.oled.vline(60, 2, 22, 1)
        self.oled.vline(66, 8, 22, 1)
        self.oled.fill_rect(71, 24, 2, 4, 1)
        self.oled.text('MicroPython', 20, 45, 1)
        self.oled.show()
        utime.sleep(1)
        
        self.oled.fill(0)
        self.oled.fill_rect(35,10,58,40,1)
        self.oled.fill_rect(40,15,48,30,0)
        self.oled.text("ISLA",45,28)
        self.oled.show()
        self.oled.fill(0)
        utime.sleep(1) 
    
    
    def disp_back(self):
        """ Back user icon"""
        self.oled.text("<",5,7)
        

    def disp_sel(self):
        """ select user icon"""
        self.oled.text("+",5,53)
        
        
    def disp_up(self):
        """ up user icon"""
        self.oled.text("^",120,7)


    def disp_down(self):
        """ down user icon."""
        self.oled.text("v",120,53)
        
        
    def cursor(self,pos):
        """ generates the cursors and a controls its positionon the screen."""
        
        if self.prev_pos < 20:    # Lower limit for the cursor to go before it wraps around.
            self.oled.fill_rect(15,0,5,64,0)
            self.oled.text(">",15,40)
            pos = 40 #Resets the cursor to the upper limit.
            
        elif self.prev_pos > 40:  # Upper limit for the cursor to go before it wraps around.
            self.oled.fill_rect(0,0,10,64,0)
            self.oled.text(">",15,20)
            pos = 20 #Resets the cursor back to the lower limit.
        
        else:
            if self.prev_pos == 50:  # Upper limit for the cursor to go before it wraps around.
                self.oled.fill_rect(0,0,10,64,0)
        
            elif self.prev_pos == 10:  # Upper limit for the cursor to go before it wraps around.
                self.oled.fill_rect(0,0,10,64,0)
                
            self.oled.fill_rect(0,0,10,64,0)  #Places the cursor where the user needs it to be.
            self.oled.text(">",15,pos)
        self.prev_pos = pos  #Store the current position of the cursor.
    
    
    def cursor_up(self):
        """ Allows for upward navigate of the cursor."""
        self.buzzer()
        self.cursor(self.prev_pos-10)  #Subtracts 10 from the current value of the current position
        
        
    def cursor_down(self):
        """ Allows for downward navigation of the cursor."""
        self.buzzer()
        self.cursor(self.prev_pos+10)  #Adds 10 to the current value of the current position
        
        
    def menu_options(self,title,opt_1,opt_2,opt_3):
        """ Takes three strings to generate a screen of menu
            options.
        """
        self.oled.fill(0)  #Clears the screen
        self.oled.text(title,35,5)
        self.oled.text(opt_1,30,20)
        self.oled.text(opt_2,30,30)
        self.oled.text(opt_3,30,40)
    
    
    def title_screen(self,line1,line2,x_1,x_2):
        """ Takes two strings and to position integers
            used to display text before a mode is engaged.
        """
        self.oled.fill(0)
        self.oled.text(line1,x_1,20)
        self.oled.text(line2,x_2,30)
        self.oled.show()
        
        
    def OT_header(self):
        """ Header for Object tracking"""
        self.oled.text("OBJECT TRACKING",15,10)
        self.disp_back
        
        
    def OA_header(self):
        """ Header for Obstacle avoidance mode"""
        self.oled.text("PROXIMITY",25,45)
        self.disp_back
        
        
    def maze_header(self):
        """ Header for Maze Solver"""
        self.oled.text("MAZE SOLVER",25,5)
        self.disp_back
    
    
    def line_header(self):
        """ Header for Line tracking"""
        self.oled.text("LINE TRACKING",25,5)
        self.disp_back
    
    
    def combat_header(self):
        """ Header for Combat Mode"""
        self.oled.text("COMBAT",35,5)
        self.disp_back
    
    def prox_disp(self,l,cl,cr,r):
        """Used to display dots showing which IR sensor on the proximity sensor
           has detected an object
        """
        self.oled.fill(0)
        self.oled.fill_rect(10, 25, 15, 15, l)
        self.oled.fill_rect(40, 25, 15, 15, cl)
        self.oled.fill_rect(70, 25, 15, 15, cr)
        self.oled.fill_rect(100, 25, 15, 15, r)
    
    def stats(self,dist,speed,time):
        
        dist_ = ("Distance:"+str(round(distance,2))+"cm")
        rpm_ = ("Max RPM:"+str(round(speed,2))+"RPM")
        speed_ = ("Max RPM:"+str(round(speed,2))+"cm/s")
           
        self.oled.fill(0)
        self.oled.text("ISLA STATS",40,5)
        self.oled.text(dist_,20,20)
        self.oled.text(rpm_,20,30)
        self.oled.text(speed_,20,40)
       
