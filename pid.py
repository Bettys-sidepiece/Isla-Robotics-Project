import  utime
import  machine

class PID:
    
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = 0
        
        self.setpoint = 0
        self.feedback = 0
        self.previous_time = 0
        self.previous_error = 0
        self.cum_error = 0
        self.max_value = 0
        self.min_value = 0
        self.interval = 0
        self.timer1 = machine.Timer(-1) # Virtual timer
        self.output = 0

    
    def set_interval(self, interval):
        self.interval = interval
        self.timer1.init(mode=machine.Timer.PERIODIC, period=interval, callback=self.control)
        self.previous_time = utime.time()
    
    
    def set_limits(self, MAX, MIN):
        self.max_error = MAX
        self.min_error = MIN
        
        
    def set_feedback(self, measure):
        self.feedback = measure        
    
    
    def set_setpoint(self, value):
        self.setpoint  = value
    
    
    def control(self, timer):
        if self.interval == 0:
            raise Exception("TimerError: Timer interval is not set")
        else:
            
            error = self.setpoint - self.feedback
            current_time = utime.time()
            self.dt = current_time - self.previous_time
            
            proportional = self.Kp * error
            self.cum_error = self.cum_error + error * self.dt
            
            # Prevent integral windup
            if (proportional > self.max_value) or (proportional < self.min_value):
                self.cum_error = 0
                
            if self.dt < 1 :
                self.derivative = 0
            else:
                self.derivative = (error - self.previous_error) / self.dt
            self.previous_error = error
            self.previous_time = current_time
            
            self.output = proportional + self.Ki * self.cum_error + self.Kd * self.derivative

    def get_response(self):
        return self.output
    #def control_data(self, timer):
    
    def stop(self):
        self.timer.deinit()

