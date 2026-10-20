/* Shared Vega-Lite config — one place for every chart's typography and axis colour.
   Tuned for the dark page: charts sit on the --panel surface (#1A4244), so axis
   furniture is light-on-dark and grid lines are only just visible. */
const VL_CONFIG = {
  "background": "transparent",
  "font": "Public Sans, system-ui, sans-serif",
  "axis": {
    "labelFontSize": 14,
    "labelColor": "#B6CFC2",
    "titleFontSize": 14,
    "titleFontWeight": 500,
    "titleColor": "#93B2A4",
    "gridColor": "#27504E",
    "domainColor": "#34635E",
    "tickColor": "#34635E",
    "labelPadding": 8,
    "titlePadding": 13
  },
  "legend": {
    "labelFontSize": 14.5,
    "labelColor": "#DCEBE0",
    "titleFontSize": 13.5,
    "titleColor": "#93B2A4",
    "symbolType": "circle",
    "symbolSize": 140,
    "orient": "top",
    "direction": "horizontal",
    "offset": 16,
    "labelLimit": 260
  },
  "view": {
    "stroke": null
  }
};
