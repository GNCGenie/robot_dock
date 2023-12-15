import time
from Arm_Lib import Arm_Device
import numpy as np

Arm = Arm_Device()

def ArmMove(thetas):
    thetas = 180/np.pi * thetas

    Arm.Arm_serial_servo_write6(thetas[0],thetas[1],thetas[2],thetas[3],thetas[4],0,5000)

def ArmRead():
    Arm = Arm_Device()
    for i in range(6):
        aa = Arm.Arm_serial_servo_read(i+1)
        print(aa,end = " ")
    print()
