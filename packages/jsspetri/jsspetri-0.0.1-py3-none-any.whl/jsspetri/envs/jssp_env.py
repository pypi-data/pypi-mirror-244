import copy 
import numpy as np
import gymnasium as gym
from gymnasium import spaces

from jsspetri.envs.petricore import Jssp_petri
from jsspetri.render.gui import Gui
from jsspetri.render.solution_plot import plot_solution
from jsspetri.render.create_directory import create_new_directory


class Jssp_Env(gym.Env):
    metadata = {"render_modes": ["human", "solution"]}

    def __init__(self, render_mode=None, instance_id="ta01" ,observation_depth=1):   
        self.jssp=Jssp_petri(instance_id)
    
        self.observation_depth=min(observation_depth,self.jssp.n_machines)
        self.observation_space = spaces.Box(low=-1, high=self.jssp.max_bound, 
                                            shape=(2*self.jssp.n_machines+2*(self.jssp.n_jobs*self.observation_depth)+self.jssp.n_machines,),dtype=np.int64) 

        #+1 is for the idle action
        self.action_space = spaces.Discrete(self.jssp.n_machines*self.jssp.n_jobs+1)  

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        if render_mode == None :
            self.gui=None
        else:
            self.gui=Gui(self.jssp)
            self.gui.render_mode=render_mode
            create_new_directory(self.jssp,self.gui)
            

# Constructing Observations From Environment States
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#observation [machine remaining time if not idle - waiting operation*observation depth -  deliverd operation ]

    def _get_obs(self):
        
        observation = []
        job_places = [p for p in self.jssp.places.values() if p.uid in self.jssp.filter_nodes("job")]
        machine_places = [p for p in self.jssp.places.values() if p.uid in self.jssp.filter_nodes("machine")]
        finished_places = [p for p in self.jssp.places.values() if p.uid in self.jssp.filter_nodes("finished_ops")]
        
        # Get the state of the machines, i.e., remaining time if not idle:
        for machine in machine_places:
            if len ( machine.token_container) == 0:
                observation.extend([machine.color,-1])
            else:
                in_process=machine.token_container[0]
                remaining_time =in_process.process_time - in_process.logging[list(in_process.logging.keys())[-1]][2]
                observation.extend([machine.color, remaining_time if remaining_time  >=0  else -1])
                
        # Get the waiting operation in the jobs depending on the depth:
        for level in range(self.observation_depth):
            for job in job_places:
                if job.token_container and level < len(job.token_container):
                    observation.extend([job.token_container[level].color[1], job.token_container[level].process_time])
                else:
                    observation.extend([-1, -1])
                                 
        # Get the number of deliverd operation 
        for delivery in finished_places:
            observation.append(len ( delivery.token_container))
         
        return np.array(observation, dtype=np.int64)

# %%
# Reset
# ~~~~~  
    def reset(self, seed=None, options=None):
        self.jssp.petri_reset()      
        observation = self._get_obs()
        info = self._get_info(0, False)

        return observation, info
 
# %%
# Reward 
# ~~~~~   
    def reward(self,fired,advantage): 
        return advantage
   

# %%
# Step
# ~~~~~
             
    def action_masks(self):
        enabled_mask=self.jssp.enabled_allocations()  
        return enabled_mask
        
    def step(self, action):
        fired,advantage =self.jssp.env_interact(self.gui,action) 
        reward=self.reward(fired,advantage)
        observation = self._get_obs()
        
        terminated=self.jssp.is_terminal()
        info = self._get_info(reward, terminated) 
        
        return observation, reward, terminated, False, info

# %%
# Rendering
# ~~~~~~~~~

    def render(self):
      
      if self.gui.render_mode== "solution":
          plot_solution(self.jssp,self.gui)

      elif self.gui.render_mode == "human":
          plot_solution(self.jssp,self.gui)
          self.gui.launch_gui()

# %%
# Close
# ~~~~~
    def close(self):   
        if self.metadata["render_modes"] == "human":
            self.gui.on_window_close()
        
# %%
# get information of the environement situation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def _get_info(self,reward, terminated):
        return {
            "Reward":reward ,"Terminated":terminated
        }


        
# %%
if __name__=="__main__":
    
    pass