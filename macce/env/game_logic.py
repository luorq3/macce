import numpy as np
import pygame

from macce.env.multiagentenv import MultiAgentEnv
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


class Macce(MultiAgentEnv):

    metadata = {"render.modes": ["human", "rgb_array"]}

    def __init__(self, version='2s_vs_2f', seed=0):
        super(Macce, self).__init__()
        self.version = version
        self._seed = seed
        self.setting = get_setting(version)
        self.name = self.setting['name']

        self.n_actions = 10

        self._init(self.setting)

    def _init(self, setting):

        self.attacker_group = pygame.sprite.Group()
        self.defender_group = pygame.sprite.Group()
        self.attacker_missile_group = pygame.sprite.Group()
        self.defender_missile_group = pygame.sprite.Group()

        attacker_entities = []
        defender_entities = []
        attacker = setting.get('attacker')
        self.n_attackers = attacker['num']
        if attacker.get('ship') is not None:
            ship = attacker['ship']
            ships = self._create_sprite('ship', **ship)
            attacker_entities += ships
            self.attacker_group.add(ships)

        defender = setting.get('defender')
        self.n_defenders = defender['num']
        if defender.get('fort') is not None:
            fort = defender['fort']
            forts = self._create_sprite('fort', **fort)
            defender_entities += forts
            self.defender_group.add(forts)

        self.attackers = ["attacker_" + str(r) for r in range(self.n_attackers)]
        self.defenders = ["defender_" + str(r) for r in range(self.n_defenders)]
        self.attacker_name_mapping = dict(zip(self.attackers, attacker_entities))
        self.defender_name_mapping = dict(zip(self.defenders, defender_entities))

        self._renderer = Renderer(screen_size,
                                  self.attacker_group,
                                  self.defender_group,
                                  self.attacker_missile_group,
                                  self.defender_missile_group)

    def _create_sprite(self, sprite_type, **kwargs):
        sprites = []
        if sprite_type == 'ship':
            coords = _ship_init_position(kwargs.get('num'))
            for i, (x, y) in enumerate(coords):
                ship = Ship('attacker', i, Rect(x, y, *ship_size), self.attacker_missile_group, **kwargs)
                sprites.append(ship)

        elif sprite_type == 'fort':
            coords = _fort_init_position(kwargs.get('num'))
            self.fort_coords = np.array(coords)
            for i, (x, y) in enumerate(coords):
                fort = Fort('defender', i, Rect(x, y, *fort_size), self.defender_missile_group, **kwargs)
                sprites.append(fort)
        else:
            raise ValueError(f'Tried to create a {sprite_type} sprite,'
                             'but without such a sprite!')
        return sprites

    def _get_render(self):
        self._renderer.draw_surface()
        return pygame.surfarray.array3d(self._renderer.surface)

    def step(self, actions):
        # obs = []
        rewards = []
        dones = []
        # infos = []

        actions_int = [int(a) for a in actions]
        self.last_action = np.eye(self.n_actions)[np.array(actions_int)]

        for agent, action in zip(self.attackers, actions):
            avail_actions = self.get_avail_agent_actions(agent)
            assert (
                    avail_actions[action] == 1
            ), f"Agent {agent} cannot perform action {action}"
            reward, done = self.attacker_name_mapping[agent].handle(action)
            rewards.append(reward)
            dones.append(done)

        return rewards, dones

    def get_obs(self):
        return [self.fort_coords] * self.n_attackers

    def get_obs_agent(self, agent_id):
        return self.fort_coords

    def get_obs_size(self):
        return self.fort_coords.shape

    def get_state(self):
        return self._get_render()

    # def get_state_size(self):
    #     """Returns the size of the global state."""
    #     raise NotImplementedError

    def get_avail_actions(self):
        avail_actions = []
        for agent_id in range(self.n_attackers):
            avail_action = self.get_avail_agent_actions(agent_id)
            avail_actions.append(avail_action)
        return avail_actions

    def get_avail_agent_actions(self, agent_id):
        unit = self.attacker_name_mapping[agent_id]

        if unit.health <= 0:
            return [1] + [0] * (self.n_actions - 1)

        avail_actions = [0] * self.n_actions
        avail_actions[1:4] = [1] * 3

        if not unit.can_fire():
            return avail_actions

        bombs_num = unit.get_bombs_num()
        enemies_num = len(self.defenders)
        for e_name, e_unit in self.defender_name_mapping.items():
            if e_unit.health > 0:
                e_id = int(e_name.split('_')[1])
                for i in range(len(bombs_num)):
                    if bombs_num[i] > 0:
                        ac_id = enemies_num * i + e_id
                        avail_actions[ac_id + 4] = 1

        return avail_actions

    def get_total_actions(self):
        """Returns the total number of actions an agent could ever take."""
        return self.n_actions

    def reset(self):
        self._init(self.setting)

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
            self._renderer = None

    def seed(self):
        return self._seed

    # def save_replay(self):
    #     """Save a replay."""
    #     raise NotImplementedError

    def get_env_info(self):
        env_info = super(Macce, self).get_env_info()
        return env_info
