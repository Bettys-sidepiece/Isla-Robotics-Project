#Motor Speed Control
#mini_bot.py
#Author : Kuzipa Mumba
import machine
import utime
from pid import PID

#PWM Definitions
LO_PWM = 25000 #65% Duty Cycle
NOM_PWM = 40000 #75% Duty Cycle
HI_PWM = 50000# 80% Duty Cycle

#Motor A
MA1 = machine.Pin(4, machine.Pin.OUT)
MA2 = machine.Pin(2, machine.Pin.OUT)

MA1PWM = machine.PWM(machine.Pin(3))
MA1PWM.freq(1000) # frequency goes from 10Hz to 20000Hz
PWMA = NOM_PWM
MA1PWM.duty_u16(PWMA)

#Motor B
MB1 = machine.Pin(8, machine.Pin.OUT)
MB2 = machine.Pin(7, machine.Pin.OUT)

MB1PWM = machine.PWM(machine.Pin(6))
MB1PWM.freq(1000)
PWMB = NOM_PWM
MB1PWM.duty_u16(PWMB)

# Speed sensor inputs
MS1 = machine.Pin(16, machine.Pin.IN)
MS2 = machine.Pin(17, machine.Pin.IN)
timer = machine.Timer(-1)

#Infrared Sensor inputs
ir1 = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)  #Right Sensor
ir2 = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_DOWN)  #Left Sensor

# Counter variables
counter1 = 0
counter2 = 0
current_rpm1 = 0
current_rpm2 = 0
last_updated = 0


#PID Speed Control
            #Kp,Ki,Kd
M1_ctrl = PID(2,0.4,0)
M2_ctrl = PID(2,0.4,0)

M1_ctrl.set_interval(1000)
M2_ctrl.set_interval(1000)

M1_ctrl.set_limits(1000, -1000)
M2_ctrl.set_limits(1000, -1000)

M1_ctrl.set_target(123)
M2_ctrl.set_target(123)


def oled_scroll():
    for i in range (0, 164):
        oled.scroll(1,0)
        oled.show()
        utime.sleep(0.01)
        
            
def clear_oled():
    oled.fill(0)
    oled.show()


def speed_control():
    global PWMA,PWMB
    error1 = M1_ctrl.setpoint - current_rpm1
    error2 = M2_ctrl.setpoint - current_rpm2
    
    if M1_ctrl.output > 0 and error1 != 0:
        PWMA += 655 + M1_ctrl.output*10
#         print("PWMA++")
    if M1_ctrl.output < 0 and error1 != 0:
        PWMA -= 655 + abs(M1_ctrl.output*10)
#         print("PWMA--")
        
    if M2_ctrl.output > 0 and error2 != 0:
        PWMB += 655 + M2_ctrl.output*10   
#         print("PWMB++")   
           
    if M2_ctrl.output < 0 and error2 != 0:
        PWMB -= 655 + abs(M2_ctrl.output*10)
#         print("PWMB--")
        
    if PWMA > HI_PWM:
        PWMA = HI_PWM
#         print("PWMA = HI_PWM")
            
    if PWMA < LO_PWM:
        PWMA = LO_PWM
#         print("PWMA = LO_PWM")
        
    if PWMB > HI_PWM:
        PWMB = HI_PWM
#         print("PWMB = HI_PWM")
        
    if PWMB  < LO_PWM:
        PWMB = LO_PWM
#         print("PWMB = HI_PWM")
    
    MA1PWM.duty_u16(int(PWMA))
    MB1PWM.duty_u16(int(PWMB))
    
    
def avoid():
    global last_updated
    
    if ir1.value() == 0:
        timer.deinit()
        turnleft()
        utime.sleep(0.25)
        last_updated = 2
        timer.init(period = 1000, mode=machine.Timer.PERIODIC, callback=pulse_delay)
        
    if ir2.value() == 0:
        timer.deinit()
        turnright()
        utime.sleep(0.25)
        last_updated = 1
        timer.init(period = 1000, mode=machine.Timer.PERIODIC, callback=pulse_delay)
    
    if ir2.value() == 0 and ir1.value() == 0:
        timer.deinit()
        stop()
        utime.sleep(0.1)
        reverse()
        utime.sleep(0.7)
        if last_updated == 1:
            turnleft()
            utime.sleep(0.3)
        if last_updated == 2:
            turnright()
            utime.sleep(0.3)
        timer.init(period = 1000, mode=machine.Timer.PERIODIC, callback=pulse_delay)

def forward():
    MA1.value(1)
    MA2.value(0)
    MB1.value(1)
    MB2.value(0)
    
    
def reverse():
    MA1.value(0)
    MA2.value(1)
    MB1.value(0)
    MB2.value(1)


def stop():
    MA1.value(0)
    MA2.value(0)
    MB1.value(0)
    MB2.value(0)
  
  
def turnleft():   
    MA1.value(1)
    MA2.value(0)
    MB1.value(0)
    MB2.value(0)


def turnright():
    MA1.value(0)
    MA2.value(0)
    MB1.value(1)
    MB2.value(0)
 
 
def counter1_IRQ(int1):
    global counter1
    counter1 += 1
    
    
def counter2_IRQ(int2):
    global counter2
    counter2 += 1
    
    
def pulse_delay(time):
    #Deinitialise timer1 to allow print and calculations
    timer.deinit()
    global counter1, counter2, current_rpm1, current_rpm2
    
    #The if statements below are intended to control the number of pulses from the
    #speed sensor, by limiting them to a value slightly higher than the expected value.
    #In the case of the Dc hobby motors, 200RPM at 6V, therefore the max has been set to 315RPM.
    if counter1 > 105:
        counter1 = 105
    if counter2 > 105:
        counter2 = 105
    
    #M1 RPM
    current_rpm1 = ((counter1/20)*60)
    #M2 RPM
    current_rpm2 = ((counter2/20)*60)
    
    #The PID.set_feedback(var) function sets the feedback for the PID controller. The feedback for this
    #system is the the respective speed of each motor
    M1_ctrl.set_feedback(current_rpm1)
    M2_ctrl.set_feedback(current_rpm2)
    
    #Print to shell statements to observe and analyse the speed and PWM of each motor
#     print("\nMotor Speed:")
#     print("\t\nM1:",str(current_rpm1),"RPM")
#     print("\t\nM2:",str(current_rpm2),"RPM")
#     print("\tPWM[RAW](M1):",str((PWMA/65536)*100))
#     print("\tPWM[RAW](M2):",str((PWMB/65536)*100))
#     
    #M1_ctrl.control_data("Terminal","M1")
    #M2_ctrl.control_data("Terminal","M2")
    
    #Reset counter variable
    counter1 = 0
    counter2 = 0
    
    #Initiates the PID control loop     
    M1_ctrl.update()
    M2_ctrl.update()
    
    #Calls the speed control function      
    speed_control()
    
    #Initialise timer one 
    timer.init(period = 1000, mode=machine.Timer.PERIODIC, callback=pulse_delay)

#Main function
def run():
    stop()
    utime.sleep(2)
    timer.init(period = 1000, mode=machine.Timer.PERIODIC, callback=pulse_delay)
    while True:
        forward()
        avoid()
        

#INTERRUPTS
MS1.irq(trigger=machine.Pin.IRQ_RISING, handler=counter1_IRQ) #left motor
MS2.irq(trigger=machine.Pin.IRQ_RISING, handler=counter2_IRQ) #right motor


#Run the main function
run()

