import numpy as np
from World import World
from Agent import Agent
from Site import Foreign_Site
from typing import List
from main import N, L, S_RADIUS
world = World()

AGENT_VELOCITY = 0.4
REPULSION_FACTOR = 0.01
behavior_time_step = 0.1
oscilation_time_increment = 0.045
DANCER_DETECT_RADIUS = 0.15
MAX_RESTING_CYCLES = 30000
DANCER_THRESHOLD = N/3
REPULSION_DETECT_RADIUS = 0.5
SITE_SENSING_DISTANCE = 0.7
MAX_EXPLORING_CYCLES = 400000

def rest(agent: Agent):
    agent.behavioral_memory["elapsed_time_in_state"] += 1

    # After performing action the agent verifies for possible state transition
    # Step 1: Get a reading of the agent's dancing 
    dancers : List[Agent] = list(filter(lambda neighbor : neighbor.state_behavior == dance 
                                  and (neighbor.x_coordinate - agent.x_coordinate)**2 
                             + (neighbor.y_coordinate - agent.y_coordinate)**2 < DANCER_DETECT_RADIUS**2, world.agents))
    
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
        if np.random.rand() < number_of_dancers/DANCER_THRESHOLD:
            agent.state_behavior = travel_to_assess
            agent.elapsed_time_in_state = 0
            agent.color = "#007FFF"
            return
    
    # If agent does not transition to the assess state it con still transition into the explore state
    if np.random.rand() < agent.behavioral_memory["elapsed_time_in_state"] /MAX_RESTING_CYCLES:
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
    
    # Step 2) After establishing a memory for the agents velocity, now we take into account
    # neighbors around him to calculate a linear velocity
    neighbors : List[Agent]  = list(filter(lambda other_agent: other_agent != agent 
    and (other_agent.x_coordinate - agent.x_coordinate)**2 + (other_agent.y_coordinate - agent.y_coordinate)**2 < REPULSION_DETECT_RADIUS**2, world.agents))

    for other_agent in neighbors:
        if other_agent.behavioral_memory.get("velocity_x") != None:
            agent.behavioral_memory["velocity_x"] -= 1/(other_agent.x_coordinate - agent.x_coordinate)*REPULSION_FACTOR
            agent.behavioral_memory["velocity_y"] -= 1/(other_agent.y_coordinate - agent.y_coordinate)*REPULSION_FACTOR
    
    if agent.behavioral_memory["velocity_x"] == 0\
        and agent.behavioral_memory["velocity_y"] == 0:
        linear_angle = np.random.rand()*2*np.pi
    else:
        linear_angle =\
            np.arctan2(agent.behavioral_memory["velocity_y"],agent.behavioral_memory["velocity_x"])
    
    # Step 3) Once the resulting linar angle vector has been found, we then create a new memory
    # to keep track of the oscilation in its motion and produce a final velocity (non-linear) 
    # This final velocity will be in terms of a first-degree monomial and a sine function
    if agent.behavioral_memory.get("oscilating_angle") == None:
        agent.behavioral_memory["oscilating_angle"] = 0
    non_linear_angle = linear_angle + np.sin(agent.behavioral_memory["oscilating_angle"])*0.045
    agent.behavioral_memory["oscilating_angle"] += oscilation_time_increment

    agent.behavioral_memory["velocity_x"] = AGENT_VELOCITY*np.cos(non_linear_angle) 
    agent.behavioral_memory["velocity_y"] = AGENT_VELOCITY*np.sin(non_linear_angle) 

    # Step 4) After establishing the final velocity, we make our agent move according to the determined velocity vector
    agent.x_coordinate += agent.behavioral_memory["velocity_x"]*behavior_time_step  
    agent.y_coordinate += agent.behavioral_memory["velocity_y"]*behavior_time_step 
    agent.x_coordinate %= L
    agent.y_coordinate %= L

    agent.behavioral_memory["elapsed_time_in_state"] += 1

    # Inspection after action:
    # Step 1) After we move our agent, we scan for any possible sites within sensing radius 
    # If we find a site we then change to the assess state and head toward that site (in the assess function) 
    foreign_sites : List[Foreign_Site] = sorted(world.sites, key = lambda foreign_site : (foreign_site.x_coordinate - agent.x_coordinate)**2 + \
                                             (foreign_site.y_coordinate - agent.y_coordinate)**2)
    closest_site = foreign_sites[0]

    if (closest_site.x_coordinate - agent.x_coordinate)**2 + \
                                             (closest_site.y_coordinate - agent.y_coordinate)**2 < SITE_SENSING_DISTANCE**2:
        # If the above condition is met we then transition the agent to travel to assess mode and make the agent 
        # travel to the site 
        agent.state_behavior = travel_to_assess
        del agent.behavioral_memory["oscilating_angle"]
        agent.behavioral_memory["elapsed_time_in_state"] = 0
        agent.behavioral_memory["target_location"] = (closest_site.x_coordinate, closest_site.y_coordinate)
        agent.color = "#007FFF"
        return
    
    # If no site is around then, the agent still may transition back to resting behavior 
    if np.random.rand() < agent.behavioral_memory["elapsed_time_in_state"] /MAX_EXPLORING_CYCLES:
        agent.state_behavior = travel_to_hub
        del agent.behavioral_memory["oscilating_angle"]
        agent.behavioral_memory["elapsed_time_in_state"] = 0
        agent.behavioral_memory["target_location"] = (world.hub.x_coordinate, world.hub.y_coordinate)
        agent.color = "#FF82AB"

def assess(agent: Agent):
    # TODO: IMPLEMENT THIS FUNCTION
    pass

def dance(agent: Agent):
    # TODO: IMPLEMENT THIS FUNCTION
    pass

def travel_to_location(agent: Agent):
    # Action: head straight to the site

    #If the directed velocities have not yet been set up, then set then up
    if "target_angle" not in agent.behavioral_memory:
        # Create new target_angle memory and use to calculate the correct vectors
        agent.behavioral_memory["target_angle"] =\
            np.arctan2((agent.behavioral_memory["target_location"][1] - agent.y_coordinate),\
                       (agent.behavioral_memory["target_location"][0] - agent.x_coordinate))
        agent.behavioral_memory["velocity_x"] = AGENT_VELOCITY*np.cos(agent.behavioral_memory["target_angle"])
        agent.behavioral_memory["velocity_y"] = AGENT_VELOCITY*np.sin(agent.behavioral_memory["target_angle"])

        # After calculating the velocity vectors we then move our agent
        agent.x_coordinate += agent.behavioral_memory["velocity_x"]*behavior_time_step  
        agent.y_coordinate += agent.behavioral_memory["velocity_y"]*behavior_time_step 
        agent.x_coordinate %= L
        agent.y_coordinate %= L
    else:
        # If the agent already has set up the velocity vectors, simply move it
        agent.x_coordinate += agent.behavioral_memory["velocity_x"]*behavior_time_step  
        agent.y_coordinate += agent.behavioral_memory["velocity_y"]*behavior_time_step 
        agent.x_coordinate %= L
        agent.y_coordinate %= L
    
    # After our action, verify if the agent has reached the target location
    if (agent.behavioral_memory["target_location"][0] - agent.x_coordinate)**2\
        + (agent.behavioral_memory["target_location"][1] - agent.y_coordinate)**2 < (S_RADIUS/4)**2:
        del agent.behavioral_memory["velocity_x"]
        del agent.behavioral_memory["velocity_y"]
        del agent.behavioral_memory["target_angle"]
        del agent.behavioral_memory["target_location"]
        agent.behavioral_memory["elapsed_time_in_state"] = 0
        return True
    else:
        return False
            

def travel_to_assess(agent : Agent):
    arrived = travel_to_location(agent)
    if arrived:
        agent.state_behavior = assess
        agent.color = "#3A5FCD"

def travel_to_hub(agent: Agent):
    arrived = travel_to_location(agent)
    if arrived:
        agent.state_behavior = rest
        agent.color = "#9C2542"
