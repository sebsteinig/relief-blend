"""Example: CAMS PM2.5 exceedance days with shaded relief."""

import earthkit.data as ekd
import earthkit.plots as ekp
from earthkit.plots import Style
from relief_blend import apply_shaded_relief

# --- Data loading ---
ds = ekd.from_source(
    "file",
    "shaded_relief/data/cams-metrics/"
    "cams_0001_sfc_pm2p5_processed_2025_HEI-SOGA_relief_interim2.nc",
)
data = ds.to_xarray()["pm2p5_exceedance_days"]
data.attrs["units"] = "days"

LEVELS = [1, 5, 10, 15, 20, 25, 30, 60, 90, 120, 150]
style = Style(colors="YlOrRd", levels=LEVELS, extend="max")

# --- Build the chart normally ---
chart = ekp.Map(domain="Global")
chart.contourf(data, style=style)
chart.coastlines(resolution="medium", linewidth=0.5)
chart.land(resolution="medium", color="#EBEBEB")
chart.legend()
chart.title("Number of days with PM2.5 above 50 µg/m³ in 2025")

# --- Save with shaded relief (one function call) ---
apply_shaded_relief(chart, "output.png", intensity=1.0, dpi=150)
print("Saved to output.png")
