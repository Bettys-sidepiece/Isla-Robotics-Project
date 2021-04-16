import utime
import machine
import os

class PID:
    
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        
        self.setpoint = 0
        self.feedback = 0
        self.previous_time = 0
        self.previous_error = 0
        
        self.derivative = 0
        self.integral = 0
        self.proportional = 0
        self.file_opened = False
        self.dt = 0
        self.output = 0
        self.max_out = 0
        self.min_out = 0
        self.control_file = None
        

    def set_interval(self, interval):
        self.dt = interval/1000
    
    
    def set_limits(self, MAX, MIN):
         self.max_out = MAX
         self.min_out = MIN
        
        
    def set_feedback(self, measure):
        self.feedback = measure        
    
    
    def set_target(self, value):
        self.setpoint  = value
    
    
    def change_in_error(self, error):
        if (error > 0 ) and self.previous_error < 0:
            return True
        if (error < 0 ) and self.previous_error > 0:
            return True
        return False
    
    
    def update(self):
        if self.dt == 0:
            raise Exception("TimerError: Timer interval is not set")
        else:
            error = self.setpoint - self.feedback
            
            if self.change_in_error(error) == True:
                self.integral = 0
                
            self.integral += error * self.dt
            
            self.proportional = self.Kp * error
            
            if self.dt > 0 : 
                self.derivative = (error - self.previous_error) / (self.dt)
            else:
                self.derivative = 0
            
            self.previous_error = error
            self.output = (self.proportional + self.Ki * self.integral + self.Kd * self.derivative)
            if self.output > self.max_out:
                self.output = self.max_out
            if self.output < self.min_out:
                self.output = self.min_out
            return self.output
          
    def get_output(self):
        return self.output
    
    
    def get_setpoint(self):
        return self.setpoint
    
    
    def get_integral(self):
        return self.intergral
    
    
    def get_derivative(self):
        return self.derivative
    
    
    def get_feedback(self):
        return self.feedback
    
    
    def control_data(self, output, name):
        if name == "":
            raise Exception("Device Name not Entered.")
        else:   
            filename = "PID Data("+str(name)+")"
            file_ls = os.listdir()
            
            if output == "Terminal":
                print("\n",filename,":")
                print("\nSetpoint ("+name+"):",str(self.setpoint))
                print("\nFeedback ("+name+"):",str(self.feedback))
                print("\nPrevious Error("+name+"):",str(self.previous_error))
                print("\nProportional ("+name+"):",str(self.proportional))
                print("\nIntegral("+name+"):",str(self.integral))
                print("\nKi("+name+"):",str(self.Ki))
                print("\nDerivative("+name+"):",str(self.derivative))
                print("\nKd("+name+"):",str(self.Kd))
                print("\nPID Response("+name+"):",str(self.update()))
                
            elif output == "File":
            
                if (filename+".txt") not in file_ls and self.file_opened == False:
                    self.control_file = open((filename+".txt"), "w")
                    self.file_opened = True
                    print("Creating control data file")
                    
                elif (filename+".txt") in file_ls and self.file_opened == True:
                    print("Writing to control data file")
                    self.control_file.write("\n"+filename)
                    self.control_file.write("\n")
                    self.control_file.write("\nSetpoint("+str(name)+"):"+ str(self.setpoint))
                    self.control_file.write("\nFeedback("+str(name)+"):"+ str(self.feedback))
                    self.control_file.write("\nPrevious Error("+str(name)+"):"+ str(self.previous_error))
                    self.control_file.write("\nProportional("+name+"):"+ str(self.proportional))
                    self.control_file.write("\nIntegral("+name+"):"+ str(self.integral))
                    self.control_file.write("\nDerivative("+name+"):"+ str(self.derivative))
                    self.control_file.write("\nPID Response("+name+"):"+ str(self.update())+"\n")
                    self.control_file.write("-----------------------------------")
                    self.control_file.flush()
                    
    def read_control_data(self, name):
        
        file_ls = os.listdir()
        filename = "PID Data ("+str(name)+").txt"
        if filename in file_ls:
            self.control_file.read(filename)
        self.control_file.close()
        
  

