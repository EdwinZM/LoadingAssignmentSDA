from transitions import Machine
from serial.tools import list_ports
import DoBotArm as dbt
import threading
import time

class Arm():
    
    def __init__(self):
        self.position = None  # Initial position is None
        self.homeX, self.homeY, self.homeZ = 0, 0, 0   # Default home coordinates
        self.device = dbt.DoBotArm("COM12", self.homeX, self.homeY, self.homeZ, home=False)

    def get_position(self, pos):
        """Set the arm's position"""
        self.position = pos

    def get_home(self):
        self.homeX, self.homeY, self.homeZ = self.device.getPosition()[0], self.device.getPosition()[1], self.device.getPosition()[2]

    
    def go_to_position(self):
        """Moves the arm to the specified (x1, y1, z1) coordinates."""
        pos = self.position
        if self.is_within_limits(pos[0], pos[1]):  # Ensure within limits
            self.device.moveArmXYZ(pos[0], pos[1], -20)
            
        else:
            print(f"Error: Position ({pos[0]}, {pos[1]}) out of bounds!")
    
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
        self.get_position([self.homeX, self.homeY, self.homeZ])
        self.go_to_position()
    
    def is_within_limits(self, x, y):
        """Check if within the operational limits"""
        return (0 <= x <= 470) and (-360 <= y <= 363)


arm = Arm()

arm.get_home()
arm.home()
time.sleep(3)
pos = [160, 120]
arm.get_position(pos)
arm.go_to_position()
