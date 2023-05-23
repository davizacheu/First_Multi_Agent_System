import matplotlib
matplotlib.use('TkAgg')  # or 'TkAgg' if you prefer an interactive window

import matplotlib.pyplot as plt
import numpy as np

from Agent.Agent import Agent
from Site import Site, Foreign_Site

# Simulation parameters
AGENT_VELOCITY = 0.5      # velocity
eta          = 0.6      # random fluctuation in angle (in radians)
L            = 20        # size of box
R            = 0.5      # interaction radius
dt           = 0.1      # time step
Nt           = 200      # number of time steps
N            = 30      # number of agents
MAX_QUALITY  = 250
N_SITES      = 5        # number of sites
S_RADIUS     = 1        # site radius

def main():
    # Step 1: Create list of the sites
    # Create hub
    hub = Site(S_RADIUS + np.random.rand()*(L - S_RADIUS), S_RADIUS + np.random.rand()*(L - S_RADIUS))
    # Foreign Sites will be represented as tuples of the following format
    sites = [Foreign_Site(S_RADIUS + np.random.rand()*(L - S_RADIUS), S_RADIUS + np.random.rand()*(L - S_RADIUS), np.random.rand()*MAX_QUALITY ) for _ in range(N_SITES)]
    
    # Step 2: Create list of Agent Objects
    agents = [Agent(np.random.rand()*L, np.random.rand()*L, AGENT_VELOCITY) for _ in range(N)]


   
    # Prep figure
    fig = plt.figure(figsize=(L,L), dpi=96)
    ax = plt.gca()
    for site in sites:
        plt.Circle((site.x_coordinate, site.y_coordinate), S_RADIUS, color ='r')

    plt.scatter([agent.x_coordinate for agent in agents],[agent.y_coordinate for agent in agents], color='r')
    pass
    
    

if __name__ == '__main__':
    main()