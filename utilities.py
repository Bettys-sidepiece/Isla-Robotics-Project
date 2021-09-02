import machine
import utime
from ssd1306 import SSD1306_I2C
import mcp23008


class UTILITIES():
    
    def __init__(self,setup = True):
        i2c = machine.I2C(0,scl = machine.Pin(21), sda= machine.Pin(20), freq = 400000)
        self.oled = SSD1306_I2C(128,64,i2c)
        self.io = mcp23008.MCP23008()
        self.prev_pos = 20
        self.prev_display = None
         
        if setup:
            outPins = list(range(0,4))
            nextVals = {}
            for pinNum in outPins:
                self.io.setup(pinNum, mcp23008.OUT)
                
            inPins = list(range(4,8))
            for pinNum in inPins:
                self.io.setup(pinNum,mcp23008.IN)
                self.io.pullup(pinNum,True)
              
              
    def buzzer(self):
        utime.sleep(0.1)
        for i in range(50):
            for j in range(1):
                self.io.output(0,1)
            for k in range(1):
                self.io.output(0,0)
        self.io.output(0,0)
        utime.sleep(0.2)
        
        
    def start_up(self):
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
        self.oled.fill_rect(36,10,58,40,1)
        self.oled.fill_rect(41,15,48,30,0)
        self.oled.text("ISLA",47,28)
        self.oled.show()
        self.oled.fill(0)
        utime.sleep(1) 
    
    
    def disp_back(self):
        self.oled.text("<",5,7)
        

    def disp_sel(self):
        self.oled.text("+",5,53)
        
        
    def disp_up(self):
        self.oled.text("up",110,7)


    def disp_down(self):
        self.oled.text("dn",110,53)
        
        
    def cursor(self,pos):
        if self.prev_pos < 20:
            self.oled.fill_rect(15,0,5,64,0)
            self.oled.text(">",15,40)
            pos = 40
            
        elif self.prev_pos > 40:
            self.oled.fill_rect(0,0,10,64,0)
            self.oled.text(">",15,20)
            pos = 20
            
        else:
            self.oled.fill_rect(0,0,10,64,0)
            self.oled.text(">",15,pos)
        self.prev_pos = pos
    
    
    def cursor_up(self):
        self.buzzer()
        self.cursor(self.prev_pos-10)
        
    def cursor_down(self):
        self.buzzer()
        self.cursor(self.prev_pos+10)
        
        
    def menu_options(self,title,opt_1,opt_2,opt_3):
        self.oled.fill(0)
        self.oled.text(title,35,5)
        self.oled.text(opt_1,30,20)
        self.oled.text(opt_2,30,30)
        self.oled.text(opt_3,30,40)
    
    
    def title_screen(self,line1,line2,x_1,x_2):
        self.oled.fill(0)
        self.oled.text(line1,x_1,20)
        self.oled.text(line2,x_2,30)
        self.oled.show()
        
        
    def OT_header(self):
        self.oled.text("OBJECT TRACKING",15,10)
        self.disp_back
        
        
    def OA_header(self):
        self.oled.text("PROXIMITY",25,45)
        self.disp_back
        
        
    def maze_header(self):
        self.oled.text("MAZE SOLVER",25,5)
        self.disp_back
    
    
    def line_header(self):
        self.oled.text("LINE TRACKING",25,5)
        self.disp_back
    
    
    def combat_header(self):
        self.oled.text("LINE TRACKING",35,5)
        self.disp_back
    
    def prox_disp(self,l,cl,cr,r):
        self.oled.fill(0)
        self.oled.fill_rect(10, 25, 15, 15, l)
        self.oled.fill_rect(40, 25, 15, 15, cl)
        self.oled.fill_rect(70, 25, 15, 15, cr)
        self.oled.fill_rect(100, 25, 15, 15, r)
    


