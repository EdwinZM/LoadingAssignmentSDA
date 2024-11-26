from transitions import Machine
from serial.tools import list_ports
from Camera import Camera
import DoBotArm as dbt
import threading
import time

class Arm():
    
    def __init__(self):
        self.position = None  # Leave it as None, dynamically assigned later
        self.homeX, self.homeY, self.homeZ = 40, 297, 0
        self.device = dbt.DoBotArm("COM5", self.homeX, self.homeY, self.homeZ, home=False)  # Use defaults
        self.camY = 143  #Origin pos X camera
        self.camX = 158 # Same shi as above but in Y
        self.ratioX = self.camX / (150)
        self.ratioY = self.camY / (46)
        self.centerCam = [58.92, 36.55] #CHECK THE COORDINATE REFERENCES BASED ON DOBOT
        self.centerDob = [202.99, 4.78] #MEASURE EVERY TIME DOBOT IS TURNED ON 
        self.centerRatio = [self.centerCam[0]/ self.centerDob[0], self.centerCam[1] / self.centerDob[1]]

    def home(self):
        """Retrieve the current position of the arm"""
        self.position = [self.homeX, self.homeY, self.homeZ]
        return self.position

    def get_position(self, pos):
        """Set the arm's position"""
        
        # self.position = [self.homeX + (pos[1] * self.ratioX) , self.homeY + (pos[0] * self.ratioY)] 
        #self.position = [self.homeX + (pos[1] * self.centerRatio[0]), self.homeY (pos[0] * self.centerRatio[1])]
        self.position = [self.homeX - pos[0], self.homeY -  pos[0] ]
        print("X:", pos[0], ", Y:", pos[1])
        print("Final pos passed to dobot:", self.position)
       
    
    def go_to_position(self):
        """Move the arm to the current position"""
        if self.position is not None:  
            pos = self.position
            self.device.moveArmXYZ(x=pos[0], y=self.homeY, z=self.homeZ)
            self.device.moveArmXYZ(x=pos[0], y=pos[1], z=self.homeZ)
            self.device.moveArmXYZ(x=pos[0], y=pos[1], z=-23)
        else:
            print("Error: Position not set")
        # self.device.moveArmXYZ(x=self.homeX, y=self.homeY, z=self.homeZ)

        

# arm = Arm()
# arm.get_position([arm.homeX, arm.homeY])
# arm.go_to_position()
