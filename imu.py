import sys
import smbus			#import SMBus module of I2C
from time import sleep          #import
import math
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value
global GyroErrorX
global GyroErrorY
global GyroErrorZ

def calib():
	global GyroErrorX
	global GyroErrorY
	global GyroErrorZ

	GyroErrorX=0
	GyroErrorY=0
	GyroErrorZ=0
	c=0
	while (c < 200):
    		gyro_x = read_raw_data(GYRO_XOUT_H)
        	gyro_y = read_raw_data(GYRO_YOUT_H)
        	gyro_z = read_raw_data(GYRO_ZOUT_H)

    		GyroErrorX = GyroErrorX + (gyro_x / 131.0)
    		GyroErrorY = GyroErrorY + (gyro_y / 131.0)
    		GyroErrorZ = GyroErrorZ + (gyro_z / 131.0)
    		c=c + 1
  	
  	GyroErrorX = GyroErrorX / 200.0
  	GyroErrorY = GyroErrorY / 200.0
  	GyroErrorZ = GyroErrorZ / 200.0

bus = smbus.SMBus(2) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()
calib()

print (" Reading Data of Gyroscope and Accelerometer")
AX=0
AY=0
PI=math.pi
Axsum=0
Aysum=0
i=0
while True:
	
	#Read Accelerometer raw value
	acc_x = read_raw_data(ACCEL_XOUT_H)
	acc_y = read_raw_data(ACCEL_YOUT_H)
	acc_z = read_raw_data(ACCEL_ZOUT_H)
	
	#Read Gyroscope raw value
	gyro_x = read_raw_data(GYRO_XOUT_H)
	gyro_y = read_raw_data(GYRO_YOUT_H)
	gyro_z = read_raw_data(GYRO_ZOUT_H)
	
	#Full scale range +/- 250 degree/C as per sensitivity scale factor
	Ay = - acc_x/16384.0 * 180 / PI
	Ax = acc_y/16384.0 * 180 / PI
	Az = 0
	
	Gx = gyro_x/131.0 - GyroErrorX
	Gy = gyro_y/131.0 - GyroErrorY
	Gz = gyro_z/131.0 - GyroErrorZ
	AX = AX + Gx  
        AY = AY + Gy 
	ax= 0.5 * AX + 0.5 * Ax
        ay= 0.5 * AY + 0.5 * Ay
	i=i+1	
	Axsum=Axsum+Ax
	Aysum=Aysum+Ay
	if i==9:
		Axprum=Axsum/10.0
		Ayprum=Aysum/10.0
		print "%.2f"%Az,"%.2f"%Axprum,"%.2f" %Ayprum,
		sys.stdout.flush()
		Axsum=0
		Aysum=0
		i=0
	#print ("Gx=%.2f" %Gx, "Gy=%.2f" %Gy, "Gz=%.2f" %Gz, "Ax=%.2f g" %Ax, "Ay=%.2f g" %Ay, "Az=%.2f g" %Az) 	
        sleep(0.01)
