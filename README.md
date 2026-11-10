# CurveLq

Which method recovers the euro area yield curve best, and where does each one break?

## How to run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
```

Then, step by step:

```bash
python -m curvelab.data
python -m curvelab.plots
python -m curvelab.ns_params
python -m curvelab.holdout
python -m curvelab.summary
```

## Findings

The test: hide the 2Y, 7Y and 15Y rates, build the curve from the other 8 maturities and measure the error on the hidden ones. Data: ECB AAA spot rates, 2806 days, 2015-2025.

| Method | RMSE, bp | 2Y | 7Y | 15Y |
|---|---|---|---|---|
| Cubic spline | 0.88 | 1.09 | 0.63 | 0.84 |
| Nelson-Siegel | 3.65 | 2.71 | 2.34 | 5.20 |
| Linear | 4.94 | 4.60 | 2.74 | 6.68 |

The cubic spline is the most accurate method: 0.88 bp against 3.65 bp for Nelson-Siegel and 4.94 bp for linear interpolation. Nelson-Siegel works well in calm years (0.65 bp in 2018) but breaks from mid-2022: its error stays above 5 bp in 2022-2025 and peaks at 11.3 bp in October 2022, when it is often worse than plain linear interpolation. The likely reason is that four parameters cannot describe the fast rate hikes and the inverted curve, and the fitted curvature and lambda jump from day to day in that period. Linear interpolation does not break at one moment, it is steadily off where the curve bends, mostly at 15Y (6.68 bp) between the 10Y and 20Y points. One caveat: the ECB data is already a smooth model curve (Svensson), not raw bond prices, which favours a smooth method like the spline.
