# Micro_Bot.py

import machine
import utime

#Input of two object detectors
irsensor_1 = machine.Pin(17,machine.Pin.IN) #Left
irsensor_2 = machine.Pin(14,machine.Pin.IN) #Right

#Input of the 
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
button1 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

#Motor A
MA1 = machine.Pin(4, machine.Pin.OUT)
MA2 = machine.Pin(3, machine.Pin.OUT)
MA1PWM = machine.PWM(machine.Pin(2))
MA1PWM.freq(3000) # frequency goes from 10Hz to 20000Hz
MA1PWM.duty_u16(39321) # 60% Duty Cycle, 100% is 65536

#Motor B
MB1 = machine.Pin(7, machine.Pin.OUT)
MB2 = machine.Pin(8, machine.Pin.OUT)
MB1PWM = machine.PWM(machine.Pin(6))

# frequency goes from 10Hz to 20000Hz.
# A frequency of between 1000 -(~3500) has shown to be most effiencent,
#but you are free to experiment with the frequency
MB1PWM.freq(3000)

# 60% Duty Cycle, 100% is 65536
MB1PWM.duty_u16(39321) 

global count
count = 0


def forward():
    MA1.value(0)
    MA2.value(1)
    MB1.value(1)
    MB2.value(0)
    
    
def reverse():
    MA1.value(1)
    MA2.value(0)
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
    MA1.value(0)
    MA2.value(1)
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
        turnleft()
        utime.sleep(1)
        stop()
        utime.sleep(1)
        reverse()
        print("\tReversing")
        utime.sleep(4)
        turnright()
        utime.sleep(1)
        stop()
        print("\tStop\n")
        global count
        count = count + 1
        
    print("Test sequence complete")


def button_irq(but):
    if button.value() == 1:
        print("\n"*20)
        print("Motors: Stopped")
        stop()
        while button1.value() == 1:
            utime.sleep(0.1)
        print("Motors: Starting")
            
def avoid(pin):
    if irsensor_1.value() == 0:
        
        print("\nIR1:Obstacle Detected\nTurning left")
        stop()
        utime.sleep(0.25)
        reverse()
        utime.sleep(1)
        turnright()
        utime.sleep(0.5)
        
    if irsensor_2.value() == 0:
        print("\nIR2:Obstacle Detected\nTurning right")
        stop()
        utime.sleep(0.25)
        reverse()
        utime.sleep(1)
        turnleft()
        utime.sleep(0.5)
        
   

#Main function
def run():
    while True:
        forward()
    
#Interrupt Request Queue
button.irq(trigger=machine.Pin.IRQ_RISING, handler=button_irq)
irsensor_1.irq(trigger=machine.Pin.IRQ_RISING, handler=avoid)
irsensor_2.irq(trigger=machine.Pin.IRQ_RISING, handler=avoid)

#Run the main function
run()
