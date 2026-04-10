"""Example: CAMS PM2.5 exceedance days with shaded relief."""

import earthkit.data as ekd
import earthkit.plots as ekp
from earthkit.plots import Style
from relief_blend import apply_shaded_relief

# --- Data loading ---
ds = ekd.from_source(
    "file",
    "examples/data/"
    "cams_0001_sfc_pm2p5_processed_2025_HEI-SOGA_relief_interim2.nc",
)
data = ds.to_xarray()["pm2p5_exceedance_days"]
data.attrs["units"] = "days"

# --- Plot 1: levels starting at 1 ---
LEVELS_FROM_1 = [1, 5, 10, 15, 20, 25, 30, 60, 90, 120, 150]
style_from_1 = Style(colors="YlOrRd", levels=LEVELS_FROM_1, extend="max")

chart = ekp.Map(crs="EqualEarth")
chart.contourf(data, style=style_from_1)
chart.coastlines(resolution="medium", linewidth=0.5)
chart.land(resolution="medium", color="#EBEBEB")
chart.legend()
chart.title("PM2.5 exceedance days 2025 — levels from 1")

apply_shaded_relief(chart, "examples/pm2p5_relief_levels_from_1.png", intensity=1.0, dpi=300)
print("Saved examples/pm2p5_relief_levels_from_1.png")

# --- Plot 2: levels starting at 0 ---
LEVELS_FROM_0 = [0, 1, 5, 10, 15, 20, 25, 30, 60, 90, 120, 150]
style_from_0 = Style(colors="YlOrRd", levels=LEVELS_FROM_0, extend="max")

chart = ekp.Map(crs="EqualEarth")
chart.contourf(data, style=style_from_0)
chart.coastlines(resolution="medium", linewidth=0.5)
chart.land(resolution="medium", color="#EBEBEB")
chart.legend()
chart.title("PM2.5 exceedance days 2025 — levels from 0")

apply_shaded_relief(chart, "examples/pm2p5_relief_levels_from_0.png", intensity=1.0, dpi=300)
print("Saved examples/pm2p5_relief_levels_from_0.png")
