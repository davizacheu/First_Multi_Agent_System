import State.State_Behaviors as behavior


class Agent:
    def __init__(self, x_coordinate, y_coordinate, constant_velocity) -> None:
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.veloctiy = constant_velocity
        self.state_behavior = behavior.rest
        self.reading = None
        self.max_resting_time = 40

    def determine_state_behavior(self):
        # TODO: THIS IS WHERE WE CONDUCT STATE TRANSITIONS
        pass

    def perform_action(self):
        # reading_of_surroundings = 
        self.state_behavior(self)

    def get_surround_reading(self):
        pass