import State_Behaviors as behavior

class Agent:
    def __init__(self, x_coordinate, y_coordinate, constant_velocity) -> None:
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.veloctiy = constant_velocity
        self.state_behavior = behavior.rest
        self.reading = None
        self.elapsed_time_in_state = 0

    def perform_action(self):
        self.state_behavior(self)

    def get_surround_reading(self):
        pass