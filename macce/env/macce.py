import gym
import numpy as np

from macce.env.renderer import FightRenderer
from multiagentenv import MultiAgentEnv


screen_size = (896, 896)


class MACCEnv(MultiAgentEnv):

    def __init__(self):
        super(MultiAgentEnv, self).__init__()
        self.action_space = gym.spaces.Discrete(6)
        self.observation_space = gym.spaces.Box(0, 255, [*screen_size, 3], dtype=np.uint8)

        self._screen_size = screen_size
        self._game = None
        self._renderer = FightRenderer(screen_size=self._screen_size)

        self.n_agents = 0
        self.episode_limit = 0



