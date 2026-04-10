"""High-level API for applying shaded relief to earthkit-plots maps."""

from __future__ import annotations

import io
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from .blend import multiply_blend

_BUILTIN_RELIEF = Path(__file__).parent / "data" / "NE_manual-shaded-relief.jpg"


def _render_axes_to_rgba(ax, fig, dpi):
    """Render a matplotlib Figure and extract just the axes region as RGBA."""
    fig.set_dpi(dpi)
    fig.canvas.draw()
    w, h = fig.canvas.get_width_height()
    full = (
        np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        .reshape(h, w, 4)
        .copy()
    )
    bbox = ax.get_window_extent(renderer=fig.canvas.get_renderer())
    x0, x1 = int(round(bbox.x0)), int(round(bbox.x1))
    y0, y1 = int(round(h - bbox.y1)), int(round(h - bbox.y0))
    return full[y0:y1, x0:x1]


def _axes_bbox_in_saved_image(chart, dpi):
    """Compute the map-axes pixel bbox inside a bbox_inches='tight' saved PNG.

    Returns (x0, y0, x1, y1) in image-array coordinates (origin top-left).
    """
    buf = io.BytesIO()
    chart.fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight")

    renderer = chart.fig.canvas.get_renderer()
    tight = chart.fig.get_tightbbox(renderer)  # inches
    ax_bbox = chart.ax.get_window_extent(renderer)  # display px at fig.dpi
    fig_dpi = chart.fig.dpi
    pad_inches = 0.1

    ax_x0_in = ax_bbox.x0 / fig_dpi
    ax_y0_in = ax_bbox.y0 / fig_dpi
    ax_x1_in = ax_bbox.x1 / fig_dpi
    ax_y1_in = ax_bbox.y1 / fig_dpi

    x0 = int(round((ax_x0_in - tight.x0 + pad_inches) * dpi))
    x1 = int(round((ax_x1_in - tight.x0 + pad_inches) * dpi))
    y0 = int(round((tight.y1 + pad_inches - ax_y1_in) * dpi))
    y1 = int(round((tight.y1 + pad_inches - ax_y0_in) * dpi))
    return x0, y0, x1, y1


def apply_shaded_relief(
    chart,
    output_path: str | Path,
    *,
    relief_path: str | Path | None = None,
    intensity: float = 1.0,
    dpi: int = 150,
):
    """Save an earthkit-plots Map with shaded relief blended in.

    1. Calls ``chart.save()`` to produce the master image (100% native
       earthkit-plots output).
    2. Locates the map-axes region inside the saved PNG.
    3. Renders the relief image on a matching projection figure.
    4. Multiply-blends only the map region and overwrites the file.

    Parameters
    ----------
    chart : earthkit.plots.Map
        A fully configured earthkit-plots Map (with data, coastlines,
        legend, title, etc. already added).
    output_path : str or Path
        Where to save the final image.
    relief_path : str, Path, or None
        Path to a global equirectangular shaded-relief image (e.g. Natural
        Earth). If *None*, uses the bundled relief asset.
    intensity : float
        Blend strength, 0 (no relief) to 1 (full multiply blend).
    dpi : int
        Output DPI.
    """
    import earthkit.plots as ekp

    output_path = Path(output_path)
    if relief_path is None:
        relief_path = _BUILTIN_RELIEF
    relief_path = str(relief_path)

    # Step 1: Save the chart exactly as earthkit-plots would
    chart.save(str(output_path), dpi=dpi)

    if intensity <= 0:
        return

    # Step 2: Locate map axes in the saved (tight-cropped) master image
    x0, y0, x1, y1 = _axes_bbox_in_saved_image(chart, dpi)

    master = np.array(Image.open(output_path).convert("RGBA"))
    x0, y0 = max(0, x0), max(0, y0)
    x1 = min(master.shape[1], x1)
    y1 = min(master.shape[0], y1)
    data_crop = master[y0:y1, x0:x1]

    # Step 3: Render relief on a matching figure, extract axes region
    relief_kwargs = {}
    if chart.domain is not None:
        relief_kwargs["domain"] = chart.domain
    relief_kwargs["crs"] = chart.crs

    relief_map = ekp.Map(**relief_kwargs)
    relief_map.image(relief_path, extent=[-180, 180, -90, 90])
    relief_map.figure._prepare_for_display()
    relief_crop = _render_axes_to_rgba(relief_map.ax, relief_map.fig, dpi)
    plt.close(relief_map.fig)
    plt.close(chart.fig)

    # Resize relief to match master's axes region
    target_h, target_w = data_crop.shape[:2]
    if relief_crop.shape[:2] != (target_h, target_w):
        relief_crop = np.array(
            Image.fromarray(relief_crop).resize(
                (target_w, target_h), Image.LANCZOS
            )
        )

    # Step 4: Blend and paste back
    blended_crop = multiply_blend(data_crop, relief_crop, opacity=intensity)
    master[y0:y1, x0:x1] = blended_crop

    # Step 5: Overwrite
    Image.fromarray(master).save(str(output_path), dpi=(dpi, dpi))
