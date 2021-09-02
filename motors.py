import machine
import utime

class MOTORS:
    def __init__(self,MA1=9,MA2=8,PWMA=7,MB1=4,MB2=5,PWMB=6):
        
        self._MA1 = machine.Pin(MA1,machine.Pin.OUT)
        self._MA2 = machine.Pin(MA2,machine.Pin.OUT)
        self._MB1 = machine.Pin(MB1,machine.Pin.OUT)
        self._MB2 = machine.Pin(MB2,machine.Pin.OUT)
        
        self.MAPWM = machine.PWM(machine.Pin(PWMA))
        self.MBPWM = machine.PWM(machine.Pin(PWMB))
        self.LO_PWM = 0
        self.NOM_PWM = 0
        self.HI_PWM = 0
        
        self.timer = machine.Timer()
          
        self.counter1 = 0
        self.counter2 = 0
        self.counter3 = 0
        self.counter4 = 0
    
        self._EA1 = None
        self._EA2  = None
        self._EB1 = None
        self._EB2 = None
        self.state = False
        
        self.M1_Rev = 0
        self.M2_Rev = 0
        self.distance = 0
        self.distance_M1 = 0
        self.distance_M2 = 0
        self.dist_travelled = 0
        self.K = 7*2*30
        self.prev_M2 = 0
        self.prev_M1 = 0
        self.error_M1 = 0
        self.error_M2 = 0
        
    
    
    def speed_control_init(self):
        self.timer.init(period = 100, mode=machine.Timer.PERIODIC, callback=self.pulse_control)
    
    
    def speed_control_deinit(self):
        self.timer.deinit()
    
    def set_PWM(self,LO,MED,HI):
        self.LO_PWM = LO
        self.NOM_PWM = MED
        self.HI_PWM = HI
        
        
    def set_freq(self,freq):
        self.MAPWM.freq(freq) # frequency goes from 10Hz to 20000Hz
        self.MBPWM.freq(freq)
        

    def motor_drive(self):
        self.MAPWM.duty_u16(self.NOM_PWM)
        self.MBPWM.duty_u16(self.NOM_PWM)


    def encoders(self,EA1=19,EB1=16,EA2=None,EB2=None):
        state = False
        self._EA1 = machine.Pin(EA1, machine.Pin.IN)
        self._EB1 = machine.Pin(EB1, machine.Pin.IN)
        
        if EA2 != None and EB2 != None:
            self._EA2 = machine.Pin(EA2, machine.Pin.IN)
            self._EB2 = machine.Pin(EB2, machine.Pin.IN)
            state=True
        self.state = state
    
    
    def interrupt_enable(self):
        if self.state:
            self._EB2.irq(trigger=machine.Pin.IRQ_RISING, handler=self.counter_4_IRQ) #left motor
            self._EA2.irq(trigger=machine.Pin.IRQ_RISING, handler=self.counter_3_IRQ) #right motor
            
        self._EB1.irq(trigger=machine.Pin.IRQ_RISING, handler=self.counter_2_IRQ) #left motor
        self._EA1.irq(trigger=machine.Pin.IRQ_RISING, handler=self.counter_1_IRQ) #right motor
    
    
    def counter_1_IRQ(self,count):
        self.counter1 = self.counter1 + 1
        
    
    def counter_2_IRQ(self,count):
        self.counter2 = self.counter2 + 1
    
    
    def counter_3_IRQ(self,count):
        self.counter1 = self.counter3 + 1
        
        
    def counter_4_IRQ(self,count):
        self.counter4 = self.counter4 + 1
        
        
    def forward(self): 
        self._MA1.value(0)
        self._MA2.value(1)
        self._MB1.value(1)
        self._MB2.value(0)
    
    
    def reverse(self):
        self._MA1.value(1)
        self._MA2.value(0)
        self._MB1.value(0)
        self._MB2.value(1)


    def stop(self):
        self._MA1.value(0)
        self._MA2.value(0)
        self._MB1.value(0)
        self._MB2.value(0)
      
      
    def turnleft(self):
        self._MA1.value(0)
        self._MA2.value(1)
        self._MB1.value(0)
        self._MB2.value(0)


    def turnright(self):
        self._MA1.value(0)
        self._MA2.value(0)
        self._MB1.value(1)
        self._MB2.value(0)
    
    def spotturn_l(self):
        self._MA1.value(1)
        self._MA2.value(0)
        self._MB1.value(1)
        self._MB2.value(0)
        self.distance_
    
    
    def spotturn_r(self):
        self._MA1.value(0)
        self._MA2.value(1)
        self._MB1.value(0)
        self._MB2.value(1)
        
        
    def distance_(self):
        radius = 2.1 #centimeters
        circ = 2*radius * 3.14
        self.distance_M1 = circ*self.M1_Rev
        self.distance_M2 = circ*self.M2_Rev
        self.distance = (self.distance_M1+ self.distance_M2)/2
        self.dist_travelled = self.distance +self.dist_travelled
         
        
    def pulse_control(self,time):
        self.timer.deinit()
    
        self.M1_Rev = self.counter1/self.K
        self.M2_Rev = self.counter2/self.K
        
        self.error_M1 = self.counter1 - self.prev_M1
        self.prev_M1 = self.counter1
        
        self.error_M1 = self.counter2 - self.prev_M2
        self.prev_M2 = self.counter2
        
        self.distance_()
        self.speed_control()
        self.counter1 = 0
        self.counter2 = 0
        self.timer.init(period = 100, mode=machine.Timer.PERIODIC, callback= self.pulse_control)


    def speed_control(self):
        adjust = 0
        pw_M1 = 0
        pw_M2 = 0
        
        if self.error_M1 != self.error_M2:
            if self.error_M1 > self.error_M2:
                adjust = self.error_M1 - self.error_M2
                pw_M2 = pw_M2 + adjust
                
                if pw_M2 > self.HI_PWM:
                    
                    pw_M1 = self.HI_PWM
                    pw_M2 = self.LO_PWM
                    
                else:
                    pw_M1 = pw_M1 - adjust
            else:
                adjust = self.error_M2 - self.error_M1
                pw_M1 = pw_M1 + adjust
                
                if pw_M1 > self.HI_PWM:
                    
                    pw_M2 = self.HI_PWM
                    pw_M1 = self.LO_PWM
                    
                else:
                    pw_M2 = pw_M2 - adjust;
            PWMA = self.MAPWM.duty_u16()+pw_M2
            PWMB = self.MBPWM.duty_u16()+pw_M1
            self.MBPWM.duty_u16(PWMA)
            self.MAPWM.duty_u16(PWMB)

