import torch
import torch.nn as nn
import torch.nn.functional as F

class SnakeNet(nn.Module):
    def __init__(self, input_dim=7, output_dim=3):
        super(SnakeNet, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_dim)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
