import numpy as np
import pygame
import gym

from macce.env.utils import *
from macce.env.sprites import Ship, Fort
from macce.env.renderer import Renderer


def _fort_init_position(nums):
    coords = []
    return coords


def _ship_init_position(nums):
    coords = []
    return coords


class Macce(gym.Env):

    metadata = {"render.modes": ["human", "rgb_array"]}

    def __init__(self, version='2s_vs_2f', seed=0):
        super(Macce, self).__init__()
        self.version = version
        self.seed = seed
        self.setting = get_setting(version)

        self._init()

    def _init(self):
        self.n_attackers = 0
        self.n_defenders = 0

        self.attacker_group = pygame.sprite.Group()
        self.defender_group = pygame.sprite.Group()
        self.attacker_missile_group = pygame.sprite.Group()
        self.defender_missile_group = pygame.sprite.Group()

        attacker_entities = []
        attacker = self.setting.get('attacker')
        if attacker.get('ship') is not None:
            ship = attacker['ship']
            self.n_attackers += ship['num']
            ships = self._create_sprite('ship', self.attacker_missile_group, **ship)
            attacker_entities += ships
            self.attacker_group.add(ships)

        defender_entities = []
        defender = self.setting.get('defender')
        if defender.get('fort') is not None:
            fort = defender['fort']
            self.n_defenders += fort['num']
            forts = self._create_sprite('fort', self.defender_missile_group, **fort)
            defender_entities += forts
            self.defender_group.add(forts)

        self.attackers = [r for r in range(self.n_attackers)]
        self.defenders = [r for r in range(self.n_defenders)]
        self.attacker_id_mapping = dict(zip(self.attackers, attacker_entities))
        self.defender_id_mapping = dict(zip(self.defenders, defender_entities))

        self._renderer = Renderer(screen_size,
                                  self.attacker_group,
                                  self.defender_group,
                                  self.attacker_missile_group,
                                  self.defender_missile_group)

    @staticmethod
    def _create_sprite(sprite_type, group, **kwargs):
        sprites = []
        if sprite_type == 'ship':
            coords = _ship_init_position(kwargs.get('num'))
            for i, (x, y) in enumerate(coords):
                ship = Ship('attacker', i, Rect(x, y, *ship_size), group, **kwargs)
                sprites.append(ship)

        elif sprite_type == 'fort':
            coords = _fort_init_position(kwargs.get('num'))
            for i, (x, y) in enumerate(coords):
                fort = Fort('defender', i, Rect(x, y, *fort_size), group, **kwargs)
                sprites.append(fort)
        else:
            raise ValueError(f'Tried to create a {sprite_type} sprite,'
                             'but without such a sprite!')
        return sprites

    def step(self, actions):
        # obs = []
        rewards = []
        dones = []

        for attacker, action in zip(self.attackers, actions[:len(self.attackers)]):
            reward, done = self.attacker_id_mapping[attacker].handle(action)
            rewards.append(reward)
            dones.append(done)

        for defender, action in zip(self.defenders, actions[len(self.attackers):]):
            reward, done = self.attacker_id_mapping[defender].handle(action)
            rewards.append(reward)
            dones.append(done)

        return rewards, dones

    def reset(self):
        self._init()

    def render(self, mode="human"):
        if mode not in Macce.metadata['render.modes']:
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
