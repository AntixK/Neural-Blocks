import torch.nn as nn
from torch.nn.utils.spectral_norm import spectral_norm

class ConvNormPool(nn.Module):
    """
    A simply block consisting of a convolution layer,
    a normalization layer, ReLU activation and a pooling
    layer. For example, this is the first block in the
    ResNet architecture.
    """

    def __init__(self, in_channels, out_channels,norm='BN', act='ReLU', **kwargs):
        super(ConvNormPool, self).__init__()

        if 'conv_args' in kwargs:
            kernel_size, stride,padding, bias = kwargs['conv_args']
            self.conv = nn.Conv2d(in_channels, out_channels,
                                  kernel_size=kernel_size,
                                  stride=stride,
                                  padding=padding, bias=bias)

        else:
            self.conv = nn.Conv2d(in_channels, out_channels,
                                  kernel_size=3,
                                  stride=2,
                                  padding=3, bias=False)

        self.norm_type = norm

        if norm == 'IN':
            self.norm = nn.InstanceNorm2d(out_channels)
        elif norm == 'GN':
            self.norm = nn.GroupNorm(16, out_channels)
        elif norm == 'SN':
            self.conv = spectral_norm(self.conv)
        else:
            if norm != 'BN':
                raise UserWarning('Undefined normalization '+norm+'. Using BatchNorm instead.')
            self.norm = nn.BatchNorm2d(out_channels)

        if act == 'LeakyReLU':
            self.act = nn.LeakyReLU(inplace=True)
        else:
            self.act = nn.ReLU(inplace=True)

        if 'pool_args' in kwargs:
            kernel_size, stride,padding, bias = kwargs['pool_args']
            self.maxpool = nn.MaxPool2d(kernel_size=kernel_size,
                                  stride=stride,
                                  padding=padding)

        else:
            self.maxpool = nn.MaxPool2d(kernel_size=3,
                                       stride=2, padding=1)

    def forward(self, input):
        if self.norm_type == 'SN':
            x = self.conv(input)
        else:
            x = self.norm(self.conv(input))
        x = self.act(x)
        x = self.maxpool(x)
        return x
