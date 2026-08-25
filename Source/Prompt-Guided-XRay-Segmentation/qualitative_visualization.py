"""Shared helpers for exporting one qualitative segmentation case per image."""

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.transforms import Bbox
from scipy.ndimage import binary_erosion, distance_transform_edt


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
    """Select deterministic qualitative stems from GT-derived polygon counts."""
    records = sorted(records, key=lambda record: str(record[name_key]))
    multi = [str(record[name_key]) for record in records if int(record.get(polygon_key, 1)) >= 2]
    single = [str(record[name_key]) for record in records if int(record.get(polygon_key, 1)) == 1]
    stems = multi[:n_multi] + single[:n_single]
    target_count = n_multi + n_single
    if len(stems) < target_count:
        fallback = [str(record[name_key]) for record in records if str(record[name_key]) not in stems]
        stems.extend(fallback[:target_count - len(stems)])
    if not stems:
        raise ValueError("No qualitative image stems are available")
    return stems


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


def export_qualitative_rows(fig, axes, records, output_dir="results/qualitative", prefix=None,
                            metric_fontsize=11, dpi=150, display_images=True):
    """Save and display each axes row as one standalone qualitative result image."""
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

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    saved_paths = []
    for index, (row_axes, record) in enumerate(zip(axes, records)):
        values = {label: _metric_value(record, keys) for label, keys in METRIC_KEYS.items()}
        metric_text = "   ".join(
            f"{label}: {value:.2f}" if label == "HD95" else f"{label}: {value:.3f}"
            for label, value in values.items()
        )

        positions = [ax.get_position() for ax in row_axes]
        x_center = 0.5 * (min(pos.x0 for pos in positions) + max(pos.x1 for pos in positions))
        y_bottom = min(pos.y0 for pos in positions)
        metric_artist = fig.text(
            x_center, y_bottom - 0.012, metric_text,
            ha="center", va="top", color="red", fontsize=metric_fontsize,
            fontweight="bold", transform=fig.transFigure,
        )
        fig.canvas.draw()

        row_bbox = Bbox.union([ax.get_tightbbox(renderer) for ax in row_axes])
        metric_bbox = metric_artist.get_window_extent(renderer=renderer)
        crop_bbox = Bbox.union([row_bbox, metric_bbox]).expanded(1.02, 1.08)
        crop_inches = crop_bbox.transformed(fig.dpi_scale_trans.inverted())

        record_name = _safe_name(_record_name(record, index))
        output_path = output_dir / f"{_safe_name(prefix)}_{index + 1:02d}_{record_name}.png"
        fig.savefig(output_path, dpi=dpi, bbox_inches=crop_inches, facecolor="white")
        saved_paths.append(str(output_path))
        metric_artist.remove()

        if display_images:
            display(Image(filename=str(output_path)))

    plt.close(fig)
    return saved_paths
