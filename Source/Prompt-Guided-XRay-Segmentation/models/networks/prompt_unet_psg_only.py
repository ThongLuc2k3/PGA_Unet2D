import torch
import torch.nn as nn
import torch.nn.functional as F


class unetConv2(nn.Module):
    def __init__(self, in_size, out_size, is_batchnorm=True):
        super().__init__()
        if is_batchnorm:
            self.conv = nn.Sequential(
                nn.Conv2d(in_size, out_size, 3, 1, 1), nn.BatchNorm2d(out_size), nn.ReLU(inplace=True),
                nn.Conv2d(out_size, out_size, 3, 1, 1), nn.BatchNorm2d(out_size), nn.ReLU(inplace=True))
        else:
            self.conv = nn.Sequential(
                nn.Conv2d(in_size, out_size, 3, 1, 1), nn.ReLU(inplace=True),
                nn.Conv2d(out_size, out_size, 3, 1, 1), nn.ReLU(inplace=True))
    def forward(self, x): return self.conv(x)


class PromptSpatialGate(nn.Module):
    def __init__(self, feature_channels):
        super().__init__()
        self.gate_conv = nn.Sequential(nn.Conv2d(1, feature_channels, 1, bias=True), nn.Sigmoid())
        self.alpha = nn.Parameter(torch.tensor(0.1))
    def forward(self, features, prompt):
        if prompt.shape[2:] != features.shape[2:]:
            prompt = F.interpolate(prompt, size=features.shape[2:], mode='bilinear', align_corners=False)
        return features * (1.0 + torch.clamp(self.alpha, 0.0, 1.0) * self.gate_conv(prompt))


class unetUp_Standard(nn.Module):
    def __init__(self, skip_ch, gate_ch, out_ch):
        super().__init__()
        self.up   = nn.ConvTranspose2d(gate_ch, skip_ch, kernel_size=4, stride=2, padding=1)
        self.conv = unetConv2(skip_ch * 2, out_ch)
    def forward(self, skip, gating):
        u = self.up(gating)
        dy, dx = u.size(2)-skip.size(2), u.size(3)-skip.size(3)
        skip = F.pad(skip, [dx//2, dx-dx//2, dy//2, dy-dy//2])
        return self.conv(torch.cat([skip, u], dim=1))


class PGA_UNet(nn.Module):
    """PSG in the encoder only: standard decoder without conditioned attention."""
    def __init__(self, feature_scale=4, n_classes=1, in_channels=1,
                 is_batchnorm=True, use_encoder_prompt=True):
        super().__init__()
        F = [int(x / feature_scale) for x in [64, 128, 256, 512, 1024]]
        self.enc1 = unetConv2(1, F[0], is_batchnorm); self.enc2 = unetConv2(F[0], F[1], is_batchnorm)
        self.enc3 = unetConv2(F[1], F[2], is_batchnorm); self.enc4 = unetConv2(F[2], F[3], is_batchnorm)
        self.ctr  = unetConv2(F[3], F[4], is_batchnorm); self.pool = nn.MaxPool2d(2)
        self.pg1 = PromptSpatialGate(F[0]); self.pg2 = PromptSpatialGate(F[1])
        self.pg3 = PromptSpatialGate(F[2]); self.pg4 = PromptSpatialGate(F[3])
        self.up4 = unetUp_Standard(F[3], F[4], F[3]); self.up3 = unetUp_Standard(F[2], F[3], F[2])
        self.up2 = unetUp_Standard(F[1], F[2], F[1]); self.up1 = unetUp_Standard(F[0], F[1], F[0])
        self.final = nn.Conv2d(F[0], n_classes, 1)

    def forward(self, inputs, prompt):
        if self.training:
            r = torch.rand(1).item()
            if r < 0.15:   prompt = torch.zeros_like(prompt)
            elif r < 0.30: prompt = torch.clamp(prompt + torch.randn_like(prompt)*0.1, 0, 1)
        c1 = self.pg1(self.enc1(inputs), prompt)
        c2 = self.pg2(self.enc2(self.pool(c1)), prompt)
        c3 = self.pg3(self.enc3(self.pool(c2)), prompt)
        c4 = self.pg4(self.enc4(self.pool(c3)), prompt)
        ct = self.ctr(self.pool(c4))
        return self.final(self.up1(c1, self.up2(c2, self.up3(c3, self.up4(c4, ct)))))
