from transitions import Machine
from serial.tools import list_ports
import DoBotArm as dbt
import threading
import time

class Arm():
    
    def __init__(self):
        self.position = None
        # Define home position coordinates
        self.homeX, self.homeY, self.homeZ = 225, 0, -43
        self.device = dbt.DoBotArm("COM10", self.homeX, self.homeY, self.homeZ, home=False)

    def get_position(self, pos):
        self.position = pos
    
    def go_to_position(self, x1, y1, z1):
        """Moves the arm to the specified (x1, y1, z1) coordinates."""
        self.device.moveArmXYZ(x1, y1, z1)
        print(f"Moving arm to position: X={x1}, Y={y1}, Z={z1}")
    
    def start_suction(self):
        """Activates the suction mechanism."""
        self.device.toggleSuction()  # Replace with the actual method to activate suction
        print("Suction activated.")

    def home(self):
        """Moves the arm to the home position and prints the current position."""
        current_pos = self.device.getPosition()
        print(f"Home Position: X={current_pos[0]}, Y={current_pos[1]}, Z={current_pos[2]}")
        self.go_to_position(self.homeX, self.homeY, self.homeZ)  # Move to home

# Example of how to use the Arm class
if __name__ == "__main__":
    arm = Arm()