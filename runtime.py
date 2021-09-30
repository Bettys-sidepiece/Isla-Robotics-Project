#RUNTIME CLASS
#Copyright (c) 2021
#Author: K.Mumba for the RP2040 Raspberry Pi Pico

import machine
import utime
from motors import *
from utilities import *
from sensors import *

    
class RUNTIME():
    """The RUNTIME CLASS is used to run the device by using other bespoke modules
       to control the motors, enable user to device communication, display text and
       oled display and cohesively control the sensors the device.
    """
    def __init__(self):
        """Configures the Motors,Proximity,Line and UI parameters of  the device"""
        self.LO = 35000  #Low speed default duty cycle
        self.MED = 40000 #Medium speed default duty cycle
        self.HI = 45000  #High speed default duty cycle
        self.speed = ":[M]"
        
        self.drive = MOTORS() #Create object of MOTORS Class
        self.drive.set_PWM(LO=self.LO,MED=self.MED,HI=self.HI) 
        self.drive.set_freq(100)
        self.drive.motor_drive() # Turns on the motors
        self.drive.encoders() # Enables encoders
    
        self.prox = PROXIMITY() #Create object of Proximity Class
        self.line = LINE()   #Create object of Line Class
        self.bat = BATTERY() #Create object of Battery Class
        self.util = UTILITIES()  #Create object of Utilities Class
        self.reset = machine.Pin(22,machine.Pin.OUT) 
        
    
    def run(self): # Main function 
        self.drive.stop() #Reset motors to off
        self.util.start_up() # Run Isla start up screen
        self.drive.interrupt_enable() #Enable encorder interrupt
        self.bat.bat_sensor_en() # Initialise the on-board battery voltage sensor
        while True:
            self.menu() 
            
    
    def disp_bat(self):
        """Displays the current battery voltage at the bottom of
           oled display
        """
        self.util.oled.text(self.bat.bat_str(),43,55)
    
    
    def object_tracking(self):
        """ The object tracking feature uses the four IR leds to
            track and the position of an object in from of the robot.
            Note: Can no be used in areas with extreme light or crowded areas
        """
        self.util.buzzer()
        self.util.buzzer()
        self.util.title_screen("OBJECT","TRACKING",35,25)
        utime.sleep(1.5)
        run_bat = str(round(self.bat.battery,2))+"V" #Hold the volatge at the start of the mode
        self.bat.bat_deinit() # Deinitilise the Battery Sensor
        
        while self.util.io.input(6):
            self.prox.proximity_enable() #Enable Proximity Sensor
            if self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 0:
                utime.sleep_ms(8)
                self.drive.stop()
                self.util.prox_disp(0,0,0,0)
                
            elif self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 1 and self.prox.prox_cntrL.value() == 1:
                utime.sleep_ms(8)
                self.drive.stop
                self.util.prox_disp(0,1,1,0)
                
            elif self.prox.prox_right.value() == 1 and self.prox.prox_left.value() == 1 and self.prox.prox_cntrR.value() == 1 and self.prox.prox_cntrL.value() == 1:
                utime.sleep_ms(8)
                self.drive.stop()
                self.util.prox_disp(1,1,1,1)
                
            elif self.prox.prox_right.value() == 1 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 1:
                utime.sleep_ms(8)
                self.drive.spotturn_l()
                self.util.prox_disp(0,1,0,1)
                utime.sleep_ms(40)
                self.drive.stop()
                
            elif self.prox.prox_right.value() == 1 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 0:
                utime.sleep_ms(8)
                self.drive.spotturn_l()
                self.util.prox_disp(0,0,0,1)
                utime.sleep_ms(25)
                self.drive.stop()
                
            elif self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 1:
                utime.sleep_ms(8)
                self.drive.spotturn_l()
                self.util.prox_disp(0,1,0,0)
                utime.sleep_ms(50)
                self.drive.stop()
                
            elif self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 1 and self.prox.prox_cntrR.value() == 1 and self.prox.prox_cntrL.value() == 0:
                utime.sleep_ms(8)
                self.drive.spotturn_r()
                self.util.prox_disp(1,0,1,0)
                utime.sleep_ms(40)
                self.drive.stop()
            
            elif self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 1 and self.prox.prox_cntrL.value() == 0:
                utime.sleep_ms(8)
                self.drive.spotturn_r()
                self.util.prox_disp(0,0,1,0)
                utime.sleep_ms(50)
                self.drive.stop()
            
            elif self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 1 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 0:
                utime.sleep_ms(8)
                self.drive.spotturn_r()
                self.util.prox_disp(0,1,0,0)
                utime.sleep_ms(25)
                self.drive.stop()
                
            self.util.oled.text(run_bat,43,55) #Display battery laevel at start of mode
            self.ui()
            
            if not self.util.io.input(6): #Exit the mode
                self.util.buzzer()
                self.bat.bat_sensor_en() #Enable battery sensor
                break


    def proximity_calibration(self):
        """ Allows the user to calibrate the sensitivity of the proximity sensors
            using the OLED display and two potentiometers. 
        """
        self.util.buzzer()
        self.util.buzzer()
        self.util.title_screen("PROXIMITY","CALIBRATION",25,20)
        utime.sleep(1)
        run_bat = str(round(self.bat.battery,2))
        self.bat.bat_deinit()
        
        
        while self.util.io.input(6):
            self.prox.proximity_enable()
            if self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 0:
                utime.sleep_ms(6)
                self.util.prox_disp(0,0,0,0)

            if self.prox.prox_right.value() == 1 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 0:
                utime.sleep_ms(6)
                self.util.prox_disp(0,0,0,1)
                
            if self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 1 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 0:
                utime.sleep_ms(6)
                self.util.prox_disp(1,0,0,0)
                
            if self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 1 and self.prox.prox_cntrL.value() == 0:
                utime.sleep_ms(6)
                self.util.prox_disp(0,0,1,0)
                
            if self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 1:
                utime.sleep_ms(6)
                self.util.prox_disp(0,1,0,0)
            
            if self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 1 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 1:
                utime.sleep_ms(6)
                self.util.prox_disp(1,1,0,0)
                
            if self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 1 and self.prox.prox_cntrR.value() == 1 and self.prox.prox_cntrL.value() == 0:
                utime.sleep_ms(6)
                self.util.prox_disp(1,0,1,0)
                
            if self.prox.prox_right.value() == 1 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 1:
                utime.sleep_ms(6)
                self.util.prox_disp(0,1,0,1)
                
            if self.prox.prox_right.value() == 1 and self.prox.prox_left.value() == 1 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 1:
                utime.sleep_ms(6)
                self.util.prox_disp(1,1,0,1)
                
            if self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 1 and self.prox.prox_cntrL.value() == 1:
                utime.sleep_ms(6)
                self.util.prox_disp(0,1,1,0)
                
            if self.prox.prox_right.value() == 1 and self.prox.prox_left.value() == 1 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 0:
                utime.sleep_ms(6)
                self.util.prox_disp(1,0,0,1)
            
            if self.prox.prox_right.value() == 1 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 1 and self.prox.prox_cntrL.value() == 0:
                utime.sleep_ms(6)
                self.util.prox_disp(0,0,1,1)
            
            if self.prox.prox_right.value() == 1 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 1 and self.prox.prox_cntrL.value() == 1:
                utime.sleep_ms(6)
                self.util.prox_disp(0,1,1,1)
            
            if self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 1 and self.prox.prox_cntrR.value() == 1 and self.prox.prox_cntrL.value() == 1:
                utime.sleep_ms(6)
                self.util.prox_disp(1,1,1,0)
                
            if self.prox.prox_right.value() == 1 and self.prox.prox_left.value() == 1 and self.prox.prox_cntrR.value() == 1 and self.prox.prox_cntrL.value() == 0:
                utime.sleep_ms(6)
                self.util.prox_disp(1,0,1,1)
                
            if self.prox.prox_right.value() == 1 and self.prox.prox_left.value() == 1 and self.prox.prox_cntrR.value() == 1 and self.prox.prox_cntrL.value() == 1:
                utime.sleep_ms(6)
                self.util.prox_disp(1,1,1,1)
                
            self.util.oled.text(run_bat+"V",43,55) 
            self.ui()
                
            if not self.util.io.input(6):
                self.util.buzzer()
                self.bat.bat_sensor_en()
                break
        
        
    def proximity_sensor(self):
        """Obstacle avoidance feature"""
        self.util.buzzer()
        self.util.title_screen("OBSTACLE","AVOIDING",35,35)
        utime.sleep(1)
        run_bat = str(round(self.bat.battery,2))  #Record most recent battery level
        self.bat.bat_deinit() 
        self.drive.speed_control_init() #Enable Motor Speed Control
        self.prox.proximity_enable() #Enable Proximity Sensor circuitry
        utime.sleep(0.5)
        while self.util.io.input(6):
            lf = 0
            rt = 0
            if self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 0:
                utime.sleep_ms(6)
                self.util.oled.fill(0)
                self.drive.forward()
                
            elif self.prox.prox_right.value() == 1 and self.prox.prox_left.value() == 1 and self.prox.prox_cntrR.value() == 1 and self.prox.prox_cntrL.value() == 1:
                utime.sleep_us(100)
                self.util.prox_disp(1,1,1,1)
                self.drive.reverse()
                utime.sleep(0.4)
                self.drive.speed_control_deinit() #Disable Motor speed control 
                self.drive.stop()
                utime.sleep(0.3)
                
                self.drive.spotturn_r()
                utime.sleep_ms(250)
                self.drive.stop()
                utime.sleep_ms(600)
                if self.prox.prox_right.value() == 1 and self.prox.prox_left.value()==1:
                    utime.sleep_ms(100)
                    self.util.prox_disp(1,1,1,1)
                    lf = 1
                else:
                    self.util.prox_disp(0,0,0,0)
                     
                self.drive.spotturn_l()
                utime.sleep_ms(250)
                
                self.drive.stop()
                utime.sleep_ms(500)
                
                self.drive.spotturn_l()
                utime.sleep_ms(250)
                self.drive.stop()
                utime.sleep_ms(600)
                if self.prox.prox_right.value() == 1 and self.prox.prox_left.value() == 1:
                    utime.sleep_ms(100)
                    self.util.prox_disp(1,1,1,1)
                    rt = 1
                else:
                    self.util.prox_disp(0,0,0,0)
                    
                self.drive.spotturn_r()
                utime.sleep_ms(250)
                self.drive.forward()
                utime.sleep(0.2)
                self.drive.stop()
                utime.sleep(0.3)
                
                if lf == 1 and rt == 0:
                   # print("lf = 1: rt = 0")
                    self.drive.turnright()
                    utime.sleep(0.6)
                    self.drive.stop()
                    utime.sleep(0.3)
                    
                elif lf == 0 and rt == 1:
                   # print("lf = 0: rt = 1")
                    self.drive.turnleft()
                    utime.sleep(0.6)
                    self.drive.stop()
                    utime.sleep(0.3)
                    
                    
                elif lf == 0 and rt == 0:
                    #print("lf = 0: rt = 0")
                    self.drive.spotturn_r()
                    utime.sleep_ms(600)
                    self.drive.stop()
                    utime.sleep(0.3)
                    
                     
                elif lf == 1 and rt == 1:
                   # print("lf = 1: rt = 1")
                    self.drive.spotturn_r()
                    utime.sleep(1.2)
                    self.drive.stop()
                    utime.sleep(0.3)
                     
                self.drive.speed_control_init()
                    
            
            elif self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 1:
                self.drive.speed_control_deinit()
                self.util.prox_disp(0,1,0,0)
                self.drive.stop()
                utime.sleep_ms(5)
                self.drive.turnleft() 
                utime.sleep_ms(2)
                self.drive.speed_control_init()
                
            elif self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 1 and self.prox.prox_cntrL.value() == 0:
                self.drive.speed_control_deinit()
                self.util.prox_disp(0,0,1,0)
                self.drive.stop()
                utime.sleep_ms(5)
                self.drive.turnright()
                utime.sleep_ms(2)
                self.drive.speed_control_init()
                
            elif self.prox.prox_right.value() == 1 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 0:
                self.drive.speed_control_deinit()
                self.util.prox_disp(0,0,0,1)
                self.drive.stop()
                utime.sleep_ms(2)
                self.drive.turnleft()
                utime.sleep_ms(50)
                self.drive.speed_control_init()
                
            elif self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 1 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 0:
                self.drive.speed_control_deinit()
                self.util.prox_disp(1,0,0,0)
                self.drive.stop()
                utime.sleep_ms(5)
                self.drive.turnright()
                utime.sleep_ms(50)
                self.drive.speed_control_init()
                
            self.util.oled.text(run_bat+"V",43,55)  
            self.ui()
            
            if not self.util.io.input(6):
                self.util.buzzer()
                self.drive.speed_control_deinit()
                self.bat.bat_sensor_en()
                break
            
        self.drive.stop()
        

    def motor_test(self):
        """Test sequence to check the motors are properly connected and functioning"""
        while True:
            run_bat = str(round(self.bat.battery,2))
            self.bat.bat_deinit()
            self.util.buzzer()
            self.util.title_screen("MOTOR","TEST",40,45)
            self.util.oled.text(run_bat+"V",43,55) 
            self.ui()
            self.util.oled.fill(0)
            utime.sleep(1)
            
            self.util.oled.fill(0)
            self.util.oled.text("FORWARD",33,20)
            self.ui()
            self.util.oled.fill(0)
            
            self.drive.stop()
            self.drive.speed_control_init()
            utime.sleep(0.5)
            self.drive.forward()
            utime.sleep(3)
            
            self.util.title_screen("TURNING","RIGHT",34,45)
            self.util.oled.text(run_bat+"V",43,55) 
            self.ui()
            self.util.oled.fill(0)
            self.drive.stop()
            utime.sleep(0.5)
            self.drive.turnright()
            utime.sleep(1.1)
            self.drive.forward()
            utime.sleep(2)
            self.drive.stop()
            utime.sleep(0.2)
            self.drive.turnright()
            utime.sleep(1.3)
            self.drive.stop()
            utime.sleep(0.2)
            self.drive.forward()
            utime.sleep(2)
            self.drive.stop()
            utime.sleep(0.2)
            self.drive.turnright()
            utime.sleep(0.2)
            
            self.util.title_screen("TURNING","LEFT",34,45)
            self.ui()
            
            self.drive.stop()
            utime.sleep(0.5)
            self.drive.turnleft()
            utime.sleep(1.3)
            self.drive.forward()
            utime.sleep(2)
            self.drive.stop()
            utime.sleep(0.2)
            self.drive.turnleft()
            utime.sleep(1.1)
            self.drive.stop()
            utime.sleep(0.2)
            self.drive.forward()
            utime.sleep(2)
            
            self.util.oled.fill(0)
            self.util.oled.text("REVERSE",33,20)
            self.util.oled.text(run_bat+"V",43,55) 
            self.ui()
            self.util.oled.fill(0)
            
            self.drive.speed_control_deinit()
            
            self.drive.stop()
            utime.sleep(0.75)
            
            self.drive.speed_control_init()
            
            self.LO = 25000 
            self.MED = 30000
            self.HI = 35000
            
            self.drive.reverse()
            utime.sleep(3)
            self.drive.speed_control_deinit()
            self.util.oled.fill(0)
            self.util.title_screen("TEST","COMPLETE",45,30)
            self.util.oled.text(run_bat+"V",43,55) 
            self.ui()
            self.util.oled.fill(0)
            self.drive.stop()
            self.util.buzzer()
            self.util.buzzer()
        
            self.bat.bat_sensor_en()
            break


    def _prox(self):
        """Menu for the proximity sensing feature"""
        self.util.prev_pos = 20
        while self.util.io.input(6):
            self.prox.proximity_disable()
            self.util.menu_options("Proximity","Avoid","Track","Maze")
            self.util.cursor(self.util.prev_pos)
            if not self.util.io.input(5):
                self.util.cursor_up()
                
            elif not self.util.io.input(4):
                self.util.cursor_down()
            
            elif not self.util.io.input(7)and self.util.prev_pos == 20:
                self.util.buzzer()
                self.proximity_sensor()
                    
            elif not self.util.io.input(7)and self.util.prev_pos == 30:
                self.util.buzzer()
                self.object_tracking()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 40:
                self.util.buzzer()
             
            self.icon(True)
            
            if not self.util.io.input(6):
                self.util.buzzer()
                break
            
            
    def _line(self):
        """Menu for the line tracking feature"""
        self.util.prev_pos = 20
        while self.util.io.input(6):
            self.util.menu_options("Line","Track","Maze","Q-Maze")
            self.util.cursor(self.util.prev_pos)
            
            if not self.util.io.input(5):
                self.util.cursor_up()
                
            elif not self.util.io.input(4):
                self.util.cursor_down()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 20:
                self.util.buzzer()
                    
            elif not self.util.io.input(7)and self.util.prev_pos == 30:
                self.util.buzzer()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 40:
                self.util.buzzer()
                
            self.icon(True)
            
            if not self.util.io.input(6):
                self.util.buzzer()
                break
        
        
    def mode(self):
        """Menu for the robots features"""
        self.util.prev_pos = 20
        while self.util.io.input(6):
            self.util.menu_options("Mode","Proximity","Line","Battle")
            self.util.cursor(self.util.prev_pos)
            if not self.util.io.input(5):
                self.util.cursor_up()
                
            elif not self.util.io.input(4):
                self.util.cursor_down()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 20:
                self.util.buzzer()
                self._prox()
                    
            elif not self.util.io.input(7)and self.util.prev_pos == 30:
                self.util.buzzer()
                self._line()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 40:
                self.util.buzzer()
                
            self.icon(True)
            
            if not self.util.io.input(6):
                self.util.buzzer()
                break
           

    def about(self):
        #Describes the creator of the device
        while self.util.io.input(6):
            self.util.oled.fill(0)
            self.util.oled.text("About",45,5)
            self.util.oled.text("ISLA",45,20)
            self.util.oled.text("Copyright 2021",10,30)
            self.util.oled.text("By K.Mumba",25,40)
            self.util.disp_back()
            self.util.oled.show()

            if not self.util.io.input(6):
                self.util.buzzer()
                break
            
            
    def settings(self):
        """Settings menu"""
        self.util.prev_pos = 20
        while self.util.io.input(6):
            self.util.menu_options("Settings","Extra","Sensors","Motors")
            self.util.cursor(self.util.prev_pos)
            if not self.util.io.input(5):
                self.util.cursor_up()
                
            elif not self.util.io.input(4):
                self.util.cursor_down()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 20:
                self.util.buzzer()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 30:
                self.util.buzzer()
                self.sensors()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 40:
                self.util.buzzer()
                self.motors_()
            self.icon(True)
            
            if not self.util.io.input(6):
                self.util.buzzer()
                break
     
    
    def sensors(self):
        """Sensors settings Menu"""
        self.util.prev_pos = 20
        while self.util.io.input(6):
            self.util.menu_options("Sensors","Scale Prox","View Line","Battery")
            self.util.cursor(self.util.prev_pos)
            if not self.util.io.input(5):
                self.util.cursor_up()
                
            elif not self.util.io.input(4):
                self.util.cursor_down()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 20:
                #Allows the user to calibrate the proximity sensor using the oled display as feedback and knobs
                self.util.buzzer()
                self.proximity_calibration()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 30:
                #Allows the user to view the line using the oled display as feedback
                self.util.buzzer()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 40:
                #Power management
                self.util.buzzer()
                
            self.icon(True)
            
            if not self.util.io.input(6):
                self.util.buzzer()
                break
     
    
    def motors_(self):
        """Motor settings menu"""
        self.util.prev_pos = 20
        while self.util.io.input(6):
            text = ("Speed"+self.speed)
            self.util.menu_options("Motors",text,"Test","Stats")
            self.util.cursor(self.util.prev_pos)
            if not self.util.io.input(5):
                self.util.cursor_up()
                
            elif not self.util.io.input(4):
                self.util.cursor_down()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 20:
                #Allows the user to define low,med and high speeds
                self.util.buzzer()
                self.set_speed()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 30:
                #Initiates the motor test sequence
                self.util.buzzer()
                self.motor_test()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 40:
                #Allows the view the travel statistics of the device
                self.util.buzzer()
                #self.util.stats()
                
            self.icon(True)
            
            if not self.util.io.input(6):
                self.util.buzzer()
                break
        
        
    def set_speed(self):
        #Enables the user to set the speed of the device
        self.util.prev_pos = 20
        while self.util.io.input(6):
            text = ("Speed"+self.speed)
            self.util.menu_options(text,"Low Speed","Med Speed","Hi Speed")
            self.util.cursor(self.util.prev_pos)
            
            if not self.util.io.input(5):
                self.util.cursor_up()
                
            elif not self.util.io.input(4):
                self.util.cursor_down()
            
            elif not self.util.io.input(7)and self.util.prev_pos == 20:
                #Allows the user to define low,med and high speeds
                self.util.buzzer()
                self.drive.set_PWM(30000,35000,40000)
                self.speed = ":[L]"
                
            elif not self.util.io.input(7)and self.util.prev_pos == 30:
                #Initiates the motor test sequence
                self.util.buzzer()
                self.drive.set_PWM(35000,40000,45000)
                self.speed = ":[M]"
                
            elif not self.util.io.input(7)and self.util.prev_pos == 40:
                #Allows the view the travel statistics of the device
                self.util.buzzer()
                self.drive.set_PWM(40000,45000,50000)
                self.speed = ":[H]"
                
            self.icon(True)
            
            if not self.util.io.input(6):
                self.util.buzzer()
                break
                

    def menu(self):
        #Main Menu
        self.util.oled.fill(0)
        self.util.menu_options("ISLA","Mode","Settings","About")
        self.util.cursor(self.util.prev_pos)
        if not self.util.io.input(5):
            self.util.cursor_up()
                
        elif not self.util.io.input(4):
            self.util.cursor_down()
    
        elif not self.util.io.input(7)and self.util.prev_pos == 20:
            self.util.buzzer()
            self.mode()
                
        elif not self.util.io.input(7)and self.util.prev_pos == 30:
            self.util.buzzer()
            self.settings()
            
        elif not self.util.io.input(7)and self.util.prev_pos == 40:
            self.util.buzzer()
            self.about()
        
        self.icon(False)  #No back button used 
        
        
    def ui(self):
        #UI when features are being run
        self.util.disp_back()
        self.util.oled.show()
        
        
    def icon(self,scr):
        #UI symbols
        if scr :
            self.util.disp_back()
        self.util.disp_up()
        self.util.disp_down()
        self.disp_bat()
        self.util.disp_sel()
        self.util.oled.show()
        
