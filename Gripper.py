import Arm

class Gripper():

    arm = Arm()

    def __init__(self):
        self.port = Gripper.arm.port
        self.device = Gripper.arm.device
        self.gripper_on = False

    def toggle(self):
        if self.gripper_on == True:
            self.gripper_on == False
        else: 
            self.gripper_on == True
        
        self.device.suck(self.gripper_on)
