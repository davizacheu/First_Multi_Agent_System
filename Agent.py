AGENT_VELOCITY = 0.5      # velocity

class Agent:
    def __init__(self, x_coordinate, y_coordinate) -> None:
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.state_behavior = behavior.rest
        self.color = "#9C2542"
        self.behavioral_memory = {"elapsed_time_in_state" : 0}

    def perform_action(self):
        self.state_behavior(self)

import State_Behaviors as behavior