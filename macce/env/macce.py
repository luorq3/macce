import math
import os
from enum import Enum

import gym
import numpy as np
import pygame
import pymunk
import pymunk.pygame_util
import yaml
from gym.utils import seeding

from macce.env.sprites import Ship
from macce.env.sprites import Fort
from macce.env.utils import *

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers
from pettingzoo.utils.conversions import parallel_wrapper_fn


screen_size = (896, 896)


def _fort_init_position(nums):
    coords = []
    x = fort_beach_rect.x
    gap = fort_beach_rect.width / (nums + 1)
    for i in range(nums):
        x += gap
        y = math.sqrt(210 ** 2 - (x - 448) ** 2)
        coords.append((x, y))

    return coords


def _ship_init_position(nums):
    coords = []
    x = 0
    gap = 856 / (nums + 1)
    for i in range(nums):
        x += gap
        y = ship_init_rect.y
        coords.append((x, y))

    return coords


def load_setting(file):
    path = f'setting/{file}.yaml'
    file = open(path, 'r')
    return yaml.safe_load(file.read())


def get_setting(game_version):
    return load_setting('scenarios')[game_version]

class raw_env(AECEnv):

    def __init__(self):
        super().__init__()
        self.setting = get_setting('2s_vs_2f')
        self.dt = 1.0 / self.setting['FPS']
        self.agents_num = self.setting['agents_num']
        self.screen_width = 896
        self.screen_height = 896

        self.agents = ["agent_" + str(r) for r in range(self.agents_num)]
        self._agent_selector = agent_selector(self.agents)

        self.observation_spaces = None
        self.action_spaces = None
        self.state_space = None

        pygame.init()
        pymunk.pygame_util.positive_y_is_up = False

        self.max_cycles = self.setting['max_cycles']

        self.agentList = []
        self.agentRewards = []
        self.recentFrameLimit = (
            20
        )

        # Create_sprites
        self._init_sprites(self.setting)

        self.done = None
        self.agent_selection = None
        self.rewards = None
        self._cumulative_rewards = None
        self.dones = None
        self.info = None
        self.frames = None
        self.np_random = None

    def _init_sprites(self, setting):

        # Sprite group
        self.attacker_group = pygame.sprite.Group()
        self.defender_group = pygame.sprite.Group()
        self.attacker_missile_group = pygame.sprite.Group()
        self.defender_missile_group = pygame.sprite.Group()

        agent_entities = []
        attacker = setting.get(self.ConsType.ATTACKER)
        if attacker.get(self.SpriteType.SHIP) is not None:
            ship = attacker[self.SpriteType.SHIP]
            ships = self._create_sprite('attacker', self.SpriteType.SHIP, **ship)
            agent_entities += ships
            self.attacker_group.add(ships)

        defender = setting.get(self.ConsType.DEFENDER)
        if defender.get(self.SpriteType.FORT) is not None:
            fort = defender[self.SpriteType.FORT]
            forts = self._create_sprite('defender', self.SpriteType.FORT, **fort)
            agent_entities += forts
            self.attacker_group.add(forts)

        self.agent_name_mapping = dict(zip(self.agents, agent_entities))

    def _create_sprite(self, aorf, sprite_type, **kwargs):
        sprites = []
        if sprite_type == self.SpriteType.SHIP:
            coords = _ship_init_position(kwargs.get('number'))
            for x, y in coords:
                ship = Ship(aorf, Rect(x, y, *ship_size), self.attacker_missile_group)
                sprites.append(ship)

        elif sprite_type == self.SpriteType.FORT:
            coords = _fort_init_position(kwargs.get('number'))
            for x, y in coords:
                fort = Fort(aorf, Rect(x, y, *fort_size), self.defender_missile_group)
                sprites.append(fort)
        else:
            raise ValueError(f'Tried to create a {sprite_type} sprite,'
                             'but without such a sprite!')

        return sprites

    class ConsType(Enum):
        ATTACKER, DEFENDER = 'attacker', 'defender'

    class SpriteType(Enum):
        SHIP, FORT = 'ship', 'fort'

    def observation_space(self, agent):
        return self.observation_spaces[agent]

    def action_space(self, agent):
        return self.action_spaces[agent]

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)

    # Observe of corresponding agent
    def observe(self, agent):
        return None

    # RGB snapshot as full state of environment
    def state(self):
        state = None

    # Call renderer to enable render
    def enable_render(self):
        pass

    # Call renderer `close` to quit Pygame
    def close(self):
        pass

    def reset(self, seed=None):
        if seed is not None:
            self.seed(seed)

        self._agent_selector.reinit(self.agents)
        self.agent_selection = self._agent_selector.next()

        self.done = False
        self.rewards = dict(zip(self.agents, [0 for _ in self.agents]))
        self._cumulative_rewards = dict(zip(self.agents, [0 for _ in self.agents]))
        self.dones = dict(zip(self.agents, [False for _ in self.agents]))
        self.info = dict(zip(self.agents, [{} for _ in self.agents]))

        self.frames = 0

        self._init_sprites(self.setting)

    def step(self, action):
        if self.dones[self.agent_selection]:
            return self._was_done_step(action)

        agent = self.agent_name_mapping[self.agent_selection]
        agent.handle(action)





