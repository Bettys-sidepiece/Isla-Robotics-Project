# Micro_Bot.py
import machine
import utime
import _thread
from pid import PID

#Input for two object detectors
irsensor_1 = machine.Pin(17,machine.Pin.IN) #Left
irsensor_2 = machine.Pin(14,machine.Pin.IN) #Right

#Motor A

MA1 = machine.Pin(4, machine.Pin.OUT)
MA2 = machine.Pin(3, machine.Pin.OUT)
MA1PWM = machine.PWM(machine.Pin(2))
MA1PWM.freq(3000) # frequency goes from 10Hz to 20000Hz

MA1PWM.duty_u16(45875) # 60% Duty Cycle, 100% is 65536

#Motor B
MB1 = machine.Pin(7, machine.Pin.OUT)
MB2 = machine.Pin(8, machine.Pin.OUT)
MB1PWM = machine.PWM(machine.Pin(6))

# frequency goes from 10Hz to 20000Hz.
# A frequency of between 1000 -(~3500) has shown to be most effiencent
MB1PWM.freq(3000)

# 60% Duty Cycle, 100% is 65536
MB1PWM.duty_u16(45875)

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

# PID Speed Control
dummy_var = 0
speed_control = PID(0,0,0) #Kp, Ki, Kd
speed_control.set_interval(500) #In milliseconds
speed_control.set_limits(275,225) #Max and Min Output
speed_control.set_setpoint(250)

speed_control.control(dummy_var)



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
    MA1.value(1)
    MA2.value(0)
    MB1.value(0)
    MB2.value(0)


def turnright():
    MA1.value(0)
    MA2.value(0)
    MB1.value(0)
    MB2.value(1)

 
def avoid():
    if irsensor_1.value() == 0:
        turnleft()
        
    if irsensor_2.value() == 0:
        turnright()


def counter1_IRQ(int1):
    global counter1
    counter1 += 1


def counter2_IRQ(int2):
    global counter2
    counter2 += 1


def pulse_delay(time):
    timer.deinit()
    global counter1, counter2, current_rpm1, current_rpm2, max_rpm1, max_rpm2, speed_control
    current_rpm1 = (counter1/20)*60
    current_rpm2 = (counter2/20)*60
    speed_control.set_feedback(current_rpm1)
    
    print("\n"*20)
    print("Motor A:",str(current_rpm1),"RPM")
    print("Motor B:",str(current_rpm2),"RPM")
    
    if max_rpm1 < current_rpm1:
        max_rpm1 = current_rpm1
        
    if max_rpm2 < current_rpm2:
        max_rpm2 = current_rpm2
           
    print("MA Highest RPM:",str(max_rpm1),"RPM")
    print("MB Highest RPM:",str(max_rpm2),"RPM")
    print("System Feedback :",str(speed_control.feedback))
    print("System Setpoint :",str(speed_control.setpoint))
    print("System Error :",str(speed_control.previous_error))
    print("PID Response(MA):",str(speed_control.get_response()))
    
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
