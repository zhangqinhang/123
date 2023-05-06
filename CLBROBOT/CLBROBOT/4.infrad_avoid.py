#!/usr/bin/python  
# coding=utf-8  
#本段代码实现树莓派智能小车的红外避障效果
#代码使用的树莓派GPIO是用的BOARD编码方式。
"""
* @par Copyright (C): 2010-2020, hunan CLB Tech
* @file         infrad_avoid
* @version      V2.0
* @details
* @par History

@author: zhulin
""" 
import RPi.GPIO as GPIO  
import time  
import sys 
 
SensorRight = 16
SensorLeft  = 12

PWMA   = 18
AIN1   = 22
AIN2   = 27

PWMB   = 23
BIN1   = 25
BIN2   = 24

BtnPin  = 19
Gpin    = 5
Rpin    = 6

#智能小车运动函数 
def t_up(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)
        
def t_stop(t_time):
        L_Motor.ChangeDutyCycle(0)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(0)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)
        
def t_down(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)

def t_left(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)

def t_right(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)
        
def keysacn():
    val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == False:
        val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == True:
        time.sleep(0.01)
        val = GPIO.input(BtnPin)
        if val == True:
            GPIO.output(Rpin,1)
            while GPIO.input(BtnPin) == False:
                GPIO.output(Rpin,0)
        else:
            GPIO.output(Rpin,0)
            
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)       # 按物理位置给GPIOs编号
    GPIO.setup(Gpin, GPIO.OUT)     # 设置绿色Led引脚模式输出
    GPIO.setup(Rpin, GPIO.OUT)     # 设置红色Led引脚模式输出
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # 设置输入BtnPin模式，拉高至高电平(3.3V) 
    GPIO.setup(SensorRight,GPIO.IN)
    GPIO.setup(SensorLeft,GPIO.IN)
	
    GPIO.setup(AIN2,GPIO.OUT)
    GPIO.setup(AIN1,GPIO.OUT)
    GPIO.setup(PWMA,GPIO.OUT)

    GPIO.setup(BIN1,GPIO.OUT)
    GPIO.setup(BIN2,GPIO.OUT)
    GPIO.setup(PWMB,GPIO.OUT)
    
if __name__ == '__main__':
    setup()
    keysacn()
    L_Motor= GPIO.PWM(PWMA,100)
    L_Motor.start(0)
    R_Motor = GPIO.PWM(PWMB,100)
    R_Motor.start(0)
    try:
        while True:
            SR_2 = GPIO.input(SensorRight)
            SL_2 = GPIO.input(SensorLeft)
            if SL_2 == True and SR_2 == True:
                print "t_up"
                t_up(50,0)
            elif SL_2 == True and SR_2 ==False:
                print "Left"
                t_left(50,0)
            elif SL_2==False and SR_2 ==True:
                print "Right"
                t_right(50,0)
            else:
                t_stop(0.3)
                t_down(50,0.4)
                t_left(50,0.5)
    except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行子程序destroy()。
        GPIO.cleanup()
