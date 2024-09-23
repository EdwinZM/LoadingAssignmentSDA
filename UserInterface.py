from Arm import *
from tkinter import *
from tkinter import ttk
from Camera import *
from Item import *
from ConveyorBelt import *
from Gripper import *
import cv2



def main():

    api = dtype.load()

    dtype.ConnectDobot(api, portName="", baudrate=115200)
    dtype.SetPTPCommonParams(api, 100, 100, isQueued = 1)
    dtype.SetHomeParams(api, 250, 0, 50, 0, isQueued = 1)
    dtype.SetHomeCmd(api, homeCmd = 0, isQueued = 1)

    root = Tk()
    root.title("Dobot UI")

    mainframe = ttk.Frame(root, padding='3 3 12 12')
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    def Load():
        camera.take_image()
        camera.process_image()
        red_pos = camera.coordinates[0]
        green_pos = camera.coordinates[1]
        blue_pos = camera.coordinates[2]

        red_item = Item("Red", red_pos)
        green_item = Item("Green", green_pos)
        blue_item = Item("Blue", blue_pos)

        items = [red_item, blue_item, green_item]

        for i in items:
            arm.get_position(i.position)
            arm.go_to_position()
            gripper.toggle()
            arm.get_position(belt.position)
            arm.go_to_position()
            gripper.toggle()
            arm.go_home()



    def Unload():
        print('unloading')

    loadBtn = ttk.Button(mainframe, text='Load', command=Load).grid(column=1, row=1, sticky=W, padx=20, pady=10)
    unloadBtn = ttk.Button(mainframe, text='Unload', command=Unload).grid(column=2, row=1, sticky=E, padx=20, pady=10)


    arm = Arm(api, dtype)
    camera = Camera()
    item = Item()
    belt = ConveyorBelt()
    gripper = Gripper(api, dtype)



    root.mainloop()


if __name__ == '__main__':
    main()
