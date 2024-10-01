from Arm import *
from tkinter import *
from tkinter import ttk
from Camera import *
from Item import *
from ConveyorBelt import *
from Gripper import *
import cv2
from serial.tools import list_ports
import pydobot



def main():

    arm = Arm()
    camera = Camera()
    item = Item()
    belt = ConveyorBelt()
    gripper = Gripper()


    states = ["Initialization", "ERROR", "Detecting Objects", "Reading User Inputs", "Moving Object", "Getting Item Position", "Getting Arm Position",
                "Getting Conveyour Position", "Moving Arm", "Picking Item", "Dropping Item"]
    machine = Machine(model=main, states=Arm.states, initial="Initialization", on_exception="Error")

    root = Tk()
    root.title("Dobot UI")

    mainframe = ttk.Frame(root, padding='3 3 12 12')
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    machine.add_transition(main, "Initialization", "Detecting Objects")

    def Load():
        try: 
            machine.add_transition(Load, "Detecting Objects", "Reading User Inputs")
            camera.take_image()
            camera.process_image()
            red_pos = camera.coordinates[0]
            green_pos = camera.coordinates[1]
            blue_pos = camera.coordinates[2]

            red_item = item("Red", red_pos)
            green_item = item("Green", green_pos)
            blue_item = item("Blue", blue_pos)

            items = [red_item, blue_item, green_item]

            def dummy_function():
                pass

            chosen_item: None

            def choose_red():
                nonlocal chosen_item
                chosen_item = red_item

            def choose_green():
                nonlocal chosen_item
                chosen_item = green_item
            
            def choose_blue():
                nonlocal chosen_item
                chosen_item = blue_item

            
           
            for i in range(3):
                match i:
                    case 0:
                        RedBtn = ttk.Button(mainframe, text='Red', command=choose_red).grid(column=2, row=1, sticky=W, padx=20, pady=10)
                        GreenBtn = ttk.Button(mainframe, text='Green', command=choose_green).grid(column=2, row=2, sticky=EW, padx=20, pady=10)
                        BlueBtn = ttk.Button(mainframe, text='Blue', command=choose_blue).grid(column=2, row=3, sticky=E, padx=20, pady=10)
                        
                    case 1:
                        GreenBtn = ttk.Button(mainframe, text='Green', command=choose_green).grid(column=2, row=1, sticky=W, padx=20, pady=10)
                        BlueBtn = ttk.Button(mainframe, text='Blue', command=choose_blue).grid(column=2, row=3, sticky=E, padx=20, pady=10)
                    case 2:
                        BlueBtn = ttk.Button(mainframe, text='Blue', command=choose_blue).grid(column=2, row=2, sticky=EW, padx=20, pady=10)

                machine.add_transition(arm.get_position, "Reading User Inputs", "Getting Item Position")
                arm.get_position(chosen_item.position)
                machine.add_transition(arm.go_to_position, "Getting Item Position", "Moving Arm")
                arm.go_to_position()
                
                machine.add_transition(gripper.toggle, "Moving Arm", "Picking Item")
                gripper.toggle_gripper()
                machine.add_transition(arm.get_position, "Picking Item", "Getting Conveyour Position")
                arm.get_position(belt.position)
                machine.add_transition(arm.go_to_position, "Getting Conveyour Position", "Moving Object")
                arm.go_to_position()
                machine.add_transition(gripper.toggle, "Moving Object", "Dropping Item")
                gripper.toggle_gripper()
                machine.add_transition(arm.go_home, "Dropping Item", "Moving Arm")
                arm.go_home()
                machine.add_transition(dummy_function, "Moving Arm", "Reading User Inputs")
                dummy_function()
                
        except NameError:
            print(NameError)



    def Unload():
        print('unloading')

    loadBtn = ttk.Button(mainframe, text='Load', command=Load).grid(column=1, row=1, sticky=W, padx=20, pady=10)
    unloadBtn = ttk.Button(mainframe, text='Unload', command=Unload).grid(column=2, row=1, sticky=E, padx=20, pady=10)






    root.mainloop()


if __name__ == '__main__':
    main()
