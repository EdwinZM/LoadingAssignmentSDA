from serial.tools import list_ports
from pydobot import Dobot 

class Gripper:
    def __init__(self, api):
        # Initializing with Dobot API and default status
        self.api = api
        self.grip_status = False  # False means gripper is open
        self.port = list_ports.comports()[0].device
        self.device = Dobot(port=self.port)

    def open_gripper(self):
        # Open the gripper
        print("Opening the gripper...")
        self.device.suck(self.grip_status)
        self.grip_status = False
        # Example of command to open gripper (if you're using Dobot)
        # dtype.SetEndEffectorSuctionCup(self.api, enableCtrl=1, isQueued=1)

    def close_gripper(self):
        # Close the gripper
        print("Closing the gripper...")
        self.device.suck(self.grip_status)
        self.grip_status = True
        # Example of command to close gripper (if you're using Dobot)
        # dtype.SetEndEffectorSuctionCup(self.api, enableCtrl=0, isQueued=1)

    def toggle_gripper(self):
        # Toggle the gripper state
        if self.grip_status:
            self.open_gripper()
        else:
            self.close_gripper()
