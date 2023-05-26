import numpy as np
from World import World
from Agent import Agent
from typing import List
world = World()

behavior_time_step = 1.0
oscilation_time_increment = 0.1

def rest(agent: Agent):
    # Action: nothing
    agent.behavioral_memory["elapsed_time_in_state"] += 1

    # After performing action the agent verifies for possible state transition
    # Step 1: Get a reading of the agent's dancing 
    dancers : List[Agent] = list(filter(lambda neighbor : neighbor.state_behavior == dance 
                                  and (neighbor.x_coordinate - agent.x_coordinate)**2 
                             + (neighbor.y_coordinate - agent.y_coordinate)**2 < 1.25**2, world.agents))
    
    # Add each site promoted by a dancer to a list of possible assessments
    possible_sites_for_assessment = {}
    for dancer in dancers:
        if (number_dancers := possible_sites_for_assessment.get(dancer.behavioral_memory["site_for_dancing"])) is not None:
            number_dancers += 1
        else:
            possible_sites_for_assessment[dancer.behavioral_memory["site_for_dancing"]] = 1
    
    # Go through each site with different probabilities of assessing different sites
    for (site, number_of_dancers) in possible_sites_for_assessment:
        # The more agents dancing for a site the more likely it is for the resting agent decide to assess that site
        if np.rand.random() < number_of_dancers/10:
            agent.state_behavior = travel_to_assess
            agent.elapsed_time_in_state = 0
            agent.color = "#007FFF"

    # If agent does not transition to the assess state it con still transition into the explore state
    if np.rand.random() < agent.behavioral_memory["elapsed_time_in_state"] /20:
        agent.state_behavior = explore
        agent.behavioral_memory["elapsed_time_in_state"] = 0
        agent.color = "#CAE00D"

def explore(agent: Agent):
    # Actions:
    # Step 1) If no memory for the agent's velocity exist then initialize stationary velocity memory

    # Step 2) After establishing a memory for the agents velocity, now we take into account
    # neighbors around him to calculate a linear velocity

    # Step 3) Once the resulting linar velocity vector has been found, we then create a new memory
    # to keep track of the oscilation in its motion and produce a final velocity (non-linear) 
    # This final velocity will be in terms of a first-degree monomial and a sine function

    # Step 4) After establishing the final velocity, we make our agent move according to the determined velocity vector
    
    # Inspection after action:
    # Step 1) After we move our agent, we scan for any possible sites within sensing radius 
    # If we find a site we then change to the assess state and head toward that site (in the assess function) 

    
    pass

def assess(agent: Agent):
    # TODO: IMPLEMENT THIS FUNCTION
    print('Agent is assessing')
    pass

def dance(agent: Agent):
    # TODO: IMPLEMENT THIS FUNCTION
    print('Agent is dancing')
    pass

def travel_to_assess(agent: Agent):
    # Action the agent enters a state where 
    pass
