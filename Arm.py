from transitions import Machine
import DobotDllType as dtype

class Arm():


    states = ["Initialization", "ERROR", "Detecting Objects", "Reading User Inputs", "Moving Object", "Getting Item Position", "Getting Arm Position",
              "Getting Conveyour Position", "Moving Arm", "Picking Item", "Dropping Item"]
    
    def __init__(self, api, dtype):
        self.machine = Machine(model=self, states=Arm.states, initial="Initialization")
        self.id = 123
        self.position = None
        self.api = api
        self.dtype = dtype

    def get_position(self, pos):
        self.position = pos
    
    def go_to_position(self):
        pos = self.position
        self.dtype.SetPTPCmd(Arm.api, dtype.PTPMode.PTPMOVLXYZMode, pos[0], pos[1], 0, 0, isQueued = 1)
    
    def go_home(self):
        self.dtype.SetPTPCmd(Arm.api, dtype.PTPMode.PTPMOVLXYZMode, 250, 0 ,50, 0, isQueued = 1)

