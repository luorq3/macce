from typing import Optional, Tuple

import gym
import numpy as np
import pygame
from macce.env.renderer import Renderer
# from macce.env.game_logic import GameLogic

from macce.env.utils import load_images


class MultiAgentCombatEnvRGB(gym.Env):

    metadata = {"render.modes": ["human", "rgb_array"]}

    def __init__(self,
                 screen_size: Tuple[int, int] = (896, 896)):
        super(MultiAgentCombatEnvRGB, self).__init__()
        self.action_space = gym.spaces.Discrete(6)
        self.observation_space = gym.spaces.Box(0, 255, [*screen_size, 3], dtype=np.uint8)

        self.images = load_images(convert=False)

        self._screen_size = screen_size
        self._game = None
        self._renderer = Renderer(screen_size=self._screen_size)

    def _get_observation(self):
        self._renderer.draw_surface()
        return pygame.surfarray.array3d(self._renderer.surface)

    def reset(self, *, seed: Optional[int] = None, return_info: bool = False, options: Optional[dict] = None):
        self._game = GameLogic(self.images, screen_size=self._screen_size)
        self._renderer.game = self._game
        return self._get_observation()

    def step(self, actions):
        rewards, alive = self._game.update_state(actions)
        obs = self._get_observation()

        done = not alive
        info = {"reward": rewards}

        return obs, rewards, done, info

    def render(self, mode="human") -> Optional[np.ndarray]:
        if mode not in MultiAgentCombatEnvRGB.metadata['render.modes']:
            raise ValueError("Invalid render mode!")

        self._renderer.draw_surface()

        if mode == 'rgb_array':
            return pygame.surfarray.array3d(self._renderer.surface)
        else:
            if self._renderer.display is None:
                self._renderer.make_display()
            self._renderer.update_display()

    def close(self):
        if self._renderer is not None:
            pygame.display.quit()
            self._renderer = None

        super().close()
