from transitions import Machine
from serial.tools import list_ports
import DoBotArm as dbt
import threading
import time

class Arm():
    
    def __init__(self):
        self.position = None  
        self.device = dbt.DoBotArm("COM6", 225, 0, -43, home=False)  

    def home(self):
        """Retrieve the current position of the arm"""
        self.position = self.device.getPosition()
        return self.position

    def get_position(self, pos):
        """Set the arm's position"""
        self.position = pos
    
    def go_to_position(self):
        """Move the arm to the current position"""
        if self.position is not None:
            pos = self.position
            self.device.moveArmXYZ(x=pos[0], y=pos[1], z=pos[2])
        else:
            print("Error: Position not set")
