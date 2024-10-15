from transitions import Machine
from serial.tools import list_ports
import DoBotArm as dbt
import threading
import time

class Arm:
    
    def __init__(self):
        # Set default position to None initially
        self.position = None
        # Initialize the Dobot Arm device
        self.device = dbt.DoBotArm("COM6", 225, 0, -43, home=False)

    def home(self):
        # Ensure device has been initialized before getting position
        if self.device is not None:
            self.position = self.device.getPosition()
        else:
            print("Error: Device not initialized.")
        return self.position

    def get_position(self, pos):
        # Manually set the position if known
        self.position = pos
    
    def go_to_position(self):
        # Move to the last known position, only if it's set
        if self.position is not None:
            pos = self.position
            self.device.moveArmXYZ(x=pos[0], y=pos[1], z=pos[2])
        else:
            print("Error: Position not set.")
