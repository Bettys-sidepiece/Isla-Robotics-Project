#MOTORS CLASS
#Copyright (c) 2021
#Author: Kuzipa Mumba for the RP2040 Raspberry Pi Pico

import machine
import utime

class MOTORS:
    """ The Motors class configures motor parameters of the ISLA robot motors
        enabling for motor and speed control.
    """
    def __init__(self,MA1=9,MA2=8,PWMA=7,MB1=4,MB2=5,PWMB=6):
        """ Set Motor control and PWM pins, and initialise other motor
            control parameters and variables
        """
        #Motor control Declarations
        self._MA1 = machine.Pin(MA1,machine.Pin.OUT)
        self._MA2 = machine.Pin(MA2,machine.Pin.OUT)
        self._MB1 = machine.Pin(MB1,machine.Pin.OUT)
        self._MB2 = machine.Pin(MB2,machine.Pin.OUT)
        
        self.MAPWM = machine.PWM(machine.Pin(PWMA))
        self.MBPWM = machine.PWM(machine.Pin(PWMB))
        
        self.LO_PWM = 0 #Default Setting
        self.NOM_PWM = 0 #Default Setting
        self.HI_PWM = 0 #Default Setting
        
        #Initialise a virtual timer for periodic speed control
        self.timer = machine.Timer()
         
        #Initialise counter variables
        self.counter1 = 0 # Default Motor A phase A signal counter variable (EA1)
        self.counter2 = 0 # Default Motor B phase A signal counter variable (EB1) 
        self.counter3 = 0 # Default Motor A phase A signal counter variable (EA2)
        self.counter4 = 0 # Default Motor B phase A signal counter variable (EB2)  
    
        #Initailise encoder input variables 
        self._EA1 = None # Default Motor A phase A signal input 
        self._EA2 = None # Default Motor B phase A signal input
        self._EB1 = None # Default Motor A phase B signal input
        self._EB2 = None # Default Motor B phase B signal input
        
        self.state = False #Default state for encoder select variable
        
        #Intialise speed control 
        self.M1_Rev = 0
        self.M2_Rev = 0
        self.distance = 0
        self.distance_M1 = 0
        self.distance_M2 = 0
        self.dist_travelled = 0
        self.K = 7*2*30 # Constant 
        self.prev_M2 = 0
        self.prev_M1 = 0
        self.error_M1 = 0
        self.error_M2 = 0
        
    
    def speed_control_init(self):
        """ initialise motor speed control.
        """
        self.timer.init(period = 100, mode=machine.Timer.PERIODIC, callback=self.pulse_control)
    
    
    def speed_control_deinit(self):
        """Deinitialise the motor speed control
        """
        self.timer.deinit()
    
    
    def set_PWM(self,LO,MED,HI):
        """ Enables user to set the Min,Mid and Max PWM signal
            sent to the motors.
        """
        self.LO_PWM = LO
        self.NOM_PWM = MED
        self.HI_PWM = HI
        
        
    def set_freq(self,freq):
        """ Set the frequency of the PWM signal
        """
        self.MAPWM.freq(freq) # frequency goes from 10Hz to 20000Hz
        self.MBPWM.freq(freq)
        

    def motor_drive(self):
        """Enables the motors and sets the PWM to user-defined MID 
        """
        self.MAPWM.duty_u16(self.NOM_PWM)
        self.MBPWM.duty_u16(self.NOM_PWM)


    def encoders(self,EA1=19,EB1=16,EA2=None,EB2=None):
        """ Set motor encoder inputs pins.
        """
        state = False #Default state for encoder local select variable
        self._EA1 = machine.Pin(EA1, machine.Pin.IN)
        self._EB1 = machine.Pin(EB1, machine.Pin.IN)
        
        if EA2 != None and EB2 != None: 
            self._EA2 = machine.Pin(EA2, machine.Pin.IN)
            self._EB2 = machine.Pin(EB2, machine.Pin.IN)
            state=True #sets state for global encoder select variable to true 
        self.state = state
    
    
    def interrupt_enable(self):
        """ Function enables the internal edge interrupts on the 2 or 4 of the
            Encoder inputs depending on the declared inputs.
        """
        if self.state:
            self._EB2.irq(trigger=machine.Pin.IRQ_RISING, handler=self.counter_4_IRQ) #left motor
            self._EA2.irq(trigger=machine.Pin.IRQ_RISING, handler=self.counter_3_IRQ) #right motor
            
        self._EB1.irq(trigger=machine.Pin.IRQ_RISING, handler=self.counter_2_IRQ) #left motor
        self._EA1.irq(trigger=machine.Pin.IRQ_RISING, handler=self.counter_1_IRQ) #right motor
    
    
    def counter_1_IRQ(self,count):
        """ Counter 1 interupt routine
        """
        self.counter1 = self.counter1 + 1  
        
    
    def counter_2_IRQ(self,count):
        """ Counter 2 interupt routine
        """
        self.counter2 = self.counter2 + 1
    
    
    def counter_3_IRQ(self,count):
        """ Counter 3 interupt routine
        """
        self.counter1 = self.counter3 + 1
        
        
    def counter_4_IRQ(self,count):
        """ Counter 4 interupt routine
        """
        self.counter4 = self.counter4 + 1
        
        
    def forward(self):
        """ Sets both motors rotation direction to clockwise
        """
        self._MA1.value(0)
        self._MA2.value(1)
        self._MB1.value(1)
        self._MB2.value(0)
    
    
    def reverse(self):
        """ Sets both motors rotation direction to anti-clockwise
        """
        self._MA1.value(1)
        self._MA2.value(0)
        self._MB1.value(0)
        self._MB2.value(1)


    def stop(self):
        """ Sets both motors to "OFF"
        """
        self._MA1.value(0)
        self._MA2.value(0)
        self._MB1.value(0)
        self._MB2.value(0)
      
      
    def turnleft(self):
        """ Sets the right motor rotation direction to clockwise
        """
        self._MA1.value(0)
        self._MA2.value(1)
        self._MB1.value(0)
        self._MB2.value(0)

        
    def turnright(self):
        """ Sets the left motor rotation direction to clockwise
        """
        self._MA1.value(0)
        self._MA2.value(0)
        self._MB1.value(1)
        self._MB2.value(0)
    
    
    def spotturn_l(self):
        """ Sets the right motor rotation direction to clockwise
            and the left motor rotation direction to anti-clockwise
        """
        self._MA1.value(1)
        self._MA2.value(0)
        self._MB1.value(1)
        self._MB2.value(0)
    
    
    def spotturn_r(self):
        """ Sets the left motor rotation direction to clockwise
            and the right motor rotation direction to anti-clockwise
        """
        self._MA1.value(0)
        self._MA2.value(1)
        self._MB1.value(0)
        self._MB2.value(1)
        
        
    def distance_(self):
        """ Determines the distance travelled by each motor
        """
        radius = 2.1 # Default radius of wheels used in cm
        circ = 2*radius * 3.14 #Circumfrence of the wheel
        
        self.distance_M1 = circ*self.M1_Rev #Calculate the distance travelled by motor A
        self.distance_M2 = circ*self.M2_Rev #Calculate the distance travelled by motor B
        
        self.distance = (self.distance_M1+ self.distance_M2)/2 # Calculate the average distance travelled by the robot
        self.dist_travelled = self.distance +self.dist_travelled # Cumulative the average distance travelled by the robot
        
         
        
    def pulse_control(self,time):
        """ Timer interrupt function calculates the rotation, error of each motor
            and calls distance and speed control functions.
        """
        self.timer.deinit() #Disable the virtual timer
    
        self.M1_Rev = self.counter1/self.K
        self.M2_Rev = self.counter2/self.K
        
        self.error_M1 = self.counter1 - self.prev_M1
        self.prev_M1 = self.counter1
        
        self.error_M1 = self.counter2 - self.prev_M2
        self.prev_M2 = self.counter2
        
        self.distance_() # Call the distance function
        self.speed_control() # Call the speed control function
        self.counter1 = 0 # Reset Counter 1
        self.counter2 = 0 # Reset Counter 2
        self.timer.init(period = 100, mode=machine.Timer.PERIODIC, callback= self.pulse_control) #Re-initialise the virtual timer


    def speed_control(self):
        """ Regulates the motor speed of both motors by regularly comparing, adjusting and setting 
            The each motor's encoder pulses proportially to the error observed.
        """
        adjust = 0
        pw_M1 = 0   # Default value of MA pulse width variable
        pw_M2 = 0   # Default value of MB pulse width variable
        
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
                    
            PWMA = self.MAPWM.duty_u16()+pw_M2  # Adjust the current PWM value 
            PWMB = self.MBPWM.duty_u16()+pw_M1  # Adjust the current PWM value
            
            self.MBPWM.duty_u16(PWMA)  # Set the motor B duty adjusted PWM value
            self.MAPWM.duty_u16(PWMB)  # Set the motor A duty adjusted PWM value

