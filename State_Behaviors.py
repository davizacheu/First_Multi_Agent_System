import numpy as np
from World import World
from Agent import Agent
from Site import Foreign_Site
from typing import List
world = World()

AGENT_VELOCITY = 0.3
REPULSION_FACTOR = 0.01
behavior_time_step = 0.1
oscilation_time_increment = 0.04

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
        if np.random.rand() < number_of_dancers/10:
            agent.state_behavior = travel_to_assess
            agent.elapsed_time_in_state = 0
            agent.color = "#007FFF"

    # If agent does not transition to the assess state it con still transition into the explore state
    if np.random.rand() < agent.behavioral_memory["elapsed_time_in_state"] /20:
        agent.state_behavior = explore
        agent.behavioral_memory["elapsed_time_in_state"] = 0
        agent.color = "#CAE00D" # bitter lemon 

def explore(agent: Agent):
    # Actions:
    # Step 1) If no memory for the agent's velocity exist then initialize stationary velocity memory
    if agent.behavioral_memory.get("velocity_x") == None:
        agent.behavioral_memory["velocity_x"] = 0
    if agent.behavioral_memory.get("velocity_y") == None:
        agent.behavioral_memory["velocity_y"] = 0
    
    agent.x_coordinate %= 20
    agent.y_coordinate %= 20

    # Step 2) After establishing a memory for the agents velocity, now we take into account
    # neighbors around him to calculate a linear velocity
    neighbors : List[Agent]  = list(filter(lambda other_agent: other_agent != agent 
    and (other_agent.x_coordinate - agent.x_coordinate)**2 + (other_agent.y_coordinate - agent.y_coordinate)**2 < 0.5**2, world.agents))

    for other_agent in neighbors:
        if other_agent.behavioral_memory.get("velocity_x") != None:
            agent.behavioral_memory["velocity_x"] -= 1/(other_agent.x_coordinate - agent.x_coordinate)*REPULSION_FACTOR
            agent.behavioral_memory["velocity_y"] -= 1/(other_agent.y_coordinate - agent.y_coordinate)*REPULSION_FACTOR
    
    if agent.behavioral_memory["velocity_x"] != 0:
        linear_angle =\
        np.arctan2(agent.behavioral_memory["velocity_y"],agent.behavioral_memory["velocity_x"])
    else:
        linear_angle = np.random.rand()*2*np.pi
    
    # Step 3) Once the resulting linar angle vector has been found, we then create a new memory
    # to keep track of the oscilation in its motion and produce a final velocity (non-linear) 
    # This final velocity will be in terms of a first-degree monomial and a sine function
    if agent.behavioral_memory.get("oscilating_angle") == None:
        agent.behavioral_memory["oscilating_angle"] = 0
    non_linear_angle = linear_angle + np.sin(agent.behavioral_memory["oscilating_angle"])*0.04
    agent.behavioral_memory["oscilating_angle"] += oscilation_time_increment

    agent.behavioral_memory["velocity_x"] = AGENT_VELOCITY*np.cos(non_linear_angle) 
    agent.behavioral_memory["velocity_y"] = AGENT_VELOCITY*np.sin(non_linear_angle) 
    # Step 4) After establishing the final velocity, we make our agent move according to the determined velocity vector
    agent.x_coordinate += agent.behavioral_memory["velocity_x"]*behavior_time_step  
    agent.y_coordinate += agent.behavioral_memory["velocity_y"]*behavior_time_step 

    # agent.x_coordinate += np.cos(agent.behavioral_memory["oscilating_angle"])*0.05
    # agent.y_coordinate += np.sin(agent.behavioral_memory["oscilating_angle"])*0.05

    agent.behavioral_memory["elapsed_time_in_state"] += 1
    # Inspection after action:
    # Step 1) After we move our agent, we scan for any possible sites within sensing radius 
    # If we find a site we then change to the assess state and head toward that site (in the assess function) 
    foreign_sites : List[Foreign_Site] = sorted(world.sites, key = lambda foreign_site : (foreign_site.x_coordinate - agent.x_coordinate)**2 + \
                                             (foreign_site.y_coordinate - agent.y_coordinate)**2)
    closest_site = foreign_sites[0]

    if (closest_site.x_coordinate - agent.x_coordinate)**2 + \
                                             (closest_site.y_coordinate - agent.y_coordinate)**2 < 1.5**2:
        # If the above condition is met we then transition the agent to travel to assess mode and make the agent 
        # travel to the site 
        agent.state_behavior = travel_to_assess
        del agent.behavioral_memory["oscilating_angle"]
        agent.behavioral_memory["elapsed_time_in_state"] = 0
        agent.color = "#007FFF"
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
