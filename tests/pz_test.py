import functools
from pettingzoo.butterfly import pistonball_v6
# from pettingzoo.magent import battle_v3
# from pettingzoo.atari import combat_plane_v2


env = pistonball_v6.env()
# env = combat_plane_v2.env()
# env = pistonball_v6.parallel_env
# pistonball_v6.env(n_pistons=20, time_penalty=-0.1, continuous=True,
#                   random_drop=True, random_rotate=True, ball_mass=0.75, ball_friction=0.3,
#                   ball_elasticity=1.5, max_cycles=125)
env.reset()

i = 0
for agent in env.agent_iter(500):
    i += 1
    print(f"iteration: {i}, agent: {agent}")
    env.render()
    observation, reward, done, info = env.last()
    action = env.action_space(agent).sample()
    # action = agent.action_space.sample()
    env.step(action)
