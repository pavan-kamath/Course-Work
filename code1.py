import argparse
from math import sin, cos, pi
from pylx16a.lx16a import *
import time
import numpy as np
import itertools




def valid_angle(angle):
    return 0.96 * round(angle/0.96)

def get_path(start,end):
    return np.array([round(valid_angle(x), 2) for x in np.linspace(start, end, int(abs(end-start)/0.96))])

def init_legs():
    global left_knee,left_hip,left_foot,left_thigh,right_hip,right_thigh,right_knee,right_foot,motors
    global left_knee_home,left_hip_home,left_foot_home,left_thigh_home,right_hip_home,right_thigh_home,right_knee_home,right_foot_home
    left_hip = LX16A(1)
    left_thigh = LX16A(2)
    left_knee = LX16A(3)
    left_foot = LX16A(4)
    right_hip = LX16A(5)
    right_thigh = LX16A(6)
    right_knee = LX16A(7)
    right_foot = LX16A(8)
    left_hip_home = 120
    left_thigh_home = 120
    left_knee_home = 120
    left_foot_home = 120
    right_hip_home = 120
    right_thigh_home = 120
    right_knee_home = 120
    right_foot_home = 120
    left_hip_offset = 0
    left_thigh_offset = -10
    left_knee_offset = 0
    left_foot_offset = -5
    right_hip_offset = 0
    right_thigh_offset = 10
    right_knee_offset = 8
    right_foot_offset = 4
    #left_hip.set_angle_limits(0,240)
    #left_thigh.set_angle_limits(0,240)
    #left_knee.set_angle_limits(0,240)
    #left_foot.set_angle_limits(0,240)
    #right_hip.set_angle_limits(0,240)
    #right_thigh.set_angle_limits(0,240)
    #right_knee.set_angle_limits(0,240)
    #right_foot.set_angle_limits(0,240)
    left_hip.set_angle_offset(left_hip_offset)
    left_thigh.set_angle_offset(left_thigh_offset)
    left_knee.set_angle_offset(left_knee_offset)
    left_foot.set_angle_offset(left_foot_offset)
    right_hip.set_angle_offset(right_hip_offset)
    right_thigh.set_angle_offset(right_thigh_offset)
    right_knee.set_angle_offset(right_knee_offset)
    right_foot.set_angle_offset(right_foot_offset)
    motors = [left_knee,left_hip,left_foot,left_thigh,right_hip,right_thigh,right_knee,right_foot]
    #actual limits
#     left_hip.set_angle_limits(90, 140)
#     left_thigh.set_angle_limits(50, 120)
#     left_knee.set_angle_limits(160, 240)
#     left_foot.set_angle_limits(80, 130)
#     right_hip.set_angle_limits(90, 140)
#     right_thigh.set_angle_limits(110, 180)
#     right_knee.set_angle_limits(48, 120)
#     right_foot.set_angle_limits(100, 150)


def to_home_position():
    left_hip_path = get_path(left_hip.get_physical_angle(),left_hip_home)
    left_thigh_path = get_path(left_thigh.get_physical_angle(),left_thigh_home)
    left_knee_path = get_path(left_knee.get_physical_angle(),left_knee_home)
    left_foot_path = get_path(left_foot.get_physical_angle(),left_foot_home)
    right_hip_path = get_path(right_hip.get_physical_angle(),right_hip_home)
    right_thigh_path = get_path(right_thigh.get_physical_angle(),right_thigh_home)
    right_knee_path = get_path(right_knee.get_physical_angle(),right_knee_home)
    right_foot_path = get_path(right_foot.get_physical_angle(),right_foot_home)
    for left_hip_step,left_thigh_step, left_knee_step,left_foot_step,right_hip_step,right_thigh_step,right_knee_step,right_foot_step in list(itertools.zip_longest(left_hip_path,left_thigh_path, left_knee_path,left_foot_path,right_hip_path,right_thigh_path,right_knee_path,right_foot_path, fillvalue=120)):
        left_hip.move(left_hip_step)
        left_thigh.move(left_thigh_step)
        left_knee.move(left_knee_step)
        left_foot.move(left_foot_step)
        right_hip.move(right_hip_step)
        right_thigh.move(right_thigh_step)
        right_knee.move(right_knee_step)
        right_foot.move(right_foot_step)
        time.sleep(0.1)

def to_active_position():
    to_home_position()
    for i in range(100):
        left_thigh.move(left_thigh.get_commanded_angle()-servo_move_unit)
        left_knee.move(left_knee.get_commanded_angle()+servo_move_unit)
        right_thigh.move(right_thigh.get_commanded_angle()+servo_move_unit)
        right_knee.move(right_knee.get_commanded_angle()-servo_move_unit)
        time.sleep(0.01)
        
def boot_exercise():
    to_home_position()
    time.sleep(2)
    for i in range(50):
        left_hip.move(left_hip.get_commanded_angle()+servo_move_unit)
        left_thigh.move(left_thigh.get_commanded_angle()-servo_move_unit)
        left_knee.move(left_knee.get_commanded_angle()+servo_move_unit)
        left_foot.move(left_foot.get_commanded_angle()-servo_move_unit)
        right_hip.move(right_hip.get_commanded_angle()-servo_move_unit)
        right_thigh.move(right_thigh.get_commanded_angle()+servo_move_unit)
        right_knee.move(right_knee.get_commanded_angle()-servo_move_unit)
        right_foot.move(right_foot.get_commanded_angle()-servo_move_unit)
        time.sleep(0.001)
    time.sleep(2)
    for i in range(50):
        left_hip.move(left_hip.get_commanded_angle()-servo_move_unit)
        left_thigh.move(left_thigh.get_commanded_angle()+servo_move_unit)
        left_knee.move(left_knee.get_commanded_angle()-servo_move_unit)
        left_foot.move(left_foot.get_commanded_angle()+servo_move_unit)
        right_hip.move(right_hip.get_commanded_angle()+servo_move_unit)
        right_thigh.move(right_thigh.get_commanded_angle()-servo_move_unit)
        right_knee.move(right_knee.get_commanded_angle()+servo_move_unit)
        right_foot.move(right_foot.get_commanded_angle()+servo_move_unit)
        time.sleep(0.001)
    for i in range(50):
        left_hip.move(left_hip.get_commanded_angle()-servo_move_unit)
        left_thigh.move(left_thigh.get_commanded_angle()-servo_move_unit)
        left_knee.move(left_knee.get_commanded_angle()+servo_move_unit)
        left_foot.move(left_foot.get_commanded_angle()-servo_move_unit)
        right_hip.move(right_hip.get_commanded_angle()+servo_move_unit)
        right_thigh.move(right_thigh.get_commanded_angle()+servo_move_unit)
        right_knee.move(right_knee.get_commanded_angle()-servo_move_unit)
        right_foot.move(right_foot.get_commanded_angle()-servo_move_unit)
        time.sleep(0.001)
    time.sleep(2)
    for i in range(50):
        left_hip.move(left_hip.get_commanded_angle()+servo_move_unit)
        left_thigh.move(left_thigh.get_commanded_angle()+servo_move_unit)
        left_knee.move(left_knee.get_commanded_angle()-servo_move_unit)
        left_foot.move(left_foot.get_commanded_angle()+servo_move_unit)
        right_hip.move(right_hip.get_commanded_angle()-servo_move_unit)
        right_thigh.move(right_thigh.get_commanded_angle()-servo_move_unit)
        right_knee.move(right_knee.get_commanded_angle()+servo_move_unit)
        right_foot.move(right_foot.get_commanded_angle()+servo_move_unit)
        time.sleep(0.001)
    #to_home_position()         

def bounce(bounces):
    time.sleep(2)
    for i in range(bounces):
        to_home_position()
        for i in range(100):
            left_thigh.move(left_thigh.get_commanded_angle()-servo_move_unit)
            left_knee.move(left_knee.get_commanded_angle()+servo_move_unit)
            right_thigh.move(right_thigh.get_commanded_angle()+servo_move_unit)
            right_knee.move(right_knee.get_commanded_angle()-servo_move_unit)
            time.sleep(0.001)
        for i in range(100):
            left_thigh.move(left_thigh.get_commanded_angle()+servo_move_unit)
            left_knee.move(left_knee.get_commanded_angle()-servo_move_unit)
            right_thigh.move(right_thigh.get_commanded_angle()-servo_move_unit)
            right_knee.move(right_knee.get_commanded_angle()+servo_move_unit)
            time.sleep(0.001)
        to_home_position()

def walk(steps):
    to_active_position()
    for i in range(20):
        left_thigh.move(left_thigh.get_commanded_angle()+4*servo_move_unit)
        left_knee.move(left_knee.get_commanded_angle()+4*servo_move_unit)
        right_knee.move(right_knee.get_commanded_angle()+0.25*4*servo_move_unit)
        time.sleep(0.01)
    for i in range(40):
        right_thigh.move(right_thigh.get_commanded_angle()-0.75*4*servo_move_unit)
        right_knee.move(right_knee.get_commanded_angle()-0.75*4*servo_move_unit)
        left_knee.move(left_knee.get_commanded_angle()-0.25*4*servo_move_unit)
        time.sleep(0.01)
    for step in range(steps):
        for i in range(40):#left leg step
            right_thigh.move(right_thigh.get_commanded_angle()+4*servo_move_unit)
            left_thigh.move(left_thigh.get_commanded_angle()-0.5*4*servo_move_unit)
            left_knee.move(left_knee.get_commanded_angle()+0.5*4*servo_move_unit)
            right_knee.move(right_knee.get_commanded_angle()+0.25*4*servo_move_unit)
            time.sleep(0.000001)
        for i in range(40):#right leg step
            right_thigh.move(right_thigh.get_commanded_angle()-4*servo_move_unit)
            left_thigh.move(left_thigh.get_commanded_angle()+0.5*4*servo_move_unit)
            right_knee.move(right_knee.get_commanded_angle()-0.25*4*servo_move_unit)
            left_knee.move(left_knee.get_commanded_angle()-0.5*4*servo_move_unit)
            time.sleep(0.000001)
    to_home_position()
    
def fast_walk(steps):
    to_active_position()
    for step in range(steps):
        for i in range(40):#left leg step
            right_thigh.move(right_thigh.get_commanded_angle()+4*servo_move_unit)
            left_thigh.move(left_thigh.get_commanded_angle()-0.5*4*servo_move_unit)
            left_knee.move(left_knee.get_commanded_angle()+0.5*4*servo_move_unit)
            right_knee.move(right_knee.get_commanded_angle()+0.25*4*servo_move_unit)
            time.sleep(0.0001)
        for i in range(40):#right leg step
            right_thigh.move(right_thigh.get_commanded_angle()-4*servo_move_unit)
            left_thigh.move(left_thigh.get_commanded_angle()+0.5*4*servo_move_unit)
            right_knee.move(right_knee.get_commanded_angle()-0.25*4*servo_move_unit)
            left_knee.move(left_knee.get_commanded_angle()-0.5*4*servo_move_unit)
            time.sleep(0.0001)
        for i in range(40):#right leg step
            right_thigh.move(right_thigh.get_commanded_angle()+4*servo_move_unit)
            left_thigh.move(left_thigh.get_commanded_angle()-0.5*4*servo_move_unit)
            right_knee.move(right_knee.get_commanded_angle()+0.25*4*servo_move_unit)
            left_knee.move(left_knee.get_commanded_angle()+0.5*4*servo_move_unit)
            time.sleep(0.0001)
        for i in range(40):#left leg step
            right_thigh.move(right_thigh.get_commanded_angle()-4*servo_move_unit)
            left_thigh.move(left_thigh.get_commanded_angle()+0.5*4*servo_move_unit)
            left_knee.move(left_knee.get_commanded_angle()-0.5*4*servo_move_unit)
            right_knee.move(right_knee.get_commanded_angle()-0.25*4*servo_move_unit)
            time.sleep(0.0001)
        
            #time.sleep(0.001)
    to_home_position()
    
def dance(steps):
    to_active_position()
    for i in range(20):
        left_thigh.move(left_thigh.get_commanded_angle()+4*servo_move_unit)
        left_knee.move(left_knee.get_commanded_angle()+4*servo_move_unit)
        right_knee.move(right_knee.get_commanded_angle()+0.25*4*servo_move_unit)
        time.sleep(0.01)
    for i in range(40):
        right_thigh.move(right_thigh.get_commanded_angle()-0.75*4*servo_move_unit)
        right_knee.move(right_knee.get_commanded_angle()-0.75*4*servo_move_unit)
        left_knee.move(left_knee.get_commanded_angle()-0.25*4*servo_move_unit)
        time.sleep(0.01)
    for step in range(steps):
        for i in range(40): #left leg step
            right_thigh.move(right_thigh.get_commanded_angle()+0.5*4*servo_move_unit)
            left_thigh.move(left_thigh.get_commanded_angle()-0.25*4*servo_move_unit)
            left_knee.move(left_knee.get_commanded_angle()+0.5*4*servo_move_unit)
            right_knee.move(right_knee.get_commanded_angle()+0.25*4*servo_move_unit)
            time.sleep(0.005)
        for i in range(40): #right leg step
            right_thigh.move(right_thigh.get_commanded_angle()-0.5*4*servo_move_unit)
            left_thigh.move(left_thigh.get_commanded_angle()+0.25*4*servo_move_unit)
            right_knee.move(right_knee.get_commanded_angle()-0.25*4*servo_move_unit)
            left_knee.move(left_knee.get_commanded_angle()-0.5*4*servo_move_unit)
            time.sleep(0.005)

def blink_led(motor):
    motor.led_power_off()
    time.sleep(0.1)
    motor.led_power_on()
    time.sleep(0.1)
    motor.led_power_off()
    time.sleep(0.1)
    motor.led_power_on()
    
def is_within_temp_limits():
    for m in motors:
        if m.get_temp() > 80:
            raise UserWarning("{} is overheating",m)
        else:
            blink_led(m)
            
def is_within_voltage_limits():
    for m in motors:
        if m.get_vin() > 12500:
            raise UserWarning("{} voltage too high",m)
        elif m.get_vin() < 4000:
            raise UserWarning("{} voltage too low",m)
        else:
            blink_led(m)
            
def health_check():
    try:
        is_within_temp_limits()
    except UserWarning as e:
        print(e)
        quit()
    try:
        is_within_voltage_limits()
    except UserWarning as e:
        print(e)
        quit()

def shutdown():
    to_home_position()


if __name__ == "__main__":
    LX16A.initialize("COM5")
    servo_move_unit = 0.24
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", type=str)
    parser.add_argument("--boot_exer", type=bool, default=False)
    parser.add_argument("--steps", type=int, default=5)
    args = parser.parse_args()
    try:
        init_legs()
        #walk(5)
    except ServoTimeoutError as e:
        print(f"Servo {e.id_} is not responding. Exiting...")
    '''try:
        to_active_position()
    except ServoTimeoutError as e:
        print(f"Servo {e.id_} is not responding. Exiting...")
    if args.boot_exer:
        try:
            boot_exercise()
            #health_check()
        except ServoTimeoutError as e:
            print(f"Servo {e.id_} is not responding. Exiting...")'''
    if args.action == "walk":
        #health_check()
        walk(args.steps)
    elif args.action == "fast_walk":
        #health_check()
        fast_walk(args.steps)
    elif args.action == "bounce":
        #health_check()
        bounce(args.steps)
    elif args.action == "dance":
        #health_check()
        dance(args.steps)
    shutdown()
    print("Thank You!! -Shay Bot")
    
    
    