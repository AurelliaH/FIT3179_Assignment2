/* Loads every Vega-Lite spec on the page.
   To add a chart: put its .vg.json in js/, add one line to CHARTS,
   and put <div class="vis" id="..."></div> in index.html. */

const CHARTS = [
  { id: "vis-trend",      spec: "js/01_trend_line.vg.json" },
  { id: "vis-waffle",     spec: "js/02_waffle.vg.json" },
  { id: "vis-choropleth", spec: "js/03_choropleth_sa4.vg.json" },
  { id: "vis-symbolmap",  spec: "js/04_symbolmap_sa4.vg.json" },
  { id: "vis-agemaps",    spec: "js/05_agemaps_sa4.vg.json" },
  { id: "vis-ranked",     spec: "js/06_ranked_regions.vg.json" },
  { id: "vis-scatter",    spec: "js/07_scatter_size_rate.vg.json" },
  { id: "vis-dumbbell",   spec: "js/08_dumbbell_state.vg.json" },
  { id: "vis-cartogram",  spec: "js/09_cartogram_state.vg.json" },
  { id: "vis-pyramid",    spec: "js/10_pyramid.vg.json" },
  { id: "vis-heatmap",    spec: "js/11_heatmap_age_state.vg.json" },
  { id: "vis-beeswarm",   spec: "js/12_beeswarm_ageband.vg.json" },
  { id: "vis-purposebars",spec: "js/13_purpose_bars.vg.json" }
];

const EMBED_OPTIONS = { actions: false, renderer: "svg", config: VL_CONFIG };

CHARTS.forEach(function (chart) {
  const el = document.getElementById(chart.id);
  if (!el) return;
  vegaEmbed("#" + chart.id, chart.spec, EMBED_OPTIONS)
    .catch(function (err) {
      el.innerHTML = '<p class="chartSub"><b>This chart did not load.</b> ' + chart.spec + '</p>';
      console.error(chart.spec, err);
    });
});
