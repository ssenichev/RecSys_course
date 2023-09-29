import torch
import torch.nn as nn


class Dice(nn.Module):
    """The Dice activation function 
    https://arxiv.org/abs/1706.06978
    """

    def __init__(self, epsilon=1e-3):
        super(Dice, self).__init__()
        self.epsilon = epsilon
        self.alpha = nn.Parameter(torch.randn(1))

    def forward(self, x: torch.Tensor):
        avg = x.mean(dim=1)
        avg = avg.unsqueeze(dim=1)
        var = torch.pow(x - avg, 2) + self.epsilon
        var = var.sum(dim=1).unsqueeze(dim=1)

        ps = (x - avg) / torch.sqrt(var)

        ps = nn.Sigmoid()(ps)  # N * 1
        return ps * x + (1 - ps) * self.alpha * x


def activation_layer(act_name):
    """
    Args:
        act_name: str or nn.Module, name of activation function
    
    Returns:
        act_layer: activation layer
    """
    act_layers = {'sigmoid' : nn.Sigmoid(),
                 'relu' : nn.ReLU(inplace=True),
                 'dice': Dice(),
                 'prelu': nn.PReLU(),
                 "softmax": nn.Softmax(dim=1)}
    
    if isinstance(act_name, str):
        act_layer = act_layers[act_name.lower()]
    elif issubclass(act_name, nn.Module):
        act_layer = act_name()
    else:
        raise NotImplementedError
    return act_layer
