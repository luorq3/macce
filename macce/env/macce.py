import numpy as np
import pygame
import gym

from macce.env.utils import *
from macce.env.sprites import Ship, Fort
from macce.env.renderer import Renderer


def _fort_init_position(nums):
    coords = []
    x = fort_beach_rect.x
    gap = fort_beach_rect.width / (nums + 1)
    for i in range(nums):
        x += gap
        y = math.sqrt(210 ** 2 - (x - 448) ** 2)
        coords.append((int(x), int(y)))

    return coords


def _ship_init_position(nums):

    if nums == 1:
        return [(700, 450)]

    coords = []
    x = 0
    gap = 856 / (nums + 1)
    for i in range(nums):
        x += gap
        y = ship_init_rect.y
        coords.append((int(x), int(y)))

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
        attacker = self.setting.get('attacker')
        defender = self.setting.get('defender')
        self.n_attackers = attacker['num']
        self.n_defenders = defender['num']

        self.attacker_group = pygame.sprite.Group()
        self.defender_group = pygame.sprite.Group()
        self.attacker_missile_group = pygame.sprite.Group()
        self.defender_missile_group = pygame.sprite.Group()

        attacker_entities = []
        if attacker.get('ship') is not None:
            ship = attacker['ship']
            ships = self._create_sprite('ship', self.attacker_missile_group, self.n_defenders, **ship)
            attacker_entities += ships
            self.attacker_group.add(ships)

        defender_entities = []
        if defender.get('fort') is not None:
            fort = defender['fort']
            forts = self._create_sprite('fort', self.defender_missile_group, self.n_attackers, **fort)
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
    def _create_sprite(sprite_type, group, n_enemies, **kwargs):
        sprites = []
        if sprite_type == 'ship':
            coords = _ship_init_position(kwargs.get('num'))
            for i, (x, y) in enumerate(coords):
                ship = Ship('attacker', i, Rect(x, y, *ship_size), n_enemies, group, **kwargs)
                sprites.append(ship)

        elif sprite_type == 'fort':
            coords = _fort_init_position(kwargs.get('num'))
            for i, (x, y) in enumerate(coords):
                fort = Fort('defender', i, Rect(x, y, *fort_size), n_enemies, group, **kwargs)
                sprites.append(fort)
        else:
            raise ValueError(f'Tried to create a {sprite_type} sprite,'
                             'but without such a sprite!')
        return sprites

    def step(self, actions):
        # obs = []
        rewards = []
        # dones = []

        for attacker, action in zip(self.attackers, actions[:len(self.attackers)]):
            reward = self._handle(self.attacker_id_mapping[attacker], action)
            rewards.append(reward)

        for defender, action in zip(self.defenders, actions[len(self.attackers):]):
            reward = self._handle(self.defender_id_mapping[defender], action)
            rewards.append(reward)

        dones = [self.attacker_id_mapping[idx].health <= 0 for idx in self.attackers] + [self.defender_id_mapping[idx].health <= 0 for idx in self.defenders]

        return rewards, dones

    def _handle(self, agent, action):
        if action in agent.not_fire_action_space():
            return agent.handle(action)
        else:
            return self.fire(agent, action)

    def fire(self, agent, action):
        assert (
            agent.can_fire()
        ), f"Agent cannot fire."

        enemy_id, missile_id = agent.action_to_enemy(action)

        enemy = self.defender_id_mapping[enemy_id] if agent.is_attacker() else self.attacker_id_mapping[enemy_id]
        assert (
            enemy.health > 0
        ), f"Agent {enemy.aorf}_{enemy_id} was already dead."

        missile = agent.missiles[missile_id]
        assert (
            missile.loadage > 0
        ), f"Missile {missile_id} of {enemy.aorf}_{enemy_id} was exhausted."

        # 1. 如果目标距离超过了炮弹的极限距离，不能造成任何伤害，直接产生一个负奖励
        dist = distance(agent.rect, enemy.rect)
        if dist > missile.range:
            return missile.penalty
        # 2. 如果在射程之内，以一定的概率产生伤害
        prob = np.random.choice(agent.miss_prob)
        damage = missile.damage * prob
        reward = damage
        enemy.health -= damage

        return reward

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
