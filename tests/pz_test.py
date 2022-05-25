from pettingzoo.atari import basketball_pong_v3


env = basketball_pong_v3.env(num_players=2)
env.reset()

i = 0
for agent in env.agent_iter(200):
    i += 1
    print(f"iteration: {i}, agent: {agent}")
    env.render()
    observation, reward, done, info = env.last()
    action = env.action_space(agent).sample()
    env.step(action)
