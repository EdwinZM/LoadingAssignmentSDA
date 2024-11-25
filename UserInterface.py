from Arm import Arm
from tkinter import *
from tkinter import ttk
from Camera import Camera
from Item import Item
from ConveyorBelt import ConveyorBelt
from Gripper import Gripper
import cv2
from serial.tools import list_ports
import pydobot
from transitions import *

class UserInterface:
    def __init__(self):
        self.chosen_item = None
        self.red_item = None
        self.green_item = None
        self.blue_item = None
        self.pos = None

        self.arm = Arm()
        self.camera = Camera()
        # self.item = Item()
        self.belt = ConveyorBelt()
       # self.gripper = Gripper()

        self.states = ["Initialization", "ERROR", "Detecting Objects", "Reading User Inputs", "Getting Item Position", 
                       "Getting Arm Position", "Getting Conveyor Position", "Moving Arm", "Picking Item", "Dropping Item", "Moving ERROR", "Getting Unloading Position"]

        self.machine = Machine(model= UserInterface, states=self.states, initial="Initialization", on_exception="ERROR")


    def setup_ui(self):
        self.root = Tk()
        self.root.title("Dobot UI")

        self.mainframe = ttk.Frame(self.root, padding='3 3 12 12')
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Buttons
        load_btn = ttk.Button(self.mainframe, text='Load', command=self.Load)
        load_btn.grid(column=1, row=1, sticky=W, padx=20, pady=10)

        unload_btn = ttk.Button(self.mainframe, text='Unload', command=self.Unload)
        unload_btn.grid(column=2, row=1, sticky=E, padx=20, pady=10)

        self.root.mainloop()

        self.machine.add_transition(self.Load, "Initialization", "Detecting Objects")
    
    def Load(self):
        
        try:
            print("loading")
            # Transitions following the state diagram
            
            self.camera.take_image()
            self.camera.process_image()
            self.machine.add_transition("self.camera.take_image", "Detecting Objects", "Reading User Inputs")

            self.pos = self.camera.coordinates

            self.arm.get_position(self.pos)
            self.machine.add_transition("self.arm.get_position", "Reading User Inputs", "Getting Item Position")
            
            self.arm.go_to_position()   
            self.machine.add_transition("self.arm.go_to_position", "Getting Item Position", "Moving Arm")
            

            # red_pos =  self.camera.coordinates[0] # [self.camera.coordinates[0][0] - self.arm.homeX, self.camera.coordinates[0][1] - self.arm.homeY]
            # green_pos = self.camera.coordinates[1] # [self.camera.coordinates[1][0] - self.arm.homeX, self.camera.coordinates[1][1] - self.arm.homeY]
            # blue_pos = self.camera.coordinates[2] # [self.camera.coordinates[2][0] - self.arm.homeX, self.camera.coordinates[2][1] - self.arm.homeY]

            # self.red_item = self.item(color="Red", position=red_pos)
            # self.green_item = self.item(color="Green", position=green_pos)
            # self.blue_item = self.item(color="Blue", position=blue_pos)

            # items = [self.red_item, self.blue_item, self.green_item]

            # self.arm.get_position(self.arm.home())


            # for i in range(3):
            #     # Buttons for choosing items
            #     red_btn = ttk.Button(self.mainframe, text='Red', command=self.choose_red)
            #     red_btn.grid(column=2, row=1, sticky=W, padx=20, pady=10)

            #     green_btn = ttk.Button(self.mainframe, text='Green', command=self.choose_green)
            #     green_btn.grid(column=2, row=2, sticky=EW, padx=20, pady=10)

            #     blue_btn = ttk.Button(self.mainframe, text='Blue', command=self.choose_blue)
            #     blue_btn.grid(column=2, row=3, sticky=E, padx=20, pady=10)


            #     # Following transitions from the diagram
            #     self.machine.add_transition(self.arm.get_position, "Reading User Inputs", "Getting Item Position")
            #     self.arm.get_position(self.chosen_item.position)

            #     self.machine.add_transition(self.arm.go_to_position, "Getting Item Position", "Moving Arm")
            #     self.arm.go_to_position()

            # if self.arm.position == self.pos:
            #     self.arm.device.moveArmXYZ(self.arm.position[0], self.arm.position[1], -10)
            #     self.machine.add_transition(self.arm.device.toggleSuction, "Moving Arm", "Picking Item")
            #     self.arm.device.toggleSuction()
            #     self.arm.device.moveArmXYZ(self.arm.position[0], self.arm.position[1], 0)

            #     self.machine.add_transition(self.belt.get_position, "Picking Item", "Getting Conveyor Position")
            #     self.belt.get_position(self.chosen_item.position[0])
            #     self.arm.get_position(self.belt.position)

            #     self.machine.add_transition(self.arm.go_to_position, "Getting Conveyor Position", "Moving Arm")
            #     self.arm.go_to_position()

                

            #     if self.arm.position == self.belt.position:
            #         self.machine.add_transition(self.gripper.toggle_gripper, "Moving Arm", "Dropping Item")
            #         self.gripper.toggle_gripper(False)

            #     self.machine.add_transition(self.arm.device.rehome, "Dropping Item", "Moving Arm")
            #     self.arm.go_to_position(self.arm.homeX, self.arm.homeY, self.arm.homeZ, True)

            #     self.machine.add_transition(self.dummy_function, "Moving Arm", "Reading User Inputs")
            #     self.dummy_function()

        except NameError as e:
            print(f"Error: {e}")


    def dummy_function(self):
        pass

    def Unload(self):
        # try:
        #     # Transitions following the state diagram
        #     self.machine.add_transition(self.Load, "Initialization", "Detecting Objects")
        #     self.camera.take_image()

        #     self.machine.add_transition(self.camera.process_image, "Detecting Objects", "Reading User Inputs")
        #     self.camera.process_image()

        #     red_pos =  self.camera.coordinates[0] # [self.camera.coordinates[0][0] - self.arm.homeX, self.camera.coordinates[0][1] - self.arm.homeY]
        #     green_pos = self.camera.coordinates[1] # [self.camera.coordinates[1][0] - self.arm.homeX, self.camera.coordinates[1][1] - self.arm.homeY]
        #     blue_pos = self.camera.coordinates[2] # [self.camera.coordinates[2][0] - self.arm.homeX, self.camera.coordinates[2][1] - self.arm.homeY]

        #     self.red_item = self.item(color="Red", position=red_pos)
        #     self.green_item = self.item(color="Green", position=green_pos)
        #     self.blue_item = self.item(color="Blue", position=blue_pos)

        #     items = [self.red_item, self.blue_item, self.green_item]

        #     self.arm.get_position(self.arm.home())


        #     for i in range(3):
        #         # Buttons for choosing items
        #         red_btn = ttk.Button(self.mainframe, text='Red', command=self.choose_red)
        #         red_btn.grid(column=2, row=1, sticky=W, padx=20, pady=10)

        #         green_btn = ttk.Button(self.mainframe, text='Green', command=self.choose_green)
        #         green_btn.grid(column=2, row=2, sticky=EW, padx=20, pady=10)

        #         blue_btn = ttk.Button(self.mainframe, text='Blue', command=self.choose_blue)
        #         blue_btn.grid(column=2, row=3, sticky=E, padx=20, pady=10)


        #         # Following transitions from the diagram
        #         self.machine.add_transition(self.arm.get_position, "Reading User Inputs", "Getting Item Position")
        #         self.arm.get_position(self.chosen_item.position)

        #         self.machine.add_transition(self.arm.go_to_position, "Getting Item Position", "Moving Arm")
        #         self.arm.go_to_position()

        #         if self.arm.position == self.chosen_item.position:
        #             self.arm.device.moveArmXYZ(self.arm.position[0], self.arm.position[1], -10)
        #             self.machine.add_transition(self.gripper.toggle_gripper, "Moving Arm", "Picking Item")
        #             self.gripper.toggle_gripper(True)
        #             self.arm.device.moveArmXYZ(self.arm.position[0], self.arm.position[1], 0)

        #         self.machine.add_transition(self.belt.get_position, "Picking Item", "Getting Unloading Position")

        #         self.arm.get_position(200, 200)

        #         self.machine.add_transition(self.arm.go_to_position, "Getting Unloading Position", "Moving Arm")
        #         self.arm.go_to_position()

                

        #         if self.arm.position == self.belt.position:
        #             self.machine.add_transition(self.gripper.toggle_gripper, "Moving Arm", "Dropping Item")
        #             self.gripper.toggle_gripper(False)

        #         self.machine.add_transition(self.arm.device.rehome, "Dropping Item", "Moving Arm")
        #         self.arm.go_to_position(self.arm.homeX, self.arm.homeY, self.arm.homeZ, True)

        #         self.machine.add_transition(self.dummy_function, "Moving Arm", "Reading User Inputs")
        #         self.dummy_function()

        # except NameError as e:
        #     print(f"Error: {e}")
        print("Unloading")


def main():
    ui = UserInterface()
    ui.setup_ui()

if __name__ == '__main__':
    main()
