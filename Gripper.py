
class Gripper():

    def __init__(self, api, dtype):
        self.api = api
        self.dtype = dtype
        self.gripper_on = False

    def toggle(self):
        if self.gripper_on == True:
            self.gripper_on == False
        else: 
            self.gripper_on == True
        
        self.dType.SetEndEffectorSuctionCup(self.api, self.gripper_on, self.gripper_on, isQueued= 1)

