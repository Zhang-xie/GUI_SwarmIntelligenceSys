import serial
import collections
import yaml
import binascii
import time
import threading
import random
import os
import sys
import enum
import socket
import threading
import json
import math
from pprint import pprint
import numpy as np
#import client as car_client


class SimpleTimer(object):
    def __init__(self, interval, callback):
        self.i = interval
        self.callback = callback
        self.t = threading.Timer(self.i, self.__f)

    def __f(self):
        self.callback()
        self.t = threading.Timer(self.i, self.__f)
        self.t.start()

    def start(self):
        self.t.start()

    def stop(self):
        self.t.cancel()


class MgsType(enum.IntEnum):
    REQUEST_POSE = 4
    REQUEST_IMU = 5
    REQUEST_UltraSonic = 6
    REQUEST_IR_4way = 7
    REQUEST_IR_2way = 8
    REQUEST_SPEED = 9
    REQUEST_UWB = 10
    REQUEST_ALL = 11
    CONTROL_MOVE = 0
    CONTROL_TURN = 1
    CONTROL_STOP = 2


def btoi(x):
    assert isinstance(x, bytes)
    return int.from_bytes(x, byteorder='big', signed=True)


def itob(x):
    assert isinstance(x, int)
    return x.to_bytes(1, byteorder='big', signed=True)


class Car_srlapp():
    def __init__(self):
        self.srl = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.07)
        self.srl.read(128)
        self.srl.reset_input_buffer()
        self.srl.reset_output_buffer()

    def control(self, mgs_t, speed=0):
        assert isinstance(mgs_t, MgsType)
        head = bytes.fromhex('fffe0000')
        sign = itob(mgs_t.value)
        if mgs_t == MgsType.CONTROL_MOVE:
            control_data = itob(1 if speed > 0 else 2)
            pwm = itob(abs(speed))
            ask = head + sign + control_data + pwm
        elif mgs_t == MgsType.CONTROL_TURN:
            control_data = itob(1 if speed > 0 else 2)
            pwm = itob(abs(speed))
            ask = head + sign + control_data + pwm
        elif mgs_t == MgsType.CONTROL_STOP:
            ask = head + sign
        #print('control send')
        for i in range(1):
            self.srl.write(ask)
            time.sleep(0.004)

    def request(self, mgs_t):
        assert isinstance(mgs_t, MgsType)
        head = bytes.fromhex('fffe0000')
        sign = itob(mgs_t.value)
        ask = head + sign
        # print('send:',ask)
        for i in range(1):
            self.srl.write(ask)
            time.sleep(0.004)

        ans = self.srl.read(128)
        # print('recv:',ans)
        if ans != '':
            reslist = [s for s in ans.split(b'\xff\xfe') if len(s) == 17 or len(s) == 23]
            if len(reslist) == 0:
                return None
            for original_msg in reslist:
                # print(original_msg)
                orderNum = original_msg[:2]
                if mgs_t == MgsType.REQUEST_POSE:
                    roll = original_msg[3:5]
                    yaw = original_msg[5:7]
                    pitch = original_msg[7:9]
                    print(btoi(roll), btoi(yaw), btoi(pitch))
                elif mgs_t == MgsType.REQUEST_ALL:
                    uwb_distance = []
                    for i in range(4):
                        uwb_distance.append(btoi(original_msg[3 + 3 * i:3 + 2 + 3 * i]))
                    left_speed = btoi(original_msg[15:15 + 2])/11
                    right_speed = btoi(original_msg[15 + 2:15 + 4])/11
                    angle_speed = btoi(original_msg[15 + 4:15 + 6])/100
                    pprint(uwb_distance)
                    print(left_speed, right_speed, angle_speed)
                    return uwb_distance, left_speed, right_speed, angle_speed
                elif mgs_t == MgsType.REQUEST_IMU:
                    angle_speed = original_msg[3:5]
                    print(btoi(angle_speed))
                elif mgs_t == MgsType.REQUEST_UltraSonic:
                    US1_distance = original_msg[3:5]
                    US1_angle = original_msg[5:6]
                    US2_distance = original_msg[6:8]
                    US2_angle = original_msg[8:9]
                    US3_distance = original_msg[9:11]
                    US3_angle = original_msg[11:12]
                    print(btoi(US1_distance), US1_angle)
                elif mgs_t == MgsType.REQUEST_IR_4way:
                    IR4_1 = original_msg[3:8]
                    IR4_2 = original_msg[8:5]
                    IR4_3 = original_msg[5:6]
                    IR4_4 = original_msg[6:7]
                elif mgs_t == MgsType.REQUEST_IR_2way:
                    IR2_1 = original_msg[3:5]
                    IR2_2 = original_msg[5:7]
                elif mgs_t == MgsType.REQUEST_SPEED:
                    left_speed = original_msg[3:5]
                    right_speed = original_msg[5:7]

                    print(btoi(left_speed), btoi(right_speed))
                    return btoi(left_speed), btoi(right_speed)
                elif mgs_t == MgsType.REQUEST_UWB:
                    uwb_distance = dict()
                    for i in range(4):
                        uwb_distance[i] = original_msg[3 + 4 * i:5 + 4 * i]
                    print(uwb_distance)
        else:
            return None


if __name__ == '__main__':
    # timer=SimpleTimer(0.01,get_srl_data)
    # timer.start()
    car = Car_srlapp()
    # car_socket=car_client.Car_socket_client()
    i = 1
    a=0
    car.control(MgsType.CONTROL_TURN, speed=30)
    time.sleep(1)
    for i in range(100):
        ans = car.request(MgsType.REQUEST_ALL)
        if ans != None:
            uwb_distance, left_speed, right_speed, angle=ans
            angle=angle/180*np.pi
            print(angle)
            if abs(angle)>0.03:
                angle=angle
            else:
                angle=0        
            a+=angle
            print(a/np.pi*180)
        time.sleep(0.02)
    car.control(MgsType.CONTROL_STOP)
    # while i<20:
        # print(i)
        #car.control(MgsType.CONTROL_MOVE, speed=int(math.sin(i/4)*70))
        # time.sleep(0.1)
        # ans=car.request(MgsType.REQUEST_SPEED)
        # i+=1
    # car.control(MgsType.CONTROL_STOP)
    # while True:
        # time.sleep(0.004)
        # ans=car.request(MgsType.REQUEST_SPEED)
        # if ans!=None:
            # speed_l,speed_r=ans
            # if speed_l!=0:
                # car.control(MgsType.CONTROL_STOP)

            # else:break
    # for i in range(10):
        # ans=car.request(MgsType.REQUEST_SPEED)

    # for i in range(10):
        # ans=car.request(MgsType.REQUEST_UWB)

