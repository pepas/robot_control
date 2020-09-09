# -*- coding: utf-8 -*-
"""
Created on  Apr 22 11:40w 2019

@author: josef.svec
"""
# TODO - reset AB and CD -> start PWM -> enable AB and CD
import smbus
import time 
import os, sys, termios, tty
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO

address =0x44
bus=smbus.SMBus(1)
Angle_R=60
Angle_P=60
button_delay = 0.1 #[s] insensivity of the buttons
duration = 0.3 #[s] duration of the selected action
PWM_f = 20000 #[Hz]
duty_max = 95
duty_min = 50
duty_current = 90

LED_PWM_f = 500
LED_duty_max = 50
LED_duty_min = 0
LED_duty_current = 0


motor_l = "P9_14"
motor_p = "P9_16"
reset_AB = "P8_15"
reset_CD = "P8_16"
#LED1 = "P8_13"
LED2 = "P8_19"
EN_3V3 = "P8_18"
#in_OTW = "P8_8"
#in_FAULT= "P8_7"

# print(PWM.VERSION)
PWM.cleanup()
# GPIO.setup(in_OTW, GPIO.IN)
# GPIO.setup(in_FAULT, GPIO.IN)
GPIO.setup(reset_AB, GPIO.OUT)
GPIO.setup(reset_CD, GPIO.OUT)
GPIO.setup(EN_3V3, GPIO.OUT)
GPIO.output(reset_AB, GPIO.LOW)
GPIO.output(reset_CD, GPIO.LOW)
GPIO.output(EN_3V3, GPIO.LOW)
PWM.start(motor_l)
PWM.start(motor_p)
# PWM.set_frequency(motor_l, PWM_f)
# PWM.set_frequency(motor_l, PWM_f)
PWM.set_duty_cycle(motor_l, 50)
PWM.set_duty_cycle(motor_p, 50)

	#PWM.start(LED2)
	#PWM.set_frequency(LED2, LED_PWM_f)
	#PWM.set_duty_cycle(LED2, 0)
def cls():
    os.system("clear")


def Go(L, R, period):
    PWM.set_duty_cycle(motor_l, L)
    PWM.set_duty_cycle(motor_p, R)
    #print("morotl: ", L)
    #print("morotp: ", R)
    GPIO.output(reset_AB, GPIO.HIGH)
    GPIO.output(reset_CD, GPIO.HIGH)
    time.sleep(period)


# Turn all motors off
def StopMotors():
    PWM.stop(motor_l)
    PWM.stop(motor_p)
    GPIO.output(reset_AB, GPIO.LOW)
    GPIO.output(reset_CD, GPIO.LOW)

# Turn both motors in the same direstion
def Forwards():
    Go(duty_current, duty_current, duration)

def Backwards():
    Go(100 - duty_current , 100 - duty_current, duration)

# Turn each motor in opposite direction to spin on the spot
def Left():
    Go(100 - duty_current, duty_current, duration)

def LSlant():
    Go(70, 90, duration)

def Right():
    Go(duty_current, 100 - duty_current, duration)

def RSlant():
    Go(90, 70, duration)

# Change of the duty cycle
def Avance(dc):
    out = dc + 5
    if out >= duty_max:
        out = duty_max
    return out
    
def Retard(dc):
    out = dc - 5
    if out <= duty_min:
        out = duty_min
    return out

# Both motor forced to stand still
def Brake():
    PWM.set_duty_cycle(motor_l, 50)
    PWM.set_duty_cycle(motor_p, 50)
    GPIO.output(reset_AB, GPIO.HIGH)
    GPIO.output(reset_CD, GPIO.HIGH)
    #time.sleep(period)
    

def Light():
    global LED_duty_current
    LED_duty_current = LED_duty_current + 10
    if LED_duty_current > LED_duty_max:
        LED_duty_current = LED_duty_min
    PWM.set_duty_cycle(LED2, LED_duty_current)

def LRoll():
    global Angle_R
    Angle_R=Angle_R+5
    if Angle_R>175:
	Angle_R=175
    bus.write_byte_data(address,4,Angle_R)
def RRoll():
    global Angle_R
    Angle_R=Angle_R-5
    if Angle_R<5:
	Angle_R=5
    bus.write_byte_data(address,4,Angle_R)
def DPitch():
    global Angle_P
    Angle_P=Angle_P+5
    if Angle_P>175:
	Angle_P=175
    bus.write_byte_data(address,3,Angle_P)
def UPitch():
    global Angle_P
    Angle_P=Angle_P-5
    if Angle_P<5:
	Angle_P=5
    bus.write_byte_data(address,3,Angle_P)
# Read an character via the serial
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Process the key pressed
while True:
   # cls()
   # char = getch()
    for line in iter(sys.stdin.readline, ''):
	char=line
	break

    if (char == "b\n"):
        Brake()
	time.sleep(button_delay)
    elif (char == "u"):
        StopMotors()
        PWM.cleanup()
        exit(0)
    elif (char == "a\n"):
        Left()
        time.sleep(button_delay)
    elif (char == "d\n"):
        Right()
        time.sleep(button_delay)
    elif (char == "w\n"):
        Forwards()
        time.sleep(button_delay)
    elif (char == "s\n"):
        Backwards()
        time.sleep(button_delay) 
    elif (char == "f"):
        duty_current = Avance(duty_current)
    elif (char == "r"):
        duty_current = Retard(duty_current)
    elif (char == "q"):
        LSlant()
        time.sleep(button_delay)
    elif (char == "n"):
        LRoll()
        time.sleep(button_delay)
    elif (char == "m"):
        RRoll()
        time.sleep(button_delay)
    elif (char == "k"):
        DPitch()
        time.sleep(button_delay)
    elif (char == "i"):
        UPitch()
        time.sleep(button_delay)
    elif (char == "e"):
        RSlant()
        time.sleep(button_delay)
    elif (char == "l"):
        Light()
        time.sleep(button_delay)
   # print("speed: ", duty_current)
   # print("pitch: ", Angle_P)
   # print("roll: ", Angle_R)
    GPIO.output(reset_AB, GPIO.LOW)
    GPIO.output(reset_CD, GPIO.LOW)



PWM.cleanup()
