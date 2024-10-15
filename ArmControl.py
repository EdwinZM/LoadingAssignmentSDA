from transitions import Machine
from serial.tools import list_ports
import DoBotArm as dbt
import threading
import time


class Arm:
    
    def __init__(self):
        # Initialize position as None
        self.position = None
        # Define home position coordinates
        self.homeX, self.homeY, self.homeZ = 225, 0, -43
        # Initialize the Dobot Arm device
        self.device = dbt.DoBotArm("COM10", self.homeX, self.homeY, self.homeZ, home=False)

    def get_position(self, pos):
        # Manually set the position
        self.position = pos
    
    def go_to_position(self, x1, y1, z1):
        # Moves the arm to the specified (x1, y1, z1) coordinates
        if self.device is not None:
            if self.is_within_limits(x1, y1):
                self.device.moveArmXYZ(x1, y1, z1)
            else:
                print(f"Error: Position ({x1}, {y1}) is out of bounds!")
        else:
            print("Error: Device not initialized.")

    def start_suction(self):
        # Activate the suction mechanism
        if self.device is not None:
            self.device.toggleSuction(True)
        else:
            print("Error: Device not initialized.")

    def stop_suction(self):
        # Deactivate the suction mechanism
        if self.device is not None:
            self.device.toggleSuction(False)
        else:
            print("Error: Device not initialized.")

    def home(self):
        # Move to the home position
        if self.device is not None:
            self.position = self.device.getPosition()
            print(f"Home Position: {self.position}")
            self.go_to_position(self.homeX, self.homeY, self.homeZ)
        else:
            print("Error: Device not initialized.")

    def is_within_limits(self, x, y):
        # Check if the coordinates are within the operational limits
        return (0 <= x <= 470) and (0 <= y <= 363)
    
    def is_within_limits(self, x, y):
        """Check if within the operational limits"""
        return (0 <= x <= 470) and (0 <= y <= 363)
