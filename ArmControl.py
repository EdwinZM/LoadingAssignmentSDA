from transitions import Machine
from serial.tools import list_ports
import DoBotArm as dbt
import threading
import time

class Arm():
    
    def __init__(self):
        self.position = None  # Initial position is None
        self.homeX, self.homeY, self.homeZ = 225, 0, -43  # Default home coordinates
        self.device = dbt.DoBotArm("COM10", self.homeX, self.homeY, self.homeZ, home=False)

    def get_position(self, pos):
        """Set the arm's position"""
        self.position = pos
    
    def go_to_position(self, x1, y1, z1):
        """Moves the arm to the specified (x1, y1, z1) coordinates."""
        if self.is_within_limits(x1, y1):  # Ensure within limits
            self.device.moveArmXYZ(x1, y1, z1)
        else:
            print(f"Error: Position ({x1}, {y1}) out of bounds!")
    
    def start_suction(self):
        """Activates the suction mechanism."""
        self.device.toggleSuction(True)
    
    def stop_suction(self):
        """Deactivates the suction mechanism."""
        self.device.toggleSuction(False)

    def home(self):
        """Moves the arm to the home position."""
        self.position = self.device.getPosition()
        print(f"Home Position: {self.position}")
        self.go_to_position(self.homeX, self.homeY, self.homeZ)
    
    def is_within_limits(self, x, y):
        """Check if within the operational limits"""
        return (0 <= x <= 470) and (0 <= y <= 363)
