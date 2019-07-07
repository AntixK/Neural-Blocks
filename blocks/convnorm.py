import torch.nn as nn
from NeuralBlocks.blocks.meanspectralnorm import MeanSpectralNormConv2d
from NeuralBlocks.blocks.meanweightnorm import MeanWeightNormConv2d

class ConvNorm(nn.Module):

    def __init__(self, in_channels, out_channels, kernel_size,
                 stride=1, padding=0, dilation=1, groups=1,
                 bias = True, padding_mode='zeros', norm = 'BN', groups_size=16):
        super(ConvNorm, self).__init__()

        if norm not in [None,'BN', 'IN', 'GN', 'LN','WN', 'MSN']:
            raise ValueError("Undefined norm value. Must be one of "
                             "[None,'BN', 'IN', 'GN', 'LN', 'WN', 'MSN']")
        layers = []
        if norm == 'MSN':
            conv2d = MeanSpectralNormConv2d(in_channels, out_channels, kernel_size,
                 stride, padding, dilation, groups,
                 bias, padding_mode)
            layers += [conv2d ]
        elif norm == 'WN':
            conv2d = MeanWeightNormConv2d(in_channels, out_channels, kernel_size,
                 stride, padding, dilation, groups,
                 bias, padding_mode)
            layers += [conv2d ]
        elif norm == 'IN':
            conv2d = nn.Conv2d(in_channels, out_channels, kernel_size,
                 stride, padding, dilation, groups,
                 bias, padding_mode)
            layers += [conv2d, nn.InstanceNorm2d(out_channels) ]
        elif norm == 'GN':
            conv2d = nn.Conv2d(in_channels, out_channels, kernel_size,
                 stride, padding, dilation, groups,
                 bias, padding_mode)
            layers += [conv2d, nn.GroupNorm(groups_size, out_channels) ]
        elif norm == 'LN':
            conv2d = nn.Conv2d(in_channels, out_channels, kernel_size,
                 stride, padding, dilation, groups,
                 bias, padding_mode)
            layers += [conv2d, nn.LayerNorm(out_channels) ]
        elif norm == 'BN':
            conv2d = nn.Conv2d(in_channels, out_channels, kernel_size,
                 stride, padding, dilation, groups,
                 bias, padding_mode)
            layers += [conv2d, nn.BatchNorm2d(out_channels) ]
        else:
            conv2d = nn.Conv2d(in_channels, out_channels, kernel_size,
                               stride, padding, dilation, groups,
                               bias, padding_mode)
            layers += [conv2d]

        self.layers= nn.Sequential(*layers)

    def forward(self, input):
        x = self.layers(input)
        return x