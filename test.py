# -*- coding: utf-8 -*-
"""
Created on  Apr 22 11:40w 2019

@author: jindrich.jansa, josef.svec
"""
# TODO - reset AB and CD -> start PWM -> enable AB and CD
import time 
import os, sys, termios, tty
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import subprocess

Angle_R=1500000
Angle_P=1500000
video0=False
button_delay = 0.1 #[s] insensivity of the buttons
duration = 0.3 #[s] duration of the selected action
PWM_f = 20000 #[Hz]
duty_max = 95
duty_min = 50
duty_current = 95

LED_PWM_f = 500
LED_duty_max = 50
LED_duty_min = 0
LED_duty_current = 0

SERV_PWM_f=60
motor_l = "P9_14"
motor_p = "P9_16"
reset_AB = "P8_15"
reset_CD = "P8_16"
LED1 = "P8_13"
LED2 = "P8_19"
EN_3V3 = "P8_18"
#in_OTW = "P8_8"
#in_FAULT= "P8_7"
kamera_a = "P9_21"
kamera_b = "P9_22"

PWM.cleanup()
subprocess.Popen("config-pin -a p9-21 pwm",shell=True)
subprocess.Popen("config-pin -a p9-22 pwm",shell=True)
subprocess.Popen("echo 0 > export",cwd="/sys/class/pwm/pwmchip1",shell=True)
subprocess.Popen("echo 1 > export",cwd="/sys/class/pwm/pwmchip1",shell=True)
subprocess.Popen("sudo sh -c 'echo 16666666 > period'",cwd="/sys/class/pwm/pwm-1:0",shell=True)
subprocess.Popen("sudo sh -c 'echo 16666666 > period'",cwd="/sys/class/pwm/pwm-1:1",shell=True)
subprocess.Popen("sudo sh -c 'echo 1 > enable'",cwd="/sys/class/pwm/pwm-1:0",shell=True)
subprocess.Popen("sudo sh -c 'echo 1 > enable'",cwd="/sys/class/pwm/pwm-1:1",shell=True)

PWM.start(LED2)
PWM.set_frequency(LED2, LED_PWM_f)
PWM.set_duty_cycle(LED2, 20)
# print(PWM.VERSION)
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
    Angle_R=Angle_R+90000
    if Angle_R>2000000:
	Angle_R=2000000
    command="sudo sh -c 'echo "+str(Angle_R)+" > duty_cycle'"
    subprocess.Popen(command,cwd="/sys/class/pwm/pwm-1:1",shell=True)
def RRoll():
    global Angle_R
    Angle_R=Angle_R-90000
    if Angle_R<600000:
	Angle_R=600000
    command="sudo sh -c 'echo "+str(Angle_R)+" > duty_cycle'"
    subprocess.Popen(command,cwd="/sys/class/pwm/pwm-1:1",shell=True)
def DPitch():
    global Angle_P
    Angle_P=Angle_P+90000
    if Angle_P>2000000:
	Angle_P=2000000
    command="sudo sh -c 'echo "+str(Angle_P)+" > duty_cycle'"
    subprocess.Popen(command,cwd="/sys/class/pwm/pwm-1:0",shell=True)
def UPitch():
    global Angle_P
    Angle_P=Angle_P-90000
    if Angle_P<600000:
	Angle_P=600000
    command="sudo sh -c 'echo "+str(Angle_P)+" > duty_cycle'"
    subprocess.Popen(command,cwd="/sys/class/pwm/pwm-1:0",shell=True)
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
    elif (char == "n\n"):
        LRoll()
        time.sleep(button_delay)
    elif (char == "m\n"):
        RRoll()
        time.sleep(button_delay)
    elif (char == "k\n"):
        DPitch()
        time.sleep(button_delay)
    elif (char == "i\n"):
        UPitch()
        time.sleep(button_delay)
    elif (char == "e"):
        RSlant()
        time.sleep(button_delay)
    elif (char == "l\n"):
        Light()
        time.sleep(button_delay)
    elif (char == "c\n"):
	subprocess.Popen("sudo systemctl stop mjpg-streamer",shell=True)
	if video0:
	    subprocess.Popen("sed -i 's/video0/video4/' /opt/scripts/tools/software/mjpg-streamer/mjpg-streamer.service",shell=True)
  	    video0=False
	else:
	    subprocess.Popen("sed -i 's/video4/video0/' /opt/scripts/tools/software/mjpg-streamer/mjpg-streamer.service",shell=True)
	    video0=True
	time.sleep(1)
	subprocess.Popen("sudo install -m 644 /opt/scripts/tools/software/mjpg-streamer/mjpg-streamer.service /etc/systemd/system",shell=True)
	subprocess.Popen("sudo systemctl daemon-reload",shell=True)
	time.sleep(1)
	subprocess.Popen("sudo systemctl restart mjpg-streamer",shell=True)

   # print("speed: ", duty_current)
   # print("pitch: ", Angle_P)
   # print("roll: ", Angle_R)
    GPIO.output(reset_AB, GPIO.LOW)
    GPIO.output(reset_CD, GPIO.LOW)



PWM.cleanup()
