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
        self.max_value = 0
        self.min_value = 0
        self.interval = 0
        self.output = 0

    
    def set_interval(self, interval):
        self.interval = interval
    
    
    def set_limits(self, MAX, MIN):
        self.max_error = MAX
        self.min_error = MIN
        
        
    def set_feedback(self, measure):
        self.feedback = measure        
    
    
    def set_setpoint(self, value):
        self.setpoint  = value
    
    
    def control(self):
        if self.interval == 0:
            raise Exception("TimerError: Time interval is not set")
        else:
            error = self.setpoint - self.feedback
            
            proportional = self.Kp * error
            self.integral = self.integral + error * self.interval/1000
            
            # Prevent integral windup
            if (proportional > self.max_value) or (proportional < self.min_value):
                self.integral = 0
            self.derivative = (error - self.previous_error) / (self.interval/1000)
        
            self.output = (proportional + self.Ki * self.integral + self.Kd * self.derivative)
            self.previous_error = error
            
    def get_response(self):
        return self.output
    
    #def control_data(self, timer):
    
    def stop(self):
        self.timer.deinit()

