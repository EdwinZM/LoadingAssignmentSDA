from transitions import Machine
from serial.tools import list_ports
from Camera import Camera
import DoBotArm as dbt
import threading
import time

class Arm():
    
    def __init__(self):
        self.position = None  # Leave it as None, dynamically assigned later
        self.homeX, self.homeY, self.homeZ = 223.89, 4.24, -23
        self.device = dbt.DoBotArm("COM9", self.homeX, self.homeY, self.homeZ, home=False)  # Use defaults
        self.camY = -41.48  #Origin pos X camera
        self.camX = -8.03 # Same shi as above but in Y
        self.ratioX = self.camX / (150)
        self.ratioY = self.camY / (46)

    def home(self):
        """Retrieve the current position of the arm"""
        self.position = self.device.getPosition()
        return self.position

    def get_position(self, pos):
        """Set the arm's position"""
        
        self.position = [self.homeX + abs(pos[0] * self.ratioX * 10), self.homeY + abs(pos[1] * self.ratioY)] 
        print(self.position)
        print(pos)
        print([self.ratioX, self.ratioY])
        print(self.homeX)
        print(self.homeY)
       
    
    def go_to_position(self):
        """Move the arm to the current position"""
        if self.position is not None:  
            pos = self.position
            self.device.moveArmXYZ(x=pos[1], y=pos[0], z=-23)
        else:
            print("Error: Position not set")
        # self.device.moveArmXYZ(x=self.homeX, y=self.homeY, z=self.homeZ)

        

# arm = Arm()
# arm.get_position([arm.homeX, arm.homeY])
# arm.go_to_position()
