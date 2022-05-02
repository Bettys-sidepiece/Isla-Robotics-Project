#include "pico/stdlib.h"
#include "hardware/pwm.h"
#include "hardware/gpio.h"
#include "hardware/timer.h"

// Setup Motor control logic pins
const uint MA1 = 4;
const uint MA2 = 3;

const uint MB1 = 7;
const uint MB2 = 6;

//Allocate GPIO 4 and 6 for the PWM Signal
const uint PWMA = 2;
const uint PWMB = 5;

const uint EA1 = 19;
const uint EB1 = 16;
const uint EA2 = 18;
const uint EB2 = 17;

int counter1 = 0;
int counter2 = 0;
int M1_RPM = 0;
int M2_RPM = 0;
const int K = 7*2*30;
int prev_M2 = 0;
int prev_M1 = 0;
int error_M1 = 0;
int error_M2 = 0;
int adjust = 0;

const int pw_max = 250;
const int pw_min = 220;
int pw_M1 = 0;
int pw_M2 = 0;
int PWM1 = 230;
int PWM2 = 230;

void counter_1();
void counter_2();

void forward();
void reverse();
void right();
void left();
void stop();

bool timer_callback();
void motor_test();
void speed_control();


int main(){

//stdio_init_all();

//Set pin functions 
    gpio_init(MA1);
    gpio_set_dir(MA1, GPIO_OUT);

    gpio_init(MB1);
    gpio_set_dir(MB1, GPIO_OUT);

    gpio_init(MA2);
    gpio_set_dir(MA2, GPIO_OUT);

    gpio_init(MB2);
    gpio_set_dir(MB2, GPIO_OUT);

// PWM Pin allocation and configuration
    gpio_set_function(PWMA, GPIO_FUNC_PWM);
    gpio_set_function(PWMB, GPIO_FUNC_PWM);

    uint PWMA_ = pwm_gpio_to_slice_num(PWMA);
    uint PWMB_ = pwm_gpio_to_slice_num(PWMB);

//Set the frequency of each cycle i.e 251
    pwm_set_wrap(PWMA_, 250);
    pwm_set_wrap(PWMB_, 250);

//Set the channels for ?% duty cycle
    pwm_set_chan_level(PWMA_, PWM_CHAN_A, PWM1);
    pwm_set_chan_level(PWMB_, PWM_CHAN_B, PWM2);

    pwm_set_enabled(PWMA_, true);
    pwm_set_enabled(PWMB_, true);

    gpio_set_irq_enabled_with_callback(EA1, GPIO_IRQ_EDGE_RISE,true, &counter_1);
    gpio_set_irq_enabled_with_callback(EB1, GPIO_IRQ_EDGE_RISE,true, &counter_2);

    struct repeating_timer timer;
    add_repeating_timer_ms(1000, timer_callback, NULL, &timer);
    
    while (true){
        tight_loop_contents();
        forward();
        }
    }


void motor_test(){
    forward();
    sleep_ms(5000);
    stop();
    sleep_ms(1000);
    reverse();
    sleep_ms(5000);
    stop();
    sleep_ms(1000);
    left();
    sleep_ms(1000);
    forward();
    sleep_ms(2000);
    right();
    sleep_ms(1000);
    forward();
    sleep_ms(2000);
    stop();
}


bool timer_callback(struct repeating_timer *t){
    bool cancel_repeating_timer (repeating_timer_t *timer);
    M1_RPM = (counter1/K)*60;
    M2_RPM = (counter2/K)*60;

    error_M1 = counter1 - prev_M1;
    prev_M1 = counter1;

    error_M2 = counter2 - prev_M2;
    prev_M1 = counter2;

    counter1 = 0;
    counter2 = 0;

    speed_control();
    struct repeating_timer timer;
    add_repeating_timer_ms(1000, timer_callback, NULL, &timer);
}


void speed_control(){
    if(error_M1!=error_M2){
        if(error_M1>error_M2){

            adjust = (error_M1-error_M2);
            pw_M2 = pw_M2 + adjust;

            if(pw_M2 > pw_max){

                pw_M2 = pw_max;
                pw_M1 = pw_min; 
            }
            else{
                pw_M1 = pw_M1 - adjust;
            }
        }
        else{
            adjust =(error_M2 - error_M1);

            pw_M1 = pw_M1 + adjust;
            if (pw_M1 > pw_max){

                pw_M1 = pw_max;
                pw_M2 = pw_min;
            }
            else{
                pw_M2 = pw_M2 - adjust;
            }
        }
        PWM1 = pw_M1;
        PWM2 = pw_M2;
    }
}


void counter_1(){
    counter1++;
}


void counter_2(){
    counter2++;
} 


void forward(){
    gpio_put(MA1, 1);
    gpio_put(MA2, 0);
    gpio_put(MB1, 0);
    gpio_put(MB2, 1);
}


void reverse(){
    gpio_put(MA1, 0);
    gpio_put(MA2, 1);
    gpio_put(MB1, 1);
    gpio_put(MB2, 0);
}


void left(){
    gpio_put(MA1, 1);
    gpio_put(MA2, 0);
    gpio_put(MB1, 0);
    gpio_put(MB2, 0);
}


void right(){
    gpio_put(MA1, 0);
    gpio_put(MA2, 0);
    gpio_put(MB1, 0);
    gpio_put(MB2, 1);
}


void stop(){
    gpio_put(MA1, 0);
    gpio_put(MA2, 0);
    gpio_put(MB1, 0);
    gpio_put(MB2, 0);
}
