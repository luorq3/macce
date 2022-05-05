import time

import gym

import macce
import numpy as np
import pygame
from PIL import Image
# from fight_env_gym import FightEnvRGB


# Action={0:NOOP, 1:UP, 2:DOWN, 3:LEFT, 4:RIGHT, 5:FIRE}
def play_with_render(env: gym.Env):
    clock = pygame.time.Clock()
    score = np.zeros(2)

    obs = env.reset()
    while True:
        env.render()

        actions = [[0, 0]] * 2
        # Getting action
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    actions[0][0] = 1
                elif event.key == pygame.K_DOWN:
                    actions[0][0] = 2
                elif event.key == pygame.K_LEFT:
                    actions[0][0] = 3
                elif event.key == pygame.K_RIGHT:
                    actions[0][0] = 4
                elif event.key == pygame.K_SPACE:
                    actions[0][0] = 5
                elif event.key == pygame.K_z:
                    actions[1][0] = 1
                elif event.key == pygame.K_c:
                    actions[1][0] = 2
                elif event.key == pygame.K_x:
                    actions[1][0] = 3

            # Processing
        obs, reward, done, info = env.step(actions)

        score += reward
        # print(f"Obs shape: {obs.shape}")
        print("Score: {}".format(score))

        clock.tick(30)

        if done:
            env.render()
            time.sleep(0.6)
            break


def visualize_obs(env, greyscale: bool):
    obs = env.reset()
    obs = np.moveaxis(obs, source=1, destination=0)
    if greyscale:
        obs = obs.mean(axis=-1)
    print(f"Obs shape: {obs.shape}")
    img = Image.fromarray(obs)
    img.show()
    time.sleep(3)
    img.close()


if __name__ == "__main__":
    mac_env = macce.make("MultiAgentCombat-rgb-v0")

    print(f"Action space: {mac_env.action_space}")
    print(f"Observation space: {mac_env.observation_space}")

    # visualize_obs(fight_env, greyscale=False)
    # visualize_obs(fight_env, greyscale=True)

    play_with_render(env=mac_env)

    mac_env.close()
