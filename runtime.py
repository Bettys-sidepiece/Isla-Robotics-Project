import machine
import utime
from motors import *
from utilities import *
from sensors import *

    
class RUNTIME():
    def __init__(self):
        
        self.LO = 35000
        self.MED = 40000
        self.HI = 45000
        self.drive = MOTORS()
        self.drive.set_PWM(LO=self.LO,MED=self.MED,HI=self.HI)
        self.drive.set_freq(100)
        self.drive.motor_drive()
        self.drive.encoders()
    
        self.prox = PROXIMITY()
        self.line = LINE()
        self.bat = BATTERY()
        self.util = UTILITIES()
        self.reset = machine.Pin(22,machine.Pin.OUT)
        
    
    def run(self):
        self.drive.stop()
        self.util.start_up()
        self.drive.interrupt_enable()
        self.bat.bat_sensor_en()
        while True:
            self.menu()
            
    
    def disp_bat(self):
        self.util.oled.text(self.bat.bat_str(),43,55)
    
    
    def object_tracking(self):
        self.util.buzzer()
        self.util.buzzer()
        self.util.title_screen("OBJECT","TRACKING",35,20)
        utime.sleep(1.5)
        run_bat = str(round(self.bat.battery,2))+"V"
        self.bat.bat_deinit()
        
        while self.util.io.input(6):
            self.prox.proximity_enable()
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
                
            self.util.oled.text(run_bat,43,55) 
            self.ui() 
            
            if not self.util.io.input(7):
                self.util.buzzer()
                while self.util.io.input(7):
                    self.util.oled.fill(0)
                    self.util.oled.text("PAUSED",35,30)
                    self.util.OT_header()
                    self.util.oled.show()   
                break
            
            if not self.util.io.input(6):
                self.util.buzzer()
                self.bat.bat_sensor_en()
                break


    def proximity_calibration(self):
        
        self.util.buzzer()
        self.util.buzzer()
        self.util.title_screen("PROXIMITY","CALIBRATION",30,20)
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
        self.util.buzzer()
        self.util.title_screen("OBSTACLE","AVOIDING",35,25)
        utime.sleep(1)
        run_bat = str(round(self.bat.battery,2))
        self.bat.bat_deinit()
        self.drive.speed_control_init()
        self.prox.proximity_enable()
        utime.sleep(0.5)
        while self.util.io.input(6):
            
            if self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 0:
                utime.sleep_ms(6)
                self.util.oled.fill(0)
                self.drive.forward()
                
            elif self.prox.prox_right.value() == 1 and self.prox.prox_left.value() == 1 and self.prox.prox_cntrR.value() == 1 and self.prox.prox_cntrL.value() == 1:
                utime.sleep_ms(6)
                self.util.prox_disp(1,1,1,1)
                self.drive.reverse()
                self.drive.speed_control_deinit()
                self.drive.stop()
                utime.sleep(0.2)
                self.drive.turnright()
                utime.sleep(0.9)
                self.drive.speed_control_init()
            
            elif self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 1:
                self.drive.speed_control_deinit()
                utime.sleep_ms(6)
                self.util.prox_disp(0,1,0,0)
                self.drive.turnleft()
                utime.sleep_ms(15)
                self.drive.speed_control_init()
                
            elif self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 1 and self.prox.prox_cntrL.value() == 0:
                self.drive.speed_control_deinit()
                utime.sleep_ms(6)
                self.util.prox_disp(0,0,1,0)
                self.drive.turnright()
                utime.sleep_ms(15)
                self.drive.speed_control_init()
                
            elif self.prox.prox_right.value() == 1 and self.prox.prox_left.value() == 0 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 0:
                self.drive.speed_control_deinit()
                utime.sleep_ms(6)
                self.util.prox_disp(0,0,0,1)
                self.drive.turnleft()
                utime.sleep_ms(15)
                self.drive.speed_control_init()
                
            elif self.prox.prox_right.value() == 0 and self.prox.prox_left.value() == 1 and self.prox.prox_cntrR.value() == 0 and self.prox.prox_cntrL.value() == 0:
                self.drive.speed_control_deinit()
                utime.sleep_ms(6)
                self.util.prox_disp(1,0,0,0)
                self.drive.turnright()
                utime.sleep_ms(15)
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
            utime.sleep(1.1)
            self.drive.stop()
            utime.sleep(0.2)
            self.drive.forward()
            utime.sleep(2)
            self.drive.stop()
            utime.sleep(0.2)
            self.drive.turnright()
            utime.sleep(0.3)
            
            self.util.title_screen("TURNING","LEFT",34,45)
            self.ui()
            
            self.drive.stop()
            utime.sleep(0.5)
            self.drive.turnleft()
            utime.sleep(1.1)
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
            
            self.drive.stop()
            utime.sleep(0.75)
            self.drive.reverse()
            utime.sleep(2)
            
            self.util.oled.fill(0)
            self.util.title_screen("TEST","COMPLETE",45,30)
            self.util.oled.text(run_bat+"V",43,55) 
            self.ui()
            self.util.oled.fill(0)
            self.drive.stop()
            self.util.buzzer()
            self.util.buzzer()
            
            self.drive.speed_control_deinit()
            self.bat.bat_sensor_en()
            break


    def _prox(self):
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
        while self.util.io.input(6):
            self.util.oled.fill(0)
            self.util.oled.text("About",45,5)
            self.util.oled.text("ISLA",45,20)
            self.util.oled.text("Copyright 2021",10,30)
            self.util.oled.text("By Kuzipa Mumba",5,40)
            self.util.disp_back()
            self.util.oled.show()

            if not self.util.io.input(6):
                self.util.buzzer()
                break
            
            
    def settings(self):
        self.util.prev_pos = 20
        while self.util.io.input(6):
            self.util.menu_options("Settings","Battery","Sensors","Motors")
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
        self.util.prev_pos = 20
        while self.util.io.input(6):
            self.util.menu_options("Sensors","Scale Prox","Scale Line","Battery")
            self.util.cursor(self.util.prev_pos)
            if not self.util.io.input(5):
                self.util.cursor_up()
                
            elif not self.util.io.input(4):
                self.util.cursor_down()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 20:
                self.util.buzzer()
                self.proximity_calibration()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 30:
                self.util.buzzer()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 40:
                self.util.buzzer()
                
            self.icon(True)
            
            if not self.util.io.input(6):
                self.util.buzzer()
                break
     
    def motors_(self):
        self.util.prev_pos = 20
        while self.util.io.input(6):
            self.util.menu_options("Motors","Set Speed","Test","Stats")
            self.util.cursor(self.util.prev_pos)
            if not self.util.io.input(5):
                self.util.cursor_up()
                
            elif not self.util.io.input(4):
                self.util.cursor_down()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 20:
                self.util.buzzer()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 30:
                self.util.buzzer()
                self.motor_test()
                
            elif not self.util.io.input(7)and self.util.prev_pos == 40:
                self.util.buzzer()
                
            self.icon(True)
            
            if not self.util.io.input(6):
                self.util.buzzer()
                break
    
    
    def set_speed(self):
        self.util.prev_pos = 20
        while self.util.io.input(6):
            self.util.menu_options("Set Speed","HI Speed","MED Speed","LO Speed")
            self.util.cursor(self.util.prev_pos)
            
            if not self.util.io.input(5):
                self.util.cursor_up()
                
            elif not self.util.io.input(4):
                self.util.cursor_down()
                
        
    def verify(self):
        self.util.oled.fill(0)
        self.util.oled.text("Are you sure",25,30)
        self.util.oled.text("yes",7,55)
        self.util.oled.text("no",122,55)
     
     
    def menu(self):
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
        
        self.icon(False)
        
        
    
    def ui(self):
        self.util.disp_back()
        self.util.oled.show()
          
    def icon(self,scr):
        if scr :
            self.util.disp_back()
        self.util.disp_up()
        self.util.disp_down()
        self.disp_bat()
        self.util.disp_sel()
        self.util.oled.show()
        


