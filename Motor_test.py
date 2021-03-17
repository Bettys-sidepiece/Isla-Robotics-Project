import machine
import utime

#This is a pico program to test DC motors.
#In my test I used a TB6612FNG motor  driver and two TT DC gear Motors
#(Modify the program depending on the pins in use)

button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
button1 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

#Motor A
MA1 = machine.Pin(7, machine.Pin.OUT)
MA2 = machine.Pin(8, machine.Pin.OUT)
MA1PWM = machine.PWM(machine.Pin(6))
MA1PWM.freq(2000) # frequency goes from 10Hz to 20000Hz
MA1PWM.duty_u16(39321) # 60% Duty Cycle, 100% is 65536

#Motor B
MB1 = machine.Pin(11, machine.Pin.OUT)
MB2 = machine.Pin(12, machine.Pin.OUT)
MB1PWM = machine.PWM(machine.Pin(10))

# frequency goes from 10Hz to 20000Hz.
# A frequency of between 1000 -(~3500) works best.
# but you are free to experiment with different frequencies.

MB1PWM.freq(2000)

# 60% Duty Cycle, 100% is 65536
MB1PWM.duty_u16(39321) 

global count
count = 0

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
    MA1.value(0)
    MA2.value(0)
    MB1.value(1)
    MB2.value(0)

def turnright():
    MA1.value(1)
    MA2.value(0)
    MB1.value(0)
    MB2.value(0)
    
def test():
    print("Test Sequence initailized\n")
    while count < 4:
        global count
        print("Test:",str(count+1))
        utime.sleep(2)
        forward()
        print("\n\tForward")
        utime.sleep(4)
        stop()
        print("\tStop")
        utime.sleep(2)
        reverse()
        print("\tReversing")
        utime.sleep(4)
        stop()
        print("\tStop\n")
        global count
        count = count + 1
        
    print("Test sequence complete")

test()
        
    
    
