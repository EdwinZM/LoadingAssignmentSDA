from transitions import Machine
from serial.tools import list_ports
from pydobot import Dobot

class Arm():
    
    def __init__(self):
        self.position = None
        self.port = list_ports.comports()[0].device
        self.device = Dobot(port=self.port)
        self.home = self.device._get_pose()
       

    def get_position(self, pos):
        self.position = pos
    
    def go_to_position(self):
        pos = self.position
        self.device.move_to(pos[0], pos[1], None, None, wait=True)
    
    def go_home(self):
        self.device.move_to(self.home.x, self.home.y, self.home.z, self.home.r, wait=True)
