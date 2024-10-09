from transitions import Machine
from serial.tools import list_ports
import DoBotArm as dbt
import threading
import time

class Arm():
    
    def __init__(self):
        self.position = None
        #self.port = list_ports.comports()[0].device
        self.homeX, self.homeY, self.homeZ = 177, 121, 0
        self.device = dbt.DoBotArm("COM6", self.homeX, self.homeY, self.homeZ, home= False)
    
    def home(self):
        return self.device.getPosition()

    def get_position(self, pos):
        self.position = pos
    
    def go_to_position(self):
        pos = self.position
        self.device.moveArmXYZ(x=pos[0], y=pos[1], z=pos[2])

arm = Arm()
arm