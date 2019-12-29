import torch.nn as nn


class MobileNet(nn.Module):
    def __init__(self):
        super(MobileNet, self).__init__()  # call parent's __init__ method.
        
        def conv(in_channels, out_channels, kernel_size, stride, padding):
            pass
        
        def conv_dw(in_channels, out_channels, kernel_size, stride, padding):
            pass