import torch
import torch.nn as nn
import torch.nn.functional as F
from survae.nn.layers import LambdaLayer
from survae.nn.layers import act_module


def init_weights(m):
    if type(m) == nn.Linear:
        torch.nn.init.xavier_uniform(m.weight)
        m.bias.data.fill_(0.01)


class MLP(nn.Sequential):
    def __init__(self, input_size, output_size, hidden_units, activation='relu', in_lambda=None, out_lambda=None):
        layers = []
        if in_lambda: layers.append(LambdaLayer(in_lambda))
        for in_size, out_size in zip([input_size] + hidden_units[:-1], hidden_units):
            layers.append(nn.Linear(in_size, out_size))
            layers.append(act_module(activation))
        layers.append(nn.Linear(hidden_units[-1], output_size))
        if out_lambda: layers.append(LambdaLayer(out_lambda))

        super(MLP, self).__init__(*layers)
        '''
        for layer in layers:
            if type(layer) == nn.Linear:
                # layer.weight.data.fill_(0)
                nn.init.xavier_normal_(layer.weight.data, 0.1)
                layer.bias.data.fill_(0)
        '''