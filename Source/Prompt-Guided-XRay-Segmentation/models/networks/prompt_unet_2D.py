import torch
import torch.nn as nn
import torch.nn.functional as F


class unetConv2(nn.Module):
    def __init__(self, in_size, out_size, is_batchnorm=True):
        super().__init__()
        if is_batchnorm:
            self.conv1 = nn.Sequential(nn.Conv2d(in_size, out_size, 3, 1, 1),
                                       nn.BatchNorm2d(out_size), nn.ReLU(inplace=True))
            self.conv2 = nn.Sequential(nn.Conv2d(out_size, out_size, 3, 1, 1),
                                       nn.BatchNorm2d(out_size), nn.ReLU(inplace=True))
        else:
            self.conv1 = nn.Sequential(nn.Conv2d(in_size, out_size, 3, 1, 1), nn.ReLU(inplace=True))
            self.conv2 = nn.Sequential(nn.Conv2d(out_size, out_size, 3, 1, 1), nn.ReLU(inplace=True))

    def forward(self, x):
        return self.conv2(self.conv1(x))


class PromptSpatialGate(nn.Module):
    """
    Uses the prompt heatmap to enhance encoder features in the prompted region.
    Formula: out = features * (1 + alpha * gate(prompt))
    It never suppresses a feature, it only boosts the prompted region.
    Alpha is learnable and starts small (0.1) so it does not disrupt early training.
    """
    def __init__(self, feature_channels):
        super().__init__()
        self.gate_conv = nn.Sequential(
            nn.Conv2d(1, feature_channels, kernel_size=1, bias=True),
            nn.Sigmoid()
        )
        self.alpha = nn.Parameter(torch.tensor(0.1))

    def forward(self, features, prompt):
        if prompt.shape[2:] != features.shape[2:]:
            prompt = F.interpolate(prompt, size=features.shape[2:],
                                   mode='bilinear', align_corners=False)
        gate  = self.gate_conv(prompt)
        alpha = torch.clamp(self.alpha, 0.0, 1.0)
        return features * (1.0 + alpha * gate)


class unetUp_PromptAttention(nn.Module):
    def __init__(self, skip_channels, gating_channels, out_channels, prompt_weight=1.0):
        super().__init__()
        self.alpha_raw = nn.Parameter(torch.tensor(-0.84))
        self.w         = prompt_weight
        self.beta      = nn.Parameter(torch.tensor(0.05))

        from models.layers.grid_attention_layer import GridAttentionBlock2D
        self.attention = GridAttentionBlock2D(
            in_channels=skip_channels,
            gating_channels=gating_channels,
            inter_channels=skip_channels // 2,
            sub_sample_factor=(2, 2)
        )

        self.prompt_encoder = nn.Sequential(
            nn.Conv2d(1, gating_channels // 2, 3, padding=1, bias=True),
            nn.InstanceNorm2d(gating_channels // 2),
            nn.ReLU(inplace=True),
            nn.Conv2d(gating_channels // 2, gating_channels, 3, padding=1, bias=True),
            nn.InstanceNorm2d(gating_channels),
            nn.ReLU(inplace=True)
        )

        self.prompt_confidence = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(gating_channels, 1, 1),
            nn.Sigmoid()
        )

        self.up   = nn.ConvTranspose2d(gating_channels, skip_channels,
                                       kernel_size=4, stride=2, padding=1)
        self.conv = unetConv2(skip_channels * 2, out_channels, is_batchnorm=True)

    def forward(self, skip, gating, prompt):
        prompt_rs = prompt if prompt.shape[2:] == gating.shape[2:] else \
                    F.interpolate(prompt, size=gating.shape[2:], mode='bilinear', align_corners=False)

        p_encoded = self.prompt_encoder(prompt_rs)
        conf      = self.prompt_confidence(p_encoded)
        # Exposed for PGA_UNet.forward(..., return_confidence=True); not used
        # in the forward computation itself, so detaching costs nothing.
        self.last_conf = conf.detach()
        alpha     = torch.sigmoid(self.alpha_raw)
        g_fused   = gating + (conf * alpha * self.w * p_encoded)

        skip_att = self.attention(skip, g_fused)
        if isinstance(skip_att, tuple):
            skip_att = skip_att[0]
        skip_att = skip_att + 0.3 * skip

        up_gating = self.up(gating)
        diffY = up_gating.size(2) - skip_att.size(2)
        diffX = up_gating.size(3) - skip_att.size(3)
        skip_att = F.pad(skip_att, [diffX // 2, diffX - diffX // 2,
                                    diffY // 2, diffY - diffY // 2])

        out      = self.conv(torch.cat([skip_att, up_gating], dim=1))
        p_refine = F.interpolate(prompt, size=out.shape[2:],
                                 mode='bilinear', align_corners=False)
        return out + self.beta * p_refine


class QualityHead(nn.Module):
    """Predicts the model's own expected Dice for the current sample, trained
    by regression against the real Dice (computed with GT, only available
    during training). At inference this needs no ground truth at all: it is
    a learned no-GT quality/confidence estimate, complementary to CAD's
    prompt-confidence gates, which only reflect trust in the prompt rather
    than the final predicted mask.

    Takes three things concatenated at full spatial resolution, not just a
    pooled abstract feature vector: the final decoder features (image and
    prompt context), the predicted probability map (what the model actually
    produced), and the prompt heatmap (what region was asked for). Two 3x3
    convolutions let it compare these spatially, for example whether the
    predicted mask extends past the prompted region or fails to align with
    it, before pooling down to a single score.
    """
    def __init__(self, in_channels):
        super().__init__()
        self.mix = nn.Sequential(
            nn.Conv2d(in_channels + 2, in_channels, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels, in_channels, 3, padding=1),
            nn.ReLU(inplace=True),
        )
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(in_channels, max(in_channels // 2, 4)),
            nn.ReLU(inplace=True),
            nn.Linear(max(in_channels // 2, 4), 1),
            nn.Sigmoid(),
        )

    def forward(self, decoder_features, prob_map, prompt_map):
        x = torch.cat([decoder_features, prob_map, prompt_map], dim=1)
        x = self.mix(x)
        pooled = self.pool(x).flatten(1)
        return self.fc(pooled).squeeze(1)


class PGA_UNet(nn.Module):
    """
    Prompt-Guided Attention UNet.
    use_encoder_prompt=True adds a PromptSpatialGate at every encoder level.
    use_encoder_prompt=False matches the original baseline (prompt only reaches the decoder).
    """

    def __init__(self, feature_scale=4, n_classes=1, in_channels=1,
                 is_batchnorm=True, use_encoder_prompt=True,
                 prompt_weights=(1.0, 0.7, 0.4, 0.2),
                 use_quality_head=False):
        super().__init__()
        self.use_encoder_prompt = use_encoder_prompt
        self.use_quality_head   = use_quality_head

        w = list(prompt_weights)
        assert len(w) == 4, "prompt_weights must have exactly 4 elements (4 decoder levels)"

        filters = [int(x / feature_scale) for x in [64, 128, 256, 512, 1024]]
        # filters = [16, 32, 64, 128, 256]

        # Encoder
        self.conv1    = unetConv2(in_channels, filters[0], is_batchnorm)
        self.maxpool1 = nn.MaxPool2d(2)
        self.conv2    = unetConv2(filters[0], filters[1], is_batchnorm)
        self.maxpool2 = nn.MaxPool2d(2)
        self.conv3    = unetConv2(filters[1], filters[2], is_batchnorm)
        self.maxpool3 = nn.MaxPool2d(2)
        self.conv4    = unetConv2(filters[2], filters[3], is_batchnorm)
        self.maxpool4 = nn.MaxPool2d(2)
        self.center   = unetConv2(filters[3], filters[4], is_batchnorm)

        # Optional prompt gates for the encoder
        if use_encoder_prompt:
            self.pg1 = PromptSpatialGate(filters[0])
            self.pg2 = PromptSpatialGate(filters[1])
            self.pg3 = PromptSpatialGate(filters[2])
            self.pg4 = PromptSpatialGate(filters[3])

        # Decoder with prompt-guided attention
        self.up_concat4 = unetUp_PromptAttention(filters[3], filters[4], filters[3], prompt_weight=w[0])
        self.up_concat3 = unetUp_PromptAttention(filters[2], filters[3], filters[2], prompt_weight=w[1])
        self.up_concat2 = unetUp_PromptAttention(filters[1], filters[2], filters[1], prompt_weight=w[2])
        self.up_concat1 = unetUp_PromptAttention(filters[0], filters[1], filters[0], prompt_weight=w[3])

        self.final = nn.Conv2d(filters[0], n_classes, 1)

        # Optional: adds new parameters, so only construct it when requested,
        # otherwise a checkpoint saved with use_quality_head=False (the
        # default, matching every checkpoint trained so far) still loads
        # cleanly into a model built with the default constructor arguments.
        if use_quality_head:
            self.quality_head = QualityHead(filters[0])

    def forward(self, inputs, prompt, return_confidence=False, return_quality=False):
        # Model-level augmentation, training only
        if self.training:
            r = torch.rand(1).item()
            if r < 0.15:
                prompt = torch.zeros_like(prompt)
            elif r < 0.30:
                prompt = torch.clamp(prompt + torch.randn_like(prompt) * 0.1, 0, 1)

        # Encoder
        c1 = self.conv1(inputs)
        if self.use_encoder_prompt:
            c1 = self.pg1(c1, prompt)

        c2 = self.conv2(self.maxpool1(c1))
        if self.use_encoder_prompt:
            c2 = self.pg2(c2, prompt)

        c3 = self.conv3(self.maxpool2(c2))
        if self.use_encoder_prompt:
            c3 = self.pg3(c3, prompt)

        c4 = self.conv4(self.maxpool3(c3))
        if self.use_encoder_prompt:
            c4 = self.pg4(c4, prompt)

        center = self.center(self.maxpool4(c4))

        # Decoder
        up4 = self.up_concat4(c4, center, prompt)
        up3 = self.up_concat3(c3, up4,    prompt)
        up2 = self.up_concat2(c2, up3,    prompt)
        up1 = self.up_concat1(c1, up2,    prompt)

        logits = self.final(up1)

        outputs = [logits]
        if return_confidence:
            # No-GT "prompt confidence" signal: the CAD gate at each decoder
            # level already learns how much to trust the prompt encoding
            # there (see unetUp_PromptAttention.prompt_confidence);
            # averaging the 4 levels gives one scalar per sample in [0, 1],
            # with no ground truth involved.
            prompt_confidence = torch.cat([
                self.up_concat4.last_conf.flatten(1),
                self.up_concat3.last_conf.flatten(1),
                self.up_concat2.last_conf.flatten(1),
                self.up_concat1.last_conf.flatten(1),
            ], dim=1).mean(dim=1)
            outputs.append(prompt_confidence)

        if return_quality:
            if not self.use_quality_head:
                raise RuntimeError(
                    "return_quality=True requires the model to be constructed "
                    "with use_quality_head=True."
                )
            # No-GT "result confidence": a learned estimate of this sample's
            # own Dice, trained by regression against the real Dice during
            # training (see LOSS_CONFIDENCE_WEIGHT in train.py). Needs no
            # ground truth at inference. Gives QualityHead the decoder
            # features, the predicted probability map, and the prompt
            # heatmap, so it can compare the actual mask and the requested
            # region rather than only summarizing an abstract feature
            # vector. Everything is detached first: up1 and logits are the
            # same tensors self.final() used for the segmentation output,
            # so without detaching, the confidence loss's gradient would
            # also flow back into the shared decoder and quietly perturb
            # segmentation quality. Detaching makes this head a pure
            # observer that never influences segmentation training.
            prob_map = torch.sigmoid(logits).detach()
            outputs.append(self.quality_head(up1.detach(), prob_map, prompt.detach()))

        return outputs[0] if len(outputs) == 1 else tuple(outputs)