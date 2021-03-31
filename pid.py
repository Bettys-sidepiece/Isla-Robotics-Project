import  utime
import  machine

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
        
#         self.max_value = 0
#         self.min_value = 0
        self.dt = 0
        self.output = 0
        

    
    def set_interval(self, interval):
        self.dt = interval/1000
    
    
#     def set_limits(self, MAX, MIN):
#         self.max_error = MAX
#         self.min_error = MIN
        
        
    def set_feedback(self, measure):
        self.feedback = measure        
    
    
    def set_setpoint(self, value):
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
    

    #def control_data(self, timer):
  

