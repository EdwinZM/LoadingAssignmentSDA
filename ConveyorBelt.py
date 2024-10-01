class ConveyorBelt:
    def __init__(self, hardware_api, initial_position=0, conveyor_width=50):
        self.hardware_api = hardware_api  
        self.velocity = 0  
        self.position = initial_position
        self.conveyor_width = conveyor_width  

    def get_position(self):
        # Call to the hardware API to get the real conveyor position
        self.position = self.hardware_api.get_conveyor_position()
        print(f"Current conveyor position: {self.position}")
        return self.position

    def move_to_position(self, new_position):
        if 0 <= new_position <= self.conveyor_width:
            print(f"Moving conveyor to position {new_position}...")
            # Hardware API call to move the conveyor to the new position
            self.hardware_api.move_conveyor_to_position(new_position)
            self.position = new_position
        else:
            print(f"Error: Position {new_position} out of bounds! Max: {self.conveyor_width}")

    def set_velocity(self, new_velocity):
        if new_velocity >= 0:
            print(f"Setting conveyor velocity to {new_velocity}...")
            # Hardware API call to set the conveyor's velocity
            self.hardware_api.set_conveyor_velocity(new_velocity)
            self.velocity = new_velocity
        else:
            print("Error: Velocity cannot be negative.")
