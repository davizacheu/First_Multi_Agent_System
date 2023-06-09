from typing import List
import matplotlib

import matplotlib.pyplot as plt
import numpy as np

from Agent import Agent
from Site import Site, Foreign_Site
from World import World

# Simulation parameters
AGENT_VELOCITY = 0.5      # velocity
eta          = 0.6      # random fluctuation in angle (in radians)
L            = 20        # size of world
R            = 0.5      # interaction radius
dt           = 0.1      # time step
Nt           = 200      # number of time steps
N            = 20  # number of agents
MAX_QUALITY  = 250
N_SITES      = 5        # number of sites
S_RADIUS     = 0.15      # site radius

agents : List[Agent] = []
sites  : List[Site]  = []
hub    : Site

def main():
    # Prep figure
    fig = plt.figure(figsize=(L,L), dpi=96)
    ax = plt.gca()
    ax.set(xlim=(-1 , L + 1), ylim=(-1 , L + 1))
    ax.set_aspect('equal')

    # Create an instance of the class World that will store the agents and sites
    # This instance will be accessiable from any part of the program
    world = World()

    # Step 1: Create list of the sites
    # Create hub
    hub = Site(S_RADIUS + np.random.rand()*(L - S_RADIUS), S_RADIUS + np.random.rand()*(L - S_RADIUS))#
    # Adding hub to the animation
    hub_dot = plt.Circle((hub.x_coordinate, hub.y_coordinate), S_RADIUS, color ='green',  alpha=0.5)
    # Adding hub to the World object
    world.hub = hub

    # Foreign Sites will be represented as tuples of the following format
    sites = [Foreign_Site(S_RADIUS + np.random.rand()*(L - S_RADIUS), S_RADIUS + np.random.rand()*(L - S_RADIUS), np.random.rand()*MAX_QUALITY ) for _ in range(N_SITES)]
    
    # Adding other sites to the World instance
    world.sites = sites

    # Step 2: Create list of Agent Objects
    agents = [Agent(hub.x_coordinate, hub.y_coordinate) for _ in range(N)]
    # Adding agents to the World object
    world.agents = agents
    
    # Simulation main loop
    while True:
        # First have each agent perform an action according to their state
        for agent in agents:
            agent.perform_action()
        
        plt.cla()
        	
        ax.add_artist(hub_dot)

        for site in sites:
            site_dot = plt.Circle((site.x_coordinate, site.y_coordinate), S_RADIUS, color ='blue',  alpha=0.5)
            ax.add_artist(site_dot)

        for agent in world.agents:
            plt.scatter(agent.x_coordinate, agent.y_coordinate, color = agent.color)

        ax.set(xlim=(0, L), ylim=(0, L))
        ax.set_aspect('equal')
        plt.pause(0.0001)

if __name__ == '__main__':
    main()