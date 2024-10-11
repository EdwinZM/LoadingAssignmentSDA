from serial.tools import list_ports
import Arm

class Gripper:
    def __init__(self, arm_instance):
        """Initializing with Arm instance"""
        self.device = arm_instance.device

    def open_gripper(self):
        """Open the gripper"""
        print("Opening the gripper...")
        self.device.toggleSuction(False)  # Assume False is open

    def close_gripper(self):
        """Close the gripper"""
        print("Closing the gripper...")
        self.device.toggleSuction(True)  # Assume True is close
