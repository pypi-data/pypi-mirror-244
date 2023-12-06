import gymnasium as gym
import numpy as np



class Actions_Filter(gym.ActionWrapper):
    def __init__(self, env):
        super().__init__(env)
        
        self.enabled_allocations = env.unwrapped.jssp.enabled_allocation()  # Get enabled allocations
        
        # Modify the action space to include only enabled allocations   
        self.action_space = gym.spaces.MultiDiscrete([len(self.enabled_allocations),self.jssp.n_jobs])  
        
    def action(self, action):
        # Map the agent's action to the corresponding enabled allocation
        action = self.enabled_allocations[action[0]]
        
        print(self.enabled_allocations)
        print(action)
        
        

        return action  


