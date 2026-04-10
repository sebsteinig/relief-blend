# relief-blend

Multiply-blend shaded relief onto matplotlib / earthkit-plots map images.

> **Limitation:** Currently only works with a single `ekp.Map` chart. Multiple maps on an earthkit-plots `Figure` are not supported yet.

## Install

```bash
pip install -e /path/to/relief-blend          # editable install
pip install -e /path/to/relief-blend[earthkit]  # with earthkit-plots + cartopy
```

## Usage

```python
import earthkit.plots as ekp
from earthkit.plots import Style
from relief_blend import apply_shaded_relief

chart = ekp.Map(domain="Global")
chart.contourf(data, style=style)
chart.coastlines()
chart.land()
chart.legend()
chart.title("My title")

# One call — saves the native earthkit-plots image, then blends relief on top
apply_shaded_relief(chart, "output.png", intensity=0.8, dpi=150)
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `chart` | — | A fully configured `earthkit.plots.Map` |
| `output_path` | — | Output file path |
| `relief_path` | bundled Natural Earth | Path to a global equirectangular relief image |
| `intensity` | `1.0` | Blend strength: 0 = no effect, 1 = full multiply |
| `dpi` | `150` | Output DPI |

### Low-level API

```python
from relief_blend import multiply_blend

blended = multiply_blend(base_rgba, layer_rgba, opacity=0.7)
```

## How it works

1. `chart.save()` produces the master PNG (100% native earthkit-plots output)
2. The map-axes pixel region is located in the saved image
3. A matching relief figure is rendered with the same projection/domain
4. Only the map region is multiply-blended; title, colorbar, and all decorations are untouched
5. The result overwrites the output file

## Dependencies

- `numpy`, `pillow`, `matplotlib` (core)
- `earthkit-plots`, `cartopy` (optional, for the high-level `apply_shaded_relief` API)

## License

MIT
