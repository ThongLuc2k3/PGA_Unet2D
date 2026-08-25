"""Shared helpers for exporting one qualitative segmentation case per image."""

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import binary_erosion, distance_transform_edt, label as connected_components


METRIC_KEYS = {
    "Dice": ("dice",),
    "IoU": ("iou",),
    "Precision": ("precision", "pre"),
    "Recall": ("recall", "rec"),
    "HD95": ("hd95",),
    "CBL": ("cbl",),
}


def select_shared_stems(records, n_multi=5, n_single=5, name_key="img_name",
                        polygon_key="n_samples"):
    """Select the same deterministic stem order for every model and prompt mode."""
    records = sorted(records, key=lambda record: str(record[name_key]))
    target_count = n_multi + n_single
    stems = [str(record[name_key]) for record in records[:target_count]]
    if not stems:
        raise ValueError("No qualitative image stems are available")
    return stems


def resolve_runtime_path(relative_path):
    """Resolve a project path in local, Colab, or Kaggle notebook runtimes."""
    relative_path = Path(relative_path)
    if relative_path.is_absolute() and relative_path.exists():
        return relative_path

    package_suffix = Path("Source/Prompt-Guided-XRay-Segmentation")
    candidates = [Path.cwd()]
    candidates.extend(Path.cwd().parents)
    candidates.extend([
        Path("/content/PGA_Unet2D") / package_suffix,
        Path("/kaggle/working/PGA_Unet2D") / package_suffix,
        Path("/content/Prompt-Guided-XRay-Segmentation"),
        Path("/kaggle/working/Prompt-Guided-XRay-Segmentation"),
    ])
    searched = []
    for root in candidates:
        candidate = root / relative_path
        searched.append(str(candidate))
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"Could not resolve '{relative_path}' in local, Colab, or Kaggle paths. "
        f"Checked: {searched}"
    )


def records_for_stems(records, stems, name_key="img_name", context="records"):
    """Return records in exact stem order and fail if any requested stem is missing."""
    by_stem = {str(record[name_key]): record for record in records}
    missing = [stem for stem in stems if stem not in by_stem]
    if missing:
        raise KeyError(f"{context} is missing qualitative stems: {missing}")
    return [by_stem[stem] for stem in stems]


def _metric_source(record):
    if isinstance(record, (tuple, list)) and len(record) == 2 and isinstance(record[1], dict):
        record = record[1]
    if not isinstance(record, dict):
        return {}
    source = dict(record.get("m", {})) if isinstance(record.get("m"), dict) else dict(record)
    if all(any(source.get(key) is not None for key in keys) for keys in METRIC_KEYS.values()):
        return source

    gt = record.get("gt")
    pred = record.get("pred", record.get("prob"))
    if gt is None or pred is None:
        return source
    gt = np.asarray(gt) > 0.5
    pred = np.asarray(pred) > 0.5
    eps = 1e-6
    tp = np.logical_and(pred, gt).sum()
    fp = np.logical_and(pred, ~gt).sum()
    fn = np.logical_and(~pred, gt).sum()
    source.setdefault("dice", float((2 * tp + eps) / (2 * tp + fp + fn + eps)))
    source.setdefault("iou", float((tp + eps) / (tp + fp + fn + eps)))
    source.setdefault("precision", float(tp / (tp + fp + eps)))
    source.setdefault("recall", float((tp + eps) / (tp + fn + eps)))

    hd95 = float(max(gt.shape))
    if pred.any() and gt.any():
        pred_edge = pred ^ binary_erosion(pred)
        gt_edge = gt ^ binary_erosion(gt)
        d1 = distance_transform_edt(~gt_edge)[pred_edge]
        d2 = distance_transform_edt(~pred_edge)[gt_edge]
        if len(d1) and len(d2):
            hd95 = float(max(np.percentile(d1, 95), np.percentile(d2, 95)))
    source.setdefault("hd95", hd95)

    cbl = 0.0
    if pred.any() and gt.any():
        gy, gx = np.where(gt)
        py, px = np.where(pred)
        gt_diag = np.hypot(gy.max() - gy.min(), gx.max() - gx.min()) + eps
        center_distance = np.hypot(px.mean() - gx.mean(), py.mean() - gy.mean())
        cbl = float(np.clip(1.0 - center_distance / gt_diag, 0.0, 1.0))
    source.setdefault("cbl", cbl)
    return source


def _metric_value(record, keys):
    source = _metric_source(record)
    for key in keys:
        value = source.get(key)
        if value is not None:
            return float(value)
    return float("nan")


def _record_name(record, index):
    if isinstance(record, (tuple, list)) and len(record) == 2 and isinstance(record[1], dict):
        return str(record[0])
    if isinstance(record, dict):
        for key in ("img_name", "stem", "image_name", "name"):
            if record.get(key):
                return str(record[key])
        if record.get("idx") is not None:
            return f"sample_{record['idx']}"
    return f"sample_{index + 1:02d}"


def _safe_name(value):
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", str(value)).strip("_")
    return value or "qualitative_result"


def _resize_panel(panel, height, width):
    """Resize an RGB panel with nearest-neighbor indexing without extra dependencies."""
    if panel.shape[:2] == (height, width):
        return panel
    y_index = np.linspace(0, panel.shape[0] - 1, height).round().astype(int)
    x_index = np.linspace(0, panel.shape[1] - 1, width).round().astype(int)
    return panel[y_index][:, x_index]


def _colored_mask(panel, threshold=5):
    panel = panel.astype(np.int16)
    return panel.max(axis=-1) - panel.min(axis=-1) >= threshold


def _record_mapping(record):
    if isinstance(record, (tuple, list)) and len(record) == 2 and isinstance(record[1], dict):
        return record[1]
    return record if isinstance(record, dict) else {}


def _record_binary_mask(record, keys, height, width):
    source = _record_mapping(record)
    value = next((source.get(key) for key in keys if source.get(key) is not None), None)
    nested_metrics = source.get("m") if isinstance(source.get("m"), dict) else {}
    if value is None and any(key in keys for key in ("pred", "prob", "prediction")):
        value = next(
            (nested_metrics.get(key) for key in ("pred", "prob", "prediction", "mask")
             if nested_metrics.get(key) is not None),
            None,
        )
    if value is None:
        return None
    value = np.asarray(value)
    value = np.squeeze(value)
    if value.ndim == 3:
        channel_axis = 0 if value.shape[0] <= 4 else -1
        value = value.max(axis=channel_axis)
    if value.ndim != 2:
        return None
    if value.shape != (height, width):
        y_index = np.linspace(0, value.shape[0] - 1, height).round().astype(int)
        x_index = np.linspace(0, value.shape[1] - 1, width).round().astype(int)
        value = value[y_index][:, x_index]
    return value > 0.5


def _record_prompt_map(record, height, width):
    source = _record_mapping(record)
    value = next(
        (source.get(key) for key in ("prompts", "prompt", "prompt_mask", "heatmap", "hm")
         if source.get(key) is not None),
        None,
    )
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        maps = [np.squeeze(np.asarray(item)) for item in value]
        maps = [item for item in maps if item.ndim == 2]
        if not maps:
            return None
        value = np.max(np.stack(maps, axis=0), axis=0)
    else:
        value = np.squeeze(np.asarray(value))
        if value.ndim == 3:
            channel_axis = 0 if value.shape[0] <= 4 else -1
            value = value.max(axis=channel_axis)
    if value.ndim != 2:
        return None
    if value.shape != (height, width):
        y_index = np.linspace(0, value.shape[0] - 1, height).round().astype(int)
        x_index = np.linspace(0, value.shape[1] - 1, width).round().astype(int)
        value = value[y_index][:, x_index]
    return np.clip(value.astype(np.float32), 0.0, 1.0)


def _blend_color(output, region, color, alpha=0.62):
    output[region] = output[region] * (1.0 - alpha) + color * alpha


def _filled_box_mask_from_panel(source_panel):
    """Convert rendered colored box outlines into filled rectangular prompts."""
    outline = _colored_mask(source_panel)
    components, count = connected_components(outline)
    filled = np.zeros(outline.shape, dtype=bool)
    for component_index in range(1, count + 1):
        ys, xs = np.where(components == component_index)
        if len(xs) < 4:
            continue
        filled[ys.min():ys.max() + 1, xs.min():xs.max() + 1] = True
    return filled


def _overlay_role_on_input(input_panel, source_panel, role, record):
    """Keep the input X-ray visible and transfer only colored annotations."""
    height, width = input_panel.shape[:2]
    source_panel = _resize_panel(source_panel, height, width)
    output = input_panel.astype(np.float32).copy()
    if role == "Prompt":
        prompt_map = _record_prompt_map(record, height, width)
        if prompt_map is not None:
            intermediate = (prompt_map > 1e-4) & (prompt_map < 1.0 - 1e-4)
            is_gaussian = np.count_nonzero(intermediate) >= 8
            if is_gaussian:
                region = prompt_map > 1e-4
                hot_rgb = plt.get_cmap("hot")(prompt_map)[..., :3] * 255.0
                output[region] = output[region] * 0.60 + hot_rgb[region] * 0.40
            else:
                region = prompt_map > 0.5
                _blend_color(output, region, np.array([255, 255, 255], dtype=np.float32), alpha=0.40)
        else:
            region = _filled_box_mask_from_panel(source_panel)
            _blend_color(output, region, np.array([255, 255, 255], dtype=np.float32), alpha=0.40)
    elif role == "Prediction":
        mask = _record_binary_mask(record, ("pred", "prob", "prediction"), height, width)
        if mask is None:
            raise KeyError("Prediction qualitative record must contain 'pred' or 'prob'")
        color = np.array([235, 45, 70], dtype=np.float32)
        _blend_color(output, mask, color)
    elif role == "Ground Truth":
        mask = _record_binary_mask(record, ("gt", "ground_truth", "mask"), height, width)
        if mask is None:
            raise KeyError("Ground-truth qualitative record must contain 'gt'")
        color = np.array([35, 210, 90], dtype=np.float32)
        _blend_color(output, mask, color)
    elif role == "TP/FP/FN":
        pred = _record_binary_mask(record, ("pred", "prob", "prediction"), height, width)
        gt = _record_binary_mask(record, ("gt", "ground_truth", "mask"), height, width)
        if pred is None or gt is None:
            raise KeyError("TP/FP/FN qualitative record must contain both prediction and ground truth")
        green = pred & gt
        red = pred & ~gt
        blue = ~pred & gt
        for region, color in (
            (red, np.array([235, 45, 45], dtype=np.float32)),
            (green, np.array([35, 210, 90], dtype=np.float32)),
            (blue, np.array([45, 90, 235], dtype=np.float32)),
        ):
            _blend_color(output, region, color)
    return np.clip(output, 0, 255).astype(np.uint8)


def export_qualitative_rows(fig, axes, records, output_dir="results/qualitative", prefix=None,
                            metric_fontsize=11, dpi=150, display_images=True):
    """Save and display each axes row as one standalone qualitative result image."""
    if display_images:
        from IPython.display import Image, display

    axes = np.asarray(axes, dtype=object)
    if axes.ndim == 1:
        axes = axes[np.newaxis, :]
    records = list(records)
    if len(records) != axes.shape[0]:
        raise ValueError(f"Expected {axes.shape[0]} records for {axes.shape[0]} axes rows, got {len(records)}")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if prefix is None:
        title = fig._suptitle.get_text() if fig._suptitle is not None else "qualitative_result"
        prefix = _safe_name(title)

    column_labels = {
        4: ("Input", "Prediction", "Ground Truth", "TP/FP/FN"),
        5: ("Input", "Prompt", "Prediction", "Ground Truth", "TP/FP/FN"),
    }.get(axes.shape[1])
    if column_labels is None:
        raise ValueError(
            f"Qualitative figures must have 4 columns without prompts or 5 columns "
            f"with prompts, got {axes.shape[1]} columns"
        )

    fig.canvas.draw()
    source_rgba = np.asarray(fig.canvas.buffer_rgba()).copy()
    source_height = source_rgba.shape[0]
    saved_paths = []
    for index, (row_axes, record) in enumerate(zip(axes, records)):
        values = {label: _metric_value(record, keys) for label, keys in METRIC_KEYS.items()}
        metric_text = "   ".join(
            f"{label}: {value:.2f}" if label == "HD95" else f"{label}: {value:.3f}"
            for label, value in values.items()
        )

        panel_images = []
        for ax in row_axes:
            x0, y0, x1, y1 = (int(round(value)) for value in ax.bbox.extents)
            top = max(0, source_height - y1)
            bottom = min(source_height, source_height - y0)
            panel_images.append(source_rgba[top:bottom, max(0, x0):max(0, x1), :3])

        input_panel = panel_images[0]
        panel_images = [
            input_panel if label == "Input" else _overlay_role_on_input(input_panel, panel, label, record)
            for panel, label in zip(panel_images, column_labels)
        ]

        row_fig, row_axes_new = plt.subplots(
            1, len(column_labels), figsize=(4 * len(column_labels), 4.6), squeeze=False)
        row_fig.patch.set_facecolor("white")
        row_axes_new = row_axes_new[0]
        for ax, panel_image, label in zip(row_axes_new, panel_images, column_labels):
            ax.imshow(panel_image)
            ax.set_title(label, fontsize=11, fontweight="bold", color="black", pad=6)
            ax.axis("off")
        row_fig.subplots_adjust(left=0.01, right=0.99, top=0.90, bottom=0.15, wspace=0.04)
        row_fig.text(
            0.5, 0.055, metric_text, ha="center", va="center", color="red",
            fontsize=metric_fontsize, fontweight="bold",
        )

        record_name = _safe_name(_record_name(record, index))
        output_path = output_dir / f"{_safe_name(prefix)}_{index + 1:02d}_{record_name}.png"
        row_fig.savefig(output_path, dpi=dpi, facecolor="white")
        saved_paths.append(str(output_path))
        plt.close(row_fig)

        if display_images:
            display(Image(filename=str(output_path)))

    plt.close(fig)
    return saved_paths
