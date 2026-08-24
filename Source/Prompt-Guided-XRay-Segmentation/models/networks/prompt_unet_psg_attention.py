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


class unetUp_Attention(nn.Module):
    """ORIGINAL attention gate (not prompt-conditioned) - identical to Attention U-Net.
    Compared with CAD (unetUp_PromptAttention): remove prompt injection into the gating signal (g_fused)
    and remove the output-side prompt residual (p_refine); all remaining parts (attention gate, residual +0.3*skip,
    up-conv, concat-conv) are kept identical to ensure a fair comparison."""
    def __init__(self, skip_channels, gating_channels, out_channels):
        super().__init__()
        from models.layers.grid_attention_layer import GridAttentionBlock2D
        self.attention = GridAttentionBlock2D(
            in_channels=skip_channels,
            gating_channels=gating_channels,
            inter_channels=skip_channels // 2,
            sub_sample_factor=(2, 2)
        )
        self.up   = nn.ConvTranspose2d(gating_channels, skip_channels, kernel_size=4, stride=2, padding=1)
        self.conv = unetConv2(skip_channels * 2, out_channels, is_batchnorm=True)

    def forward(self, skip, gating):
        skip_att = self.attention(skip, gating)
        if isinstance(skip_att, tuple):
            skip_att = skip_att[0]
        skip_att = skip_att + 0.3 * skip

        up_gating = self.up(gating)
        diffY = up_gating.size(2) - skip_att.size(2)
        diffX = up_gating.size(3) - skip_att.size(3)
        skip_att = F.pad(skip_att, [diffX // 2, diffX - diffX // 2,
                                    diffY // 2, diffY - diffY // 2])
        return self.conv(torch.cat([skip_att, up_gating], dim=1))


class PGA_UNet(nn.Module):
    """PSG in the encoder with a vanilla unconditioned attention gate in the decoder: no CAD."""
    def __init__(self, feature_scale=4, n_classes=1, in_channels=1,
                 is_batchnorm=True, use_encoder_prompt=True):
        super().__init__()
        F_ = [int(x / feature_scale) for x in [64, 128, 256, 512, 1024]]
        self.enc1 = unetConv2(1, F_[0], is_batchnorm); self.enc2 = unetConv2(F_[0], F_[1], is_batchnorm)
        self.enc3 = unetConv2(F_[1], F_[2], is_batchnorm); self.enc4 = unetConv2(F_[2], F_[3], is_batchnorm)
        self.ctr  = unetConv2(F_[3], F_[4], is_batchnorm); self.pool = nn.MaxPool2d(2)
        self.pg1 = PromptSpatialGate(F_[0]); self.pg2 = PromptSpatialGate(F_[1])
        self.pg3 = PromptSpatialGate(F_[2]); self.pg4 = PromptSpatialGate(F_[3])
        self.up4 = unetUp_Attention(F_[3], F_[4], F_[3]); self.up3 = unetUp_Attention(F_[2], F_[3], F_[2])
        self.up2 = unetUp_Attention(F_[1], F_[2], F_[1]); self.up1 = unetUp_Attention(F_[0], F_[1], F_[0])
        self.final = nn.Conv2d(F_[0], n_classes, 1)

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
