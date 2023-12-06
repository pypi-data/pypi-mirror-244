from gymnasium.envs.registration import register

register(
     id="Jssp-v0",
     entry_point="jsspetri.envs.jssp_env:Jssp_Env",

     nondeterministic=False,
     max_episode_steps=10000,
     #reward_threshold=0
     
     
)




