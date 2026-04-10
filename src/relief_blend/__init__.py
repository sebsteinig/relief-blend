"""relief-blend: multiply-blend shaded relief onto map plots."""

from .blend import multiply_blend
from .core import apply_shaded_relief

__all__ = ["apply_shaded_relief", "multiply_blend"]
