# Micro_Bot.py
import machine
import utime
import _thread
from pid import PID

#Input for two object detectors
irsensor_1 = machine.Pin(17,machine.Pin.IN) #Left
irsensor_2 = machine.Pin(14,machine.Pin.IN) #Right

#PWM Definitions

LO_PWM = 40000 #61% Duty Cycle
NOM_PWM = 46000 #70% Duty Cycle
HI_PWM = 55000 # 84% Duty Cycle

#Motor A
MA1 = machine.Pin(4, machine.Pin.OUT)
MA2 = machine.Pin(3, machine.Pin.OUT)

MA1PWM = machine.PWM(machine.Pin(2))
MA1PWM.freq(3000) # frequency goes from 10Hz to 20000Hz
PWMA = 46000
MA1PWM.duty_u16(PWMA)

#Motor B
MB1 = machine.Pin(7, machine.Pin.OUT)
MB2 = machine.Pin(8, machine.Pin.OUT)

MB1PWM = machine.PWM(machine.Pin(6))
MB1PWM.freq(3000)
PWMB = 46000
MB1PWM.duty_u16(PWMB)

# Speed sensor inputs
MS1 = machine.Pin(10, machine.Pin.IN)
MS2 = machine.Pin(11, machine.Pin.IN)
timer = machine.Timer(-1)

# Counter variables
counter1 = 0
counter2 = 0
current_rpm1 = 0
max_rpm1 = 0
current_rpm2 = 0
max_rpm2 = 0
correction = 0
timeout = 0
sec = 0
mins = 0
hr = 0

# PID Speed Control
#dummy_var = 0
Kp = 2
Ki = 0.1
Kd = 0
#Motor 1
speed_control = PID(Kp,Ki,Kd) #Kp, Ki, Kd
speed_control.set_interval(1000) #In milliseconds
speed_control.set_setpoint(250)

#Motor 2
speed_control2 = PID(Kp,Ki,Kd) #Kp, Ki, Kd
speed_control2.set_interval(1000) #In milliseconds
speed_control2.set_setpoint(250)


def forward():
    MA1.value(1)
    MA2.value(0)
    MB1.value(0)
    MB2.value(1)
    
    
def reverse():
    MA1.value(0)
    MA2.value(1)
    MB1.value(1)
    MB2.value(0)
 
 
def stop():
    MA1.value(0)
    MA2.value(0)
    MB1.value(0)
    MB2.value(0)
  
  
def turnleft():   
    PWMA = 50000
    MA1.value(1)
    MA2.value(0)
    MB1.value(0)
    MB2.value(0)


def turnright():
    
    PWMB = 50000
    MA1.value(0)
    MA2.value(0)
    MB1.value(0)
    MB2.value(1)

 
def avoid():
    global timeout
    if irsensor_2.value() == 0:
        turnleft()
        utime.sleep(0.25)
        
        if timeout >  3:
            reverse()
            utime.sleep(1)
            turnleft()
            utime.sleep(0.25)
            timeout = 0
        
    if irsensor_1.value() == 0:
        turnright()
        utime.sleep(0.25)
        if timeout >  3:
            reverse()
            utime.sleep(1)
            turnleft()
            utime.sleep(0.25)
            timeout = 0
    
    if sec > 0 and current_rpm1 == 0 and current_rpm2 == 0:
        reverse()
        utime.sleep(1)
        turnright()
        
    if irsensor_1.value() == 0 and irsensor_2.value() == 0:
        reverse()
        utime.sleep(2)
        stop()
        utime.sleep(0.1)
        turnleft()
        utime.sleep(1)

    
def runtime():
    global sec, mins, hr
    sec += 1
    if sec == 59:
        mins += 1
        sec = 0
    if mins == 59:
        hr += 1
        mins = 0
        
    print("Runtime -",str(hr)+":"+str(mins)+":"+str(sec),"\n")
    

def counter1_IRQ(int1):
    global counter1
    counter1 += 1
    
    
def counter2_IRQ(int2):
    global counter2
    counter2 += 1


def speed_controller():
    global PWMA, PWMB, LO_PWM, HI_PWM

    if speed_control.previous_error < 0:
        PWMA += abs(speed_control.output)
        if PWMA + abs(speed_control.output) > HI_PWM:
            PWMA -= (speed_control2.output)
            
    if speed_control2.previous_error < 0:
        PWMB += abs(speed_control2.output)
        if PWMB + abs(speed_control2.output) > HI_PWM:
            PWMB -= (speed_control2.output)
            
    if speed_control.previous_error > 0:
        PWMA -= abs(speed_control.output)
        if PWMA - abs(speed_control.output) < LO_PWM:
            PWMA += (speed_control2.output)
            
    if speed_control2.previous_error > 0:
        PWMB -= abs(speed_control2.output)
        if PWMB - abs(speed_control2.output) < LO_PWM:
            PWMB += (speed_control2.output)
    
    PWMB = PWMA
    
def pulse_delay(time):
    timer.deinit()
    global counter1, counter2, current_rpm1, current_rpm2, max_rpm1, max_rpm2

    current_rpm1 = (counter1/20)*60
    current_rpm2 = (counter2/20)*60
    
    speed_control.set_feedback(current_rpm1)
    speed_control.update()
     
    speed_control2.set_feedback(current_rpm2)
    speed_control2.update()
     
    
    print("\n"*10)
    runtime()
    print("Motor Speed Data:")
    print("\n\tM1 Rotational Speed :",str(current_rpm1),"RPM")
    print("\tM2 Rotational Speed:",str(current_rpm2),"RPM")
    
    if max_rpm1 < current_rpm1:
        max_rpm1 = current_rpm1
        
    if max_rpm2 < current_rpm2:
        max_rpm2 = current_rpm2
           
    print("\tM1 Highest RPM:",str(max_rpm1),"RPM")
    print("\tM2 Highest RPM:",str(max_rpm2),"RPM")
    print("\n\tPWM(M1):",str((PWMA/65536)*100),"%")
    print("\tPWM(M2):",str((PWMB/65536)*100),"%")
    print("\tPWM [RAW](M1):",str(PWMA))
    print("\tPWM [RAW](M2):",str(PWMB))
     
    print("\n\nPID Data:",)
    print("\n\tSetpoint(M1):",str(speed_control.setpoint))
    print("\tSetpoint(M2):",str(speed_control2.setpoint))
    print("\n\tFeedback(M1):",str(speed_control.feedback))
    print("\tFeedback(M2):",str(speed_control2.feedback))
    print("\n\tPrevious Error(M1):",str(speed_control.previous_error))
    print("\tPrevious Error(M2):",str(speed_control2.previous_error))
    print("\n\tProportional(M1):",str(speed_control.proportional))
    print("\tProportional(M2):",str(speed_control2.proportional))
    print("\n\tIntegral(M1):",str(speed_control.integral))
    print("\tIntegral(M2):",str(speed_control2.integral))
#     print("\n\tKi(M1):",str(speed_control.Ki))
#     print("\tKi(M2):",str(speed_control2.Ki))
    print("\n\tDerivative(M1):",str(speed_control.derivative))
    print("\tDerivative(M2):",str(speed_control2.derivative))
#     print("\n\tKd(M1):",str(speed_control.Kd))
#     print("\tKd(M2):",str(speed_control2.Kd))
    print("\n\tPID Response(M1):",str(speed_control.output))
    print("\tPID Response(M2):",str(speed_control2.output))
    
    speed_controller()
    counter1 = 0
    counter2 = 0
    timer.init(period = 1000, mode=machine.Timer.PERIODIC, callback=pulse_delay)
    
    
#Main function
def run():
    while True:
        global counter1, counter2
        forward()
        avoid()

#INTERRUPTS
MS1.irq(trigger=machine.Pin.IRQ_RISING, handler=counter1_IRQ)
MS2.irq(trigger=machine.Pin.IRQ_RISING, handler=counter2_IRQ)
timer.init(period = 1000, mode=machine.Timer.PERIODIC, callback=pulse_delay)

#Run the main function
run()
