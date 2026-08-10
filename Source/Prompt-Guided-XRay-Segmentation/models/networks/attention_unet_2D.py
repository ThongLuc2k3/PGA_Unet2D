import torch
import torch.nn as nn
import torch.nn.functional as F

from models.networks_other import init_weights
from .utils import unetConv2
from models.layers.grid_attention_layer import GridAttentionBlock2D

# ================================================================
# 1. UPSAMPLING BLOCK WITH ATTENTION GATE (ORIGINAL DESIGN)
# ================================================================
class unetUp_Attention(nn.Module):
    def __init__(self, skip_channels, gating_channels, out_channels):
        super(unetUp_Attention, self).__init__()

        # Attention gate (3D implementation fixed to run in 2D)
        self.attention = GridAttentionBlock2D(in_channels=skip_channels,
                                              gating_channels=gating_channels,
                                              inter_channels=skip_channels // 2,
                                              sub_sample_factor=(2, 2))

        # Standard decoder path
        self.up = nn.ConvTranspose2d(gating_channels, skip_channels, kernel_size=4, stride=2, padding=1)
        self.conv = unetConv2(skip_channels * 2, out_channels, is_batchnorm=True)

    def forward(self, skip, gating):
        # 1. Filter the skip connection through the attention gate (image only, no prompt)
        skip_att = self.attention(skip, gating)

        # Handle the case where the original code returns a tuple
        if isinstance(skip_att, tuple):
            skip_att = skip_att[0]

        # 2. Upsample the gating signal
        up_gating = self.up(gating)

        # Align spatial size in case of pixel offset from padding
        offset = up_gating.size()[2] - skip_att.size()[2]
        pad = 2 * [offset // 2, offset // 2]
        skip_att = F.pad(skip_att, pad)

        # 3. Concat and conv
        out = self.conv(torch.cat([skip_att, up_gating], dim=1))
        return out

# ================================================================
# 2. ORIGINAL ATTENTION U-NET ARCHITECTURE (BASELINE)
# ================================================================
class Attention_UNet_2D(nn.Module):
    def __init__(self, feature_scale=4, n_classes=1, in_channels=1, is_batchnorm=True):
        super(Attention_UNet_2D, self).__init__()
        self.in_channels = in_channels
        self.is_batchnorm = is_batchnorm
        self.feature_scale = feature_scale

        filters = [64, 128, 256, 512, 1024]
        filters = [int(x / self.feature_scale) for x in filters]

        # --- Encoder ---
        self.conv1 = unetConv2(self.in_channels, filters[0], self.is_batchnorm)
        self.maxpool1 = nn.MaxPool2d(kernel_size=2)

        self.conv2 = unetConv2(filters[0], filters[1], self.is_batchnorm)
        self.maxpool2 = nn.MaxPool2d(kernel_size=2)

        self.conv3 = unetConv2(filters[1], filters[2], self.is_batchnorm)
        self.maxpool3 = nn.MaxPool2d(kernel_size=2)

        self.conv4 = unetConv2(filters[2], filters[3], self.is_batchnorm)
        self.maxpool4 = nn.MaxPool2d(kernel_size=2)

        self.center = unetConv2(filters[3], filters[4], self.is_batchnorm)

        # --- Decoder (uses the original attention block) ---
        self.up_concat4 = unetUp_Attention(skip_channels=filters[3], gating_channels=filters[4], out_channels=filters[3])
        self.up_concat3 = unetUp_Attention(skip_channels=filters[2], gating_channels=filters[3], out_channels=filters[2])
        self.up_concat2 = unetUp_Attention(skip_channels=filters[1], gating_channels=filters[2], out_channels=filters[1])
        self.up_concat1 = unetUp_Attention(skip_channels=filters[0], gating_channels=filters[1], out_channels=filters[0])

        self.final = nn.Conv2d(filters[0], n_classes, 1)

        # Weight initialization
        for m in self.modules():
            if isinstance(m, nn.Conv2d) or isinstance(m, nn.BatchNorm2d):
                init_weights(m, init_type='kaiming')

    def forward(self, inputs):
        # Encoder path
        conv1 = self.conv1(inputs)
        maxpool1 = self.maxpool1(conv1)

        conv2 = self.conv2(maxpool1)
        maxpool2 = self.maxpool2(conv2)

        conv3 = self.conv3(maxpool2)
        maxpool3 = self.maxpool3(conv3)

        conv4 = self.conv4(maxpool3)
        maxpool4 = self.maxpool4(conv4)

        center = self.center(maxpool4)

        # Decoder path: only skip and gating are passed, no prompt at all
        up4 = self.up_concat4(skip=conv4, gating=center)
        up3 = self.up_concat3(skip=conv3, gating=up4)
        up2 = self.up_concat2(skip=conv2, gating=up3)
        up1 = self.up_concat1(skip=conv1, gating=up2)

        final = self.final(up1)
        return final