import torch
from torch import nn


class CheckersEvaluator(nn.Module):
    def __init__(self):
        super(CheckersEvaluator, self).__init__()

        self.fc1 = nn.Conv2d(1,16,5)
        # self.fc1 = nn.Linear(8 * 8, 128)
        self.fc2 = nn.Linear(256, 64)
        self.fc3 = nn.Linear(64, 2)

        self.relu = nn.ReLU()

    def forward(self, x):
        x = torch.tensor(x, dtype=torch.float)
        # x = x.view(-1, 8 * 8)
        x = x.unsqueeze(0)

        x = self.relu(self.fc1(x))
        x = x.view( -1)

        x = self.relu(self.fc2(x))
        x = self.fc3(x)

        return x
