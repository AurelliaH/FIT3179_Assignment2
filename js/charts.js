/* Loads every Vega-Lite spec on the page.
   To add a chart: put its .vg.json in js/, add one line to CHARTS,
   and put <div class="vis" id="..."></div> in index.html. */

const CHARTS = [
  { id: "vis-trend",      spec: "js/01_trend_line.vg.json" },
  { id: "vis-waffle",     spec: "js/02_waffle.vg.json" },
  { id: "vis-choropleth", spec: "js/03_choropleth_sa4.vg.json" },
  { id: "vis-dotmap",     spec: "js/04_dotdensity_sa4.vg.json" },
  { id: "vis-bivariate",  spec: "js/05_bivariate_sa4.vg.json" },
  { id: "vis-agemaps",    spec: "js/06_agemaps_sa4.vg.json" },
  { id: "vis-ranked",     spec: "js/07_ranked_regions.vg.json" },
  { id: "vis-scatter",    spec: "js/08_scatter_size_rate.vg.json" },
  { id: "vis-dumbbell",   spec: "js/09_dumbbell_state.vg.json" },
  { id: "vis-cartogram",  spec: "js/10_cartogram_state.vg.json" },
  { id: "vis-pyramid",    spec: "js/11_pyramid.vg.json" },
  { id: "vis-heatmap",    spec: "js/12_heatmap_age_state.vg.json" },
  { id: "vis-ridgeline",  spec: "js/13_ridgeline_ageband.vg.json" },
  { id: "vis-purposebars",spec: "js/14_purpose_bars.vg.json" }
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
