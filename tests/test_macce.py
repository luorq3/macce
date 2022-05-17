from macce.env.game_logic import Macce

import time

import macce
import numpy as np
import pygame
from PIL import Image


# Action={0:NOOP, 1:UP, 2:DOWN, 3:LEFT, 4:RIGHT, 5:FIRE}
def play_with_render(env):
    clock = pygame.time.Clock()
    score = np.zeros(2)

    obs = env.reset()
    while True:
        env.render()

        actions = [0] * 2
        # Getting action
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    actions[0] = 1
                elif event.key == pygame.K_RIGHT:
                    actions[0] = 2
                elif event.key == pygame.K_LEFT:
                    actions[0] = 3

        # Processing
        obs, reward, done, info = env.step(actions)

        # score += reward
        # print(f"Obs shape: {obs.shape}")
        # print("Score: {}".format(score))

        clock.tick(30)

        # if done:
        #     env.render()
        #     time.sleep(0.6)
        #     break


def visualize_obs(env, greyscale: bool):
    obs = env.get_state()
    obs = np.moveaxis(obs, source=1, destination=0)
    if greyscale:
        obs = obs.mean(axis=-1)
    print(f"Obs shape: {obs.shape}")
    img = Image.fromarray(obs)
    img.show()
    time.sleep(3)
    img.close()


if __name__ == "__main__":
    env = Macce(version="1s_vs_1f")

    # print(f"Action space: {env.get_total_actions()}")
    # print(f"Observation space: {env.get_state()}")
    # visualize_obs(env, greyscale=False)
    # visualize_obs(env, greyscale=True)

    play_with_render(env=env)

    env.close()
