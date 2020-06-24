#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile
from pybricks.tools import wait
from pybricks.robotics import DriveBase

#devining variable
target = 33.0
error = 0.0
integral = 0.0
derivative = 0.0
last_error = 0.0
max_speed = 1000
delta_t = 0.004

#setup
sensor = ColorSensor(Port.S2)
left_motor = Motor(Port.D)
right_motor = Motor(Port.B)
robot = DriveBase(left_motor, right_motor, 57, 115)
brick.sound.beep()

def Pid_cal(Kp, Ki, Kd):
    global target, error, integral, derivative, last_error, delta_t
    last_error = error
    currentVal = sensor.reflection()
    print(currentVal)
    error = target - currentVal
    integral += (error + last_error) / 2.0 * delta_t
    derivative = error - last_error / delta_t

    pCor = Kp * error
    iCor = Ki * integral
    dCor = Kd * derivative
    correction = pCor + iCor + dCor
    
    print(pCor, iCor, dCor)
    return correction

#loop start
while True: 
    cor_val = Pid_cal(0.98, 0.00001, 3)
    if cor_val > 100:
        cor_val = 100
    elif cor_val < -100:
        cor_val = -100

    robot.drive(max_speed, cor_val)
#end loop