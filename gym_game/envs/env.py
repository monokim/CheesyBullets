import gym
from gym import spaces
import numpy as np
from gym_game.envs.game import Game
import time
from util import Timer

class Env(gym.Env):
    metadata = {'render.modes' : ['human']}
    def __init__(self):
        self.action_space = spaces.Discrete(5)
        self.game = Game()
        self.memory = []
        self.timer = Timer()
        #self.is_view = False

    def reset(self):
        del self.game
        self.game = Game()
        #obs = self.game.observe()
        #return obs

    def step(self, action):
        self.game.action(action)
        reward = self.game.evaluate()
        done = self.game.is_done()
        #obs = self.game.observe()
        self.game.view()
        return None, reward, done, {}

    def render(self, mode="human", close=False):
        return self.game.get_screen()
        #self.game.view()

    def save_memory(self, file):
        np.save(file, self.memory)
        print(file + " saved")

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
