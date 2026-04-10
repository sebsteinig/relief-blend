"""Low-level blending functions (numpy only)."""

import numpy as np


def multiply_blend(base, layer, opacity=1.0):
    """Multiply-blend two RGBA uint8 arrays.

    Parameters
    ----------
    base : np.ndarray
        Base image, shape (H, W, 4), dtype uint8.
    layer : np.ndarray
        Layer image (e.g. shaded relief), shape (H, W, 4), dtype uint8.
    opacity : float
        Blend strength between 0 (no effect) and 1 (full multiply blend).

    Returns
    -------
    np.ndarray
        Blended image, shape (H, W, 4), dtype uint8.
    """
    base_f = base[:, :, :3].astype(np.float64) / 255.0
    layer_f = layer[:, :, :3].astype(np.float64) / 255.0
    blended = base_f * layer_f
    result = blended * opacity + base_f * (1.0 - opacity)
    out = base.copy()
    out[:, :, :3] = np.clip(result * 255.0, 0, 255).astype(np.uint8)
    return out
