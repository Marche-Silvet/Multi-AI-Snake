# agent/snake_agent.py

import random
import numpy as np
import torch
import torch.optim as optim
import torch.nn as nn

from agent.snake_net import SnakeNet
from config import TRAINING_EPISODES, MODEL_SAVE_INTERVAL

class SnakeAgent:
    def __init__(self, mode='training'):
        self.mode = mode  # 'training' or 'inference'
        self.net = SnakeNet()
        self.optimizer = optim.Adam(self.net.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()
        self.epsilon = 1.0         # Starting exploration probability
        self.epsilon_min = 0.01    # Minimum epsilon
        self.epsilon_decay = 0.995 # Decay rate per move
        self.training_episode = 0  # Count of training episodes
        self.cumulative_reward = 0 # For logging

    def decide_move(self, features):
        """Choose an action based on state features."""
        self.net.eval()
        if self.mode == 'training' and random.random() < self.epsilon:
            return random.randint(0, 2)
        else:
            with torch.no_grad():
                input_tensor = torch.FloatTensor(features)
                q_values = self.net(input_tensor)
                return torch.argmax(q_values).item()
    
    def learn(self, state, action, reward, next_state, done):
        """Perform a learning update after an action."""
        self.net.train()
        state_tensor = torch.FloatTensor(state)
        next_tensor = torch.FloatTensor(next_state)
        
        # Q-learning update.
        q_pred = self.net(state_tensor)[action]
        with torch.no_grad():
            q_next = self.net(next_tensor).max().item() if not done else 0.0
        
        gamma = 0.9
        target = reward + gamma * q_next
        loss = self.criterion(q_pred, torch.tensor(target))
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Decay exploration rate.
        if self.mode == 'training' and self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        return loss.item()

    def set_mode(self, mode):
        self.mode = mode

    def save_model(self, filename):
        torch.save(self.net.state_dict(), filename)
    
    def load_model(self, filename):
        self.net.load_state_dict(torch.load(filename))
        print(f"Loaded model from {filename}")
