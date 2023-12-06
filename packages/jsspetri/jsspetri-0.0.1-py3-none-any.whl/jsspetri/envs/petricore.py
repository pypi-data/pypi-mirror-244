import os
import copy
import numpy as np
import pandas as pd

from jsspetri.render.create_png import create_png

#%% JSSP buiding block definiton 

class Jssp_petri:
    
    uid = 0  # Class-level variable to track the current ID
       
    def __init__(self, instanceID):
        self.instanceID = instanceID
        self.instance_path = os.path.join(os.path.dirname(__file__), "instances\\", f"{self.instanceID}")
        
        self.instance=pd.DataFrame()
        
        self.n_jobs=0
        self.n_machines=0
        self.max_bound=0

        self.places = {}
        self.transitions ={}
        
        self.load_instance()
        self.create_jssp()
        print(self.instance)  
       
        self.delivery_history={}
        
        self.internal_clock=0
        self.interaction_counter=0
        self.total_internal_steps=0
        
        self.action_map=self.action_mapping(self.n_machines, self.n_jobs)


    def __str__(self):
         return f" JSSP {self.instanceID} : {self.n_jobs} jobs X {self.n_machines} machine "
     
        
    class Token():
        def __init__(self,initial_place, color=(None,None),process_time=0 ,order=0):
            '''
            color =(job_color, machine_color)
            ----------
            '''            
            self.uid = str (Jssp_petri.uid) 
            Jssp_petri.uid += 1  
      
            self.color = color
            self.process_time=process_time
            self.order=order
            self.logging={initial_place:[0,0,0]}  # entry time , leave time, elapset time 
            

        def __str__(self):
            return f"id: {self.uid}, color: {self.color} , process_time {self.process_time} , order{self.order} ,logging : {self.logging}"
        
  
    class Place:
        def __init__(self,label,role="",color=None ):
            self.uid = str (Jssp_petri.uid) 
            Jssp_petri.uid += 1  
     
            self.label = label
            self.type = role 
            self.parents = []
            self.children = []
            
            self.token_container=[]
            self.color=color

        def add_arc(self, node, parent=True):
            if parent:
                self.parents.append(node)
            else:
                self.children.append(node)

        def __str__(self):
            return f" Place name: {self.label}, type={self.type} ,Tokens: {len(self.token_container)} ,color: {self.color}  ,parents={self.parents} ,childs={self.children} , id ={self.uid}"

    
    class Transition:
        def __init__(self,label,role="" ,color=None):
            
            self.uid = str (Jssp_petri.uid) 
            Jssp_petri.uid += 1  
            
            self.label = label
            self.type = role
            self.color=color
            
            self.parents = []
            self.children = []
            self.enabled = True 
  
        def add_arc(self, node, parent=True):
            if parent:
                self.parents.append(node)
            else:
                self.children.append(node)

        def __str__(self):
            return f" Transition name: {self.label},type={self.type},color: {self.color} ,parents={self.parents} ,childs={self.children} , id ={self.uid}"
        
#%% manipulate JSSP         
        

    def load_instance(self): 
       data = []

       try:
           with open(self.instance_path, 'r') as file:
            for line in file:
                elements = line.strip().split()
                data.append(elements)
                
            print(f" Instance '{self.instanceID}' is loaded  .")

       except FileNotFoundError:
           print(f"The file '{self.instance_path}' was not found.")
       except Exception as e:
           print(f"An error occurred: {str(e)}")
           
       raw_instance= pd.DataFrame(data).fillna(0).drop(0)
       raw_instance = raw_instance.apply(pd.to_numeric, errors='coerce')
       
       # get the maximum number of operation / token  
       self.max_bound= max([ len(row) for row in raw_instance.values])
       self.max_bound=raw_instance.values.max().max()
       

       for i in range(0, raw_instance.shape[1], 2):
           
            machine = raw_instance.columns[i]
            time = raw_instance.columns[i + 1]
            machine_time = f" {int (i/2)}"
            self.instance[machine_time] = list(zip(raw_instance[machine], raw_instance[time]))
     
 
       self.n_jobs=self.instance.shape[0]
       self.n_machines=self.instance.shape[1]
      
      
       return raw_instance
   
        
    def add_nodes_layer(self, is_place=True, node_type="" ,number=1 ):
        
        if is_place :
            for i in range(number):
                place_name = f"{node_type} {i}"
                place = self.Place(place_name, node_type ,color=i )
                self.places[place.uid] = place

        else:
            for i in range(number):
                transition_name = f"{node_type} {i}" 
                transition = self.Transition(transition_name, node_type ,color=i)
                self.transitions[transition.uid] = transition 
                
                
    def add_connection(self, parent_type, child_type ,contype="p2t" ,full_connect=False):
        
        if contype == "p2t":
            
          parent_node = [p for p in self.places.values() if p.type == parent_type]
          child_node = [t for t in self.transitions.values() if t.type == child_type]
          
        elif contype == "t2p":
            parent_node = [t for t in self.transitions.values() if t.type == parent_type]
            child_node = [p for p in self.places.values() if p.type == child_type]
                        
          
        if full_connect : 
            for parent in parent_node:
                for child in child_node:
                    parent.add_arc(child, parent=False)
                    child.add_arc(parent, parent=True)
        else: 
            
            for parent,child in zip (parent_node,child_node):   
                parent.add_arc(child, parent=False)
                child.add_arc(parent, parent=True)
                

    def filter_nodes(self,node_type):
        
        filtered_nodes=[]
        for place in self.places.values():
            if place.type == node_type:
                filtered_nodes.append(place.uid)
                
        for transition in self.transitions.values():
            if transition.type == node_type:
                filtered_nodes.append(transition.uid)     
                
        return  filtered_nodes
    
    def add_tokens(self):
        #Add idle tokens 
        for uid in self.filter_nodes("idle")  :
            self.places[uid].token_container.append(self.Token(initial_place=uid,color=(None,self.places[uid].color)))
            self.places[uid].color=None 
            
        #Add tokens :
        for job,uid in enumerate(self.filter_nodes("job")) : 
            for i,operation in enumerate (self.instance.iloc[job]):  
                machine,process_time= operation 
                self.places[uid].token_container.append(
                    self.Token(initial_place=uid,color=(job,machine),process_time=process_time, order=i))
   
    def create_jssp(self):
        
        nodes_layers=[ (True,"job",self.n_jobs),
                       # (False,"preselect",self.n_jobs),
                       # (True,"queue",self.n_jobs),
                       (False,"allocate",self.n_machines),
                       (True,"machine",self.n_machines),
                       (False,"finish_op",self.n_machines),
                       (True,"finished_ops",self.n_machines),  
                       #(True,"idle",self.n_machines),
                          
                       ]
                         
        layers_to_connect=[
                           ("job","allocate","p2t",True),
                           # ("job","preselect","p2t",False),
                           # ("preselect","queue","t2p",False),
                           # ("queue","allocate","p2t",True),  
                           ("allocate","machine","t2p",False),
                           ("machine","finish_op","p2t",False),
                           ("finish_op","finished_ops","t2p",False),
                           #("finish_op","idle","t2p",False),
                           #("idle","allocate","p2t",False)
                           
                           ]
        
        #Add nodes : plaxes and transitions
        for is_place,node_type,number in nodes_layers:   
            self.add_nodes_layer(is_place,node_type,number)
    
        #Add arcs places and transitions 
        for parent_type, child_type, contype, full_connect in layers_to_connect:   
            self.add_connection(parent_type, child_type,contype, full_connect)
            
        #Add jobs tokens     
        self.add_tokens()
          
        #Add idles transition :
        transition = self.Transition("standby", "allocate" ,color=self.n_machines)
        transition.children.append(self.Place("standby_place", "idle_state" ,color=self.n_machines ))
        
        self.transitions[transition.uid] = transition
        
        print (f"JSSP {self.instanceID} : {self.n_jobs} jobs X {self.n_machines} machines  loaded ")
               
       
#%%  manipulate Petri-Jssp 

    def projected_makespan(self):
        
        waiting_penalty = self.n_machines
        
        completion_time=[1 for _ in range(self.n_machines)]
        jobs_queue=[p for p in self.places.values() if p.uid in self.filter_nodes("job")]
        machine_places = [p for p in self.places.values() if p.uid in self.filter_nodes("machine")]  
    
        # Step 1: Estimate completion time for operations in process
        for machine in machine_places :
            if  len (machine.token_container)>0:
              for in_process in machine.token_container :
                  elapsed=in_process.logging[list(in_process.logging.keys())[-1]][2] 
                  remaining = in_process.process_time-elapsed
                  completion_time[in_process.color[1]]= self.internal_clock +remaining 
            else  :
                completion_time=[self.internal_clock for _ in range(self.n_machines)]

        # Step 2: Assume optimal processing of remaining operations
        for job in jobs_queue:
            if  len (job.token_container)>0:
                for operation in job.token_container:
                    completion_time[operation.color[1]]+=operation.process_time * waiting_penalty
                    
        return max (completion_time)
 

    def time_tick(self,gui,action):
          
          self.internal_clock += 1
          self.total_internal_steps+=1
          # increment time in token logging 
          for place in self.places.values() : 
              for token in place.token_container:
               token.logging[list(token.logging.keys())[-1]][2]+=1
                             
          if gui is not None and  gui.render_mode == "human"  :   
             create_png(gui,action)
               
                     
    def is_terminal(self):  
  
         output=[p for p in self.places.values() if p.uid in self.filter_nodes("finished_ops")]
         to_deliver=[len(self.instance[job]) for job in self.instance]
         delivered =[len(out.token_container) for out in output]
         
         # print (to_deliver)
         # print (delivered)
         
         return all(to_deliver[i] <= delivered[i] for i in range(len(to_deliver)))
     
        
    def action_mapping(self,n_machiens,n_jobs):      
        #move the action from multidiscrete to discrete to allow masking and DQN
         
         tuples = []
         mapping_dict = {}

         for machine in range(n_machiens):
             for job in range(n_jobs):
                 tuple_entry = (machine, job)
                 tuples.append(tuple_entry)
                 # Create an inverse mapping from the index to the tuple
                 index = len(tuples) - 1
                 mapping_dict[index] = tuple_entry 
                 
         idle = {len(mapping_dict.keys()): (self.n_machines,0)}
         mapping_dict.update(idle)
         
         return mapping_dict


    def enabled_allocations(self):
        
        allocate_transitions = [t for t in self.transitions.values() if t.uid in self.filter_nodes("allocate")]
        jobs_queue=[p for p in self.places.values() if p.uid in self.filter_nodes("job")]
        
        enabled_mask = [False] * len (self.action_map.keys()) 
        for key,action in  self.action_map.items():
   
            idle =True 
            job_op=jobs_queue[action[1]]
            allocation =  allocate_transitions[action[0]]
            machine = allocation.children[0]
            
            if len (machine.token_container)>0:
                idle =False
              
            if len (job_op.token_container)>0 :
                operation_color =job_op.token_container[0].color[1]
                if machine.color==operation_color and  idle :
                    enabled_mask[key]=True
             
        # idles transition is always enabled      
        enabled_mask[-1]=True
        
        
        #filtered_actions = [value for value, mask in zip(self.action_map.values(), enabled_mask) if mask]
     
        return  enabled_mask 
    
    def transfer_token(self,origin,destination,current_clock=0):
        
         logging=  origin.token_container[0].logging[origin.uid]  
         logging[1]=logging[0]+logging[2]

         token=copy.copy(origin.token_container[0])
         origin.token_container.pop(0) 
         destination.token_container.append(token)          
         token.logging[destination.uid]=[current_clock,0,0] 
         
         
    def fire_colored (self,action):
        '''
        - to make it compatible with Gym , the iput is multid discreate [transiton (machine) , job ]
        ----------
        ''' 
        self.interaction_counter+=1
        
        
        fired=False
        action=self.action_map[action]
        transition_num= action[0]
        job_num=action[1]
        
        
        transition=[t for t in self.transitions.values() if t.uid in self.filter_nodes("allocate")][transition_num] 
        if  transition_num!=self.n_machines:# aka not standby 
            if len(transition.children[0].token_container)==0  :  
                for job_queue in transition.parents:  
                    if len (job_queue.token_container)>0 :
                        if  job_queue.token_container[0].color == (job_num,transition.color): 
                            self.transfer_token(job_queue,transition.children[0],current_clock=self.internal_clock) 
                            fired=True            
        else :
             fired =True
             
        return fired


    def fire_timed (self):
        '''
        this fires the autonomus transitons 
        -------
        '''
       
        ready_transitions=[]
        machine_places=[p for p in self.places.values() if p.uid in self.filter_nodes("machine")] 
        for place in  machine_places :
            for token in place.token_container :
                if token.logging[list(token.logging.keys())[-1]][2]>token.process_time:
                    ready_transitions.append(place.children[0])

        for transition in ready_transitions :    
            self.transfer_token(transition.parents[0],transition.children[0],current_clock=self.internal_clock)
            
            
        #keep a history of delivery (to use in solution later )
        finished_tokens = []
        finished_places = [p for p in self.places.values() if p.uid in self.filter_nodes("finished_ops")]
        for place in finished_places:
            finished_tokens.extend(place.token_container)  
        self.delivery_history[self.internal_clock]=finished_tokens
        
        
    def env_interact(self,gui,action):
        

        before = self.projected_makespan()

        self.fire_timed()
        fired=self.fire_colored(action)
        self.time_tick(gui,action)   
  
        # only the idle is enabled aka no action available 
        while sum (self.enabled_allocations()) == 1 : 
  
            self.fire_timed()
            self.time_tick(gui,action) 
            if self.is_terminal() :
                break

        after = self.projected_makespan()   
        #print(self.projected_makespan() )

        return fired, (before-after)

    def petri_reset(self):   
        
        self.internal_clock=0
        for place in self.places.values() :
            place.token_container=[]
        # Add tokens 
        self.add_tokens()
            
        
#%%  test

if __name__ == "__main__":
    
    jssp=Jssp_petri("ta01")
    


    




