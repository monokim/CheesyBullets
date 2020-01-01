import sys
import numpy as np
import math
import random
import matplotlib.pyplot as plt

from dqn import DQN, ReplayMemory, Transition
from util import Timer

import gym
import gym_game
import torch
import torch.nn.functional as F
import util

def simulate():
    num_episodes = 20000
    #env.is_view = True
    for epi in range(num_episodes):
        env.reset()
        last_screen = torch.from_numpy(env.render()).unsqueeze(0).to(device)
        current_screen = torch.from_numpy(env.render()).unsqueeze(0).to(device)
        state = current_screen - last_screen
        total_reward = 0
        timer.set_timer("episode")
        #if epi == 500:
        for t in range(MAX_T):
            action = select_action(state)
            _, reward, done, _ = env.step(action.item())

            total_reward += float(reward)
            reward = torch.tensor([reward], device=device)
            last_screen = current_screen
            current_screen = torch.from_numpy(env.render()).unsqueeze(0).to(device)
            if done:
                next_state = None
            else:
                next_state = current_screen - last_screen

            memory.push(state, action, next_state, reward)
            state = next_state

            #env.render()
            optimize_model()

            if done:
                print("episode %d, total reward = %f" % (epi + 1, total_reward))
                break

        timer.print_time("episode")
        print("")
        if epi % TARGET_UPDATE == 0:
            target_net.load_state_dict(policy_net.state_dict())


def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transition = memory.sample(BATCH_SIZE)
    batch = Transition(*zip(*transition))
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)

    state_action_values = policy_net(state_batch).gather(1, action_batch)
    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0].detach()

    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))
    optimizer.zero_grad()
    loss.backward()
    for param in policy_net.parameters():
        param.grad.data.clamp_(-1, 1)
    optimizer.step()


def select_action(state):
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            return policy_net(state).max(1)[1].view(1, 1)
    else:
        return torch.tensor([[random.randrange(n_actions)]], device=device, dtype=torch.long)


if __name__ == "__main__":
    BATCH_SIZE = 128
    GAMMA = 0.999
    EPS_START = 0.9
    EPS_END = 0.05
    EPS_DECAY = 200
    TARGET_UPDATE = 10
    MAX_T = 9999
    steps_done = 0
    timer = Timer()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    env = gym.make("Game-v0")
    height, width = 64, 64

    n_actions = env.action_space.n
    policy_net = DQN(width, height, n_actions).to(device)
    target_net = DQN(width, height, n_actions).to(device)
    target_net.load_state_dict(policy_net.state_dict())
    target_net.eval()

    optimizer = torch.optim.RMSprop(policy_net.parameters())
    memory = ReplayMemory(3000)
    simulate()
