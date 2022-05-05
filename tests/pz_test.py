import functools
from pettingzoo.butterfly import pistonball_v6

@functools.lru_cache(maxsize=None)
def policy(obs, agent_i):
    return 1


env = pistonball_v6.parallel_env()
# env = pistonball_v6.parallel_env
# pistonball_v6.env(n_pistons=20, time_penalty=-0.1, continuous=True,
#                   random_drop=True, random_rotate=True, ball_mass=0.75, ball_friction=0.3,
#                   ball_elasticity=1.5, max_cycles=125)
env.reset()


for agent in env.agent_iter():
    observation, reward, done, info = env.last()
    action = policy(observation, agent)
    env.step(action)
