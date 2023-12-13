import time
from Arm_Lib import Arm_Device

def ArmMove(thetas):
    # Create a robotic arm object
    Arm = Arm_Device()
    time.sleep(1)

    # home position
    Arm.Arm_serial_servo_write6(0,0,0,0,0,0,1500)

ArmMove([0])
