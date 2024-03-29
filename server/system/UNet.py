import torch.nn as nn
import torch

def double_conv(in_channels, out_channels):
    return nn.Sequential(
        nn.Conv2d(in_channels, out_channels, 3, padding=1),
        nn.ReLU(inplace=True),
        nn.Conv2d(out_channels, out_channels, 3, padding=1),
        nn.ReLU(inplace=True)
    )


class UNet(nn.Module):

    def __init__(self, n_class):
        super().__init__()
        #         f = [16, 32, 64, 128]
        #         f=[64,128,256,512]
        f = [32, 64, 128, 256]
        self.dconv_down1 = double_conv(3, f[0])
        self.dconv_down2 = double_conv(f[0], f[1])
        self.dconv_down3 = double_conv(f[1], f[2])
        self.dconv_down4 = double_conv(f[2], f[3])

        self.maxpool = nn.MaxPool2d(2)
        self.upsample = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)

        self.dconv_up3 = double_conv(f[2] + f[3], f[2])
        self.dconv_up2 = double_conv(f[1] + f[2], f[1])
        self.dconv_up1 = double_conv(f[1] + f[0], f[0])

        self.conv_last = nn.Conv2d(f[0], n_class, 1)

    def forward(self, x):
        conv1 = self.dconv_down1(x)
        x = self.maxpool(conv1)

        conv2 = self.dconv_down2(x)
        x = self.maxpool(conv2)

        conv3 = self.dconv_down3(x)
        x = self.maxpool(conv3)

        x = self.dconv_down4(x)

        x = self.upsample(x)
        x = torch.cat([x, conv3], dim=1)

        x = self.dconv_up3(x)
        x = self.upsample(x)
        x = torch.cat([x, conv2], dim=1)

        x = self.dconv_up2(x)
        x = self.upsample(x)
        x = torch.cat([x, conv1], dim=1)

        x = self.dconv_up1(x)

        out = self.conv_last(x)

        return out
