from serial.tools import list_ports
import Arm

class Gripper:
    def __init__(self, arm_instance):
        # Use the device from the Arm instance passed in
        self.device = arm_instance.device

    def open_gripper(self):
        # Open the gripper (deactivate suction)
        if self.device is not None:
            print("Opening the gripper...")
            self.device.toggleSuction(False)
        else:
            print("Error: Device not initialized.")

    def close_gripper(self):
        # Close the gripper (activate suction)
        if self.device is not None:
            print("Closing the gripper...")
            self.device.toggleSuction(True)
        else:
            print("Error: Device not initialized.")
